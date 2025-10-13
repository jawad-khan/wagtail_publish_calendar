import json

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from wagtail.models import Page, Revision, DraftStateMixin

from .forms import ScheduleForm


def calendar_view(request):
    """
    Renders the main calendar view and form for the modal.
    """
    form = ScheduleForm()
    context = {"form": form, "page_title": "Page Scheduler"}
    return render(
        request,
        "wagtail_publish_calendar/calendar.html",
        context
    )


def get_page_schedule_dates(request):
    """
    Creates event data with descriptive titles and color codes.
    """
    models = [Page]
    models += [
        model
        for model in apps.get_models()
        if issubclass(model, DraftStateMixin) and not issubclass(model, Page)
    ]

    # 1. get all expired objects with live = True
    expired_qs = []
    for model in models:
        expired_qs += [
            model.objects.filter(live=True, expire_at__gt=timezone.now()).order_by(
                "expire_at"
            )
        ]

    events = []
    for queryset in expired_qs:
        for obj in queryset:
            events.append(get_expire_event(obj))

    revisions = Revision.objects.filter(
        approved_go_live_at__gt=timezone.now()).order_by("approved_go_live_at")
    for event in revisions:
        events.append(get_publish_event(event))

    return JsonResponse(events, safe=False)


def get_publish_event(event):
    return {
        "id": f"{event.id}-start",
        "title": f"{event.object_str} (Go-live)",  # <-- COMBINED TITLE
        "start": event.approved_go_live_at.isoformat(),
        "color": "#008352",
        "extendedProps": {"type": "start"},
    }


def get_expire_event(event):
    revision = event.latest_revision
    return {
        "id": f"{revision.id}-end",
        "title": f"{revision.object_str} (Expire)",  # <-- COMBINED TITLE
        "start": event.expire_at.isoformat(),
        "color": "#cd4444",
        "extendedProps": {"type": "end"},
    }


def update_page_schedule_date(request):
    """
    Updates both go-live and expiry dates for a given page ID in a single
    request.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
        revision = Revision.objects.get(id=data.get("page_id"))

        # A null or empty string from the frontend means the date should be cleared
        go_live_str = data.get("go_live_at")
        expire_str = data.get("expire_at")

        revision.content_object.expire_at = parse_datetime(
            expire_str) if expire_str else None
        revision.content_object.save()

        revision.approved_go_live_at = parse_datetime(
            go_live_str) if go_live_str else None
        revision.save()

        return JsonResponse({"status": "ok",
                             "message": f"Schedule for '{revision.object_str}' updated."})

    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
