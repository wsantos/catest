from __future__ import unicode_literals

from django.db import models

from eventualgram.constants import MEDIA_TYPE_CHOICES


class InstagramMedia(models.Model):
    instagram_id = models.CharField(max_length=50)
    media_type = models.PositiveSmallIntegerField(choices=MEDIA_TYPE_CHOICES)
    username = models.CharField(max_length=50)
    caption = models.TextField()
    created_time = models.DateTimeField(null=True)
    url = models.URLField()
    low_resolution_url = models.URLField()

    class Meta:
        ordering = ('-created_time',)
