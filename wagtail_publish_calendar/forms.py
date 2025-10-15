"""
Forms for wagtail_publish_calendar.
"""

from django import forms
from wagtail.admin.widgets import AdminDateTimeInput


class ScheduleForm(forms.Form):
    go_live_at = forms.DateTimeField(
        required=False,
        widget=AdminDateTimeInput(attrs={"id": "start-datetime"}),
        label="Go live date/time",
        help_text="Optional. When the page should go live.",
    )

    expiry_at = forms.DateTimeField(
        required=False,
        widget=AdminDateTimeInput(attrs={"id": "end-datetime"}),
        label="Expiry date/time",
        help_text="Optional. When the page should expire.",
    )
