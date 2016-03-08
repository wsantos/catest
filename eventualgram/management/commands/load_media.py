"""Fire off tasks to generate ChapterBook covers."""

import urlparse

from django.core.management.base import BaseCommand
from instagram.client import InstagramAPI
import pytz

from eventualgram.constants import INSTAGRAM_CLIENT_ID, MEDIA_TYPE_MAP, TAG
from eventualgram.models import InstagramMedia


class Command(BaseCommand):
    help = 'Deletes existing media and loads all media with the {} tag.'.format(TAG)

    def handle(self, *args, **options):
        """Loads all medias from a given tag.

        Existing media is first cleared from the database, so this is a complete
        refresh.
        """
        InstagramMedia.objects.all().delete()

        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID)
        max_tag_id = None
        finished = False
        utc = pytz.utc

        while not finished:
            media_list, next_url = api.tag_recent_media(
                50, tag_name=TAG, max_tag_id=max_tag_id)

            for media in media_list:
                print 'Creating:', media.id
                media_type = MEDIA_TYPE_MAP[media.type]
                InstagramMedia.objects.create(
                    instagram_id=media.id,
                    media_type=media_type,
                    username=media.user.username,
                    caption=media.caption or '',
                    created_time=utc.localize(media.created_time),
                    url=media.link,
                    low_resolution_url=media.get_low_resolution_url()
                )

            if next_url is None:
                finished = True
            if next_url is not None:
                parsed = urlparse.urlparse(next_url)
                max_tag_id = urlparse.parse_qs(parsed.query)['max_tag_id'][0]
                print '**max_tag_id:', max_tag_id
