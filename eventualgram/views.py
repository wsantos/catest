from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from eventualgram.constants import MEDIA_PER_PAGE, MEDIA_TYPE_MAP
from eventualgram.models import InstagramMedia


def index(request):
    """Main page. Shows images, filtered as needed.

    Takes three optional GET arguments:
    `username` -> filters the results to those that exactly match the given
                  username.
    `media_type` -> filters the results to those that match the given media type.
    `caption` -> filters the results to those that include the given text in
                 their caption.
    """
    if not InstagramMedia.objects.all().exists():
        return render(request, 'empty.html', {})

    media_list = InstagramMedia.objects.all()

    username = request.GET.get('username', '')
    if username:
        media_list = media_list.filter(username=username)

    try:
        media_type = int(request.GET.get('media_type', None))
    except (ValueError, TypeError):
        media_type = None
    if media_type is not None and media_type in MEDIA_TYPE_MAP.values():
        media_list = media_list.filter(media_type=media_type)

    caption = request.GET.get('caption', None)
    if caption is not None:
        media_list = media_list.filter(caption__icontains=caption)

    paginator = Paginator(media_list, MEDIA_PER_PAGE)
    page_number = request.GET.get('page', 1)
    try:
        media_page = paginator.page(page_number)
    except PageNotAnInteger:
        media_page = paginator.page(1)
    except EmptyPage:
        media_page = paginator.page(paginator.num_pages)

    context = {
        'media_page': media_page,
        'username': username,
        'media_type': media_type,
    }
    return render(request, 'index.html', context)
