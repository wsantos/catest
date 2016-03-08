from django.http import HttpRequest, QueryDict
from django.test import TestCase
import mock

from eventualgram import views
from eventualgram.constants import IMAGE
from eventualgram.models import InstagramMedia


class TestViews(TestCase):
    """Tests for eventualgram.views."""

    @mock.patch('eventualgram.views.render')
    def test_empty(self, render):
        """If no media is loaded, the empty template is used."""
        request = HttpRequest()

        views.index(request)

        self.assertEqual(render.call_count, 1)
        _, template, _ = render.call_args[0]
        self.assertEqual(template, 'empty.html')

    @mock.patch('eventualgram.views.render')
    def test_not_empty(self, render):
        """If media is loaded, the index template is used."""
        InstagramMedia.objects.create(media_type=IMAGE)
        request = HttpRequest()

        views.index(request)

        self.assertEqual(render.call_count, 1)
        _, template, _ = render.call_args[0]
        self.assertEqual(template, 'index.html')

    @mock.patch('eventualgram.views.render')
    def test_no_page(self, render):
        """If no page is specified, the first page is rendered."""
        InstagramMedia.objects.create(media_type=IMAGE)
        request = HttpRequest()

        views.index(request)

        self.assertEqual(render.call_count, 1)
        _, _, context = render.call_args[0]
        self.assertEqual(context['images'].number, 1)

    @mock.patch('eventualgram.views.render')
    def test_non_integer_page_number(self, render):
        """If a non-integer page is specified, the first page is rendered."""
        InstagramMedia.objects.create(media_type=IMAGE)
        request = HttpRequest()
        request.GET = QueryDict('page=eleventeen')

        views.index(request)

        self.assertEqual(render.call_count, 1)
        _, _, context = render.call_args[0]
        self.assertEqual(context['images'].number, 1)

    @mock.patch('eventualgram.views.render')
    def test_page_number_too_large(self, render):
        """If the page number goes past the last image, the last page is rendered."""
        while InstagramMedia.objects.count() <= views.IMAGES_PER_PAGE:
            InstagramMedia.objects.create(media_type=IMAGE)
        request = HttpRequest()
        request.GET = QueryDict('page=9999')

        views.index(request)

        self.assertEqual(render.call_count, 1)
        _, _, context = render.call_args[0]
        self.assertEqual(context['images'].number, 2)

    @mock.patch('eventualgram.views.render')
    def test_valid_page_number(self, render):
        """If valid page number is specified, that page is rendered."""
        while InstagramMedia.objects.count() <= views.IMAGES_PER_PAGE:
            InstagramMedia.objects.create(media_type=IMAGE)
        request = HttpRequest()
        request.GET = QueryDict('page=2')

        views.index(request)

        self.assertEqual(render.call_count, 1)
        _, _, context = render.call_args[0]
        self.assertEqual(context['images'].number, 2)


class TestLoadMedia(TestCase):
    """Tests for the load_media command."""

