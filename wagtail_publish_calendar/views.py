"""
Views for wagtail_publish_calendar.
"""

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
    context = {"form": form, "page_title": "Content Scheduler"}
    return render(
        request,
        "wagtail_publish_calendar/calendar.html",
        context
    )


def get_page_schedule_dates(request):
    """
    Creates event data for all expirable and schedulable Wagtail content types.
    """
    models = [Page]
    models += [
        model
        for model in apps.get_models()
        if issubclass(model, DraftStateMixin) and not issubclass(model, Page)
    ]
    expired_qs = []
    for model in models:
        expired_qs += [model.objects.filter(live=True, expire_at__gt=timezone.now())]
    events = []
    for queryset in expired_qs:
        for obj in queryset:
            events.append(get_expire_event(obj, request.user))
    revisions = Revision.objects.filter(approved_go_live_at__gt=timezone.now())
    for event in revisions:
        events.append(get_publish_event(event, request.user))

    return JsonResponse(events, safe=False)


def get_publish_event(event, user):
    """Return event dict for a scheduled publish revision."""
    model = event.content_object
    return {
        "id": f"{event.id}-start",
        "title": f"{event.object_str} (Go-live)",  # <-- COMBINED TITLE
        "start": event.approved_go_live_at.isoformat(),
        "color": "#008352",
        "extendedProps": {"type": "start"},
        "can_edit": model.permissions_for_user(user).can_publish()
    }


def get_expire_event(event, user):
    """Return event dict for an expiring object (any content type)."""
    revision = event.latest_revision
    return {
        "id": f"{revision.id}-end",
        "title": f"{revision.object_str} (Expire)",  # <-- COMBINED TITLE
        "start": event.expire_at.isoformat(),
        "color": "#cd4444",
        "extendedProps": {"type": "end"},
        "can_edit": event.permissions_for_user(user).can_publish()
    }


def update_page_schedule_date(request):
    """
    Updates go-live and expiry dates for any supported Wagtail object via AJAX.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    go_live_str = data.get("go_live_at")
    expire_str = data.get("expire_at")
    revision_id = data.get("page_id")

    try:
        revision = Revision.objects.get(id=revision_id)
        model = revision.content_object

        if not model.permissions_for_user(request.user).can_publish():
            return JsonResponse({"error": "Permission denied"}, status=403)

        revision.approved_go_live_at = parse_datetime(go_live_str) if go_live_str\
            else None
        revision.save()

        model.expire_at = parse_datetime(expire_str) if expire_str else None
        model.save()


        return JsonResponse({"status": "ok",
                             "message": f"Schedule for '{revision.object_str}' updated."})

    except Revision.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
