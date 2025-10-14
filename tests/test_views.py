import datetime
import logging
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.utils import timezone

from wagtail_publish_calendar import views
from .utils import PageTestMixin

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_calendar_view_renders_template():
    factory = RequestFactory()
    request = factory.get("/admin/publish-calendar/")
    User = get_user_model()
    request.user = User.objects.create_user(username="testuser", password="testpass")
    response = views.calendar_view(request)
    assert response.status_code == 200
    assert "Page Scheduler" in response.content.decode()


@pytest.mark.django_db
class TestGetPageScheduleDates(PageTestMixin):

    def test_get_page_schedule_dates(self):
        factory = RequestFactory()
        request = factory.get("/admin/publish-calendar/get-page-schedule-dates/")
        live_data = timezone.now() + datetime.timedelta(days=5)
        expiry_date =  timezone.now() + datetime.timedelta(days=15)
        self.page.save_revision(approved_go_live_at=live_data)
        self.page.expire_at =expiry_date
        self.page.save()
        response = views.get_page_schedule_dates(request)
        assert response.status_code == 200
        import json

        data = json.loads(response.content)
        assert isinstance(data, list)
        assert data[1]["title"] == "{} (Go-live)".format(self.page.title)
        assert data[0]["title"] == "{} (Expire)".format(self.page.title)
        assert data[0]["start"] == expiry_date.isoformat()
        assert data[1]["start"] == live_data.isoformat()
        assert data[0]["id"] == "{}-end".format(self.page.id)
        assert data[1]["id"] == "{}-start".format(self.page.id)

@pytest.mark.django_db
@mock.patch("wagtail_publish_calendar.views.Page")
def test_update_page_schedual_date_success(mock_page):
    factory = RequestFactory()
    request = factory.post(
        "/admin/publish-calendar/update-page-schedual-date/",
        content_type="application/json",
        data=b'{"page_id": 1, "go_live_at": "2025-09-22T10:00:00", "expire_at": "2025-09-23T10:00:00"}',
    )
    page = mock.Mock()
    page.title = "Test Page"
    mock_page.objects.get.return_value = page
    response = views.update_page_schedule_date(request)
    import json

    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["status"] == "ok"


@pytest.mark.django_db
def test_update_page_schedual_date_invalid_method():
    factory = RequestFactory()
    request = factory.get("/admin/publish-calendar/update-page-schedual-date/")
    response = views.update_page_schedule_date(request)
    assert response.status_code == 405
