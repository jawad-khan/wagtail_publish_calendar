"""
Wagtail admin hooks for wagtail_publish_calendar.
"""

from django.urls import include, path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

# No need for a separate views import if you use the app's urls
from . import urls as calendar_urls


@hooks.register("register_admin_urls")
def register_admin_urls():
    """Register admin URLs for the publish calendar app."""
    return [
        path("publish-calendar/", include(calendar_urls, namespace="wagtail_publish_calendar")),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    """Add Pages Scheduler to the Wagtail admin menu."""
    return MenuItem("Content Scheduler", reverse("wagtail_publish_calendar:calendar"), icon_name="date")
