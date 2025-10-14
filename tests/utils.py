from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page, Site


class PageTestMixin(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        home = Page(title="Home")
        root.add_child(instance=home)
        cls.page = Page(
            title="My Page",
            slug="mypage",
        )
        home.add_child(instance=cls.page)
