import json
from itertools import chain

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from wagtail.models import Page, Revision

from .forms import ScheduleForm


def calendar_view(request):
    """
    Renders the main calendar view and form for the modal.
    """
    form = ScheduleForm()
    context = {"form": form, "page_title": "Page Scheduler"}
    return render(request, "wagtail_publish_calendar/calendar.html", context)


def get_page_schedule_dates(request):
    """
    Creates event data with descriptive titles and color codes.
    """
    expired_pages = Page.objects.filter(live=True, expire_at__gt=timezone.now()).order_by("expire_at")
    revisions = Revision.objects.filter(approved_go_live_at__gt=timezone.now()).order_by("approved_go_live_at")

    events = []
    for event in chain(expired_pages, revisions):
        if getattr(event, "expire_at", None):
            events.append(get_expire_event(event))
        if getattr(event, "approved_go_live_at", None):
            events.append(get_publish_event(event))

    return JsonResponse(events, safe=False)


def get_publish_event(event):
    return {
        "id": f"{event.object_id}-start",
        "title": f"{event.content.get('title')} (Go-live)",  # <-- COMBINED TITLE
        "start": event.approved_go_live_at.isoformat(),
        "color": "#008352",
        "extendedProps": {"type": "start"},
    }


def get_expire_event(event):
    return {
        "id": f"{event.id}-end",
        "title": f"{event.title} (Expire)",  # <-- COMBINED TITLE
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
        page = Page.objects.get(id=data.get("page_id"))

        # A null or empty string from the frontend means the date should be cleared
        go_live_str = data.get("go_live_at")
        expire_str = data.get("expire_at")

        revision = page.latest_revision
        revision.approved_go_live_at = parse_datetime(go_live_str) if go_live_str else None
        revision.save()

        page.expire_at = parse_datetime(expire_str) if expire_str else None
        page.save()

        return JsonResponse({"status": "ok", "message": f"Schedule for '{page.title}' updated."})

    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
