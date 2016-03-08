from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from eventualgram.constants import MEDIA_PER_PAGE
from eventualgram.models import InstagramMedia


def index(request):
    if not InstagramMedia.objects.all().exists():
        return render(request, 'empty.html', {})

    media_list = InstagramMedia.objects.all()

    username = request.GET.get('username', None)
    if username is not None:
        media_list = media_list.filter(username=username)

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
    }
    return render(request, 'index.html', context)
