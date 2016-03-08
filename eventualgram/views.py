from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from eventualgram.constants import IMAGES_PER_PAGE
from eventualgram.models import InstagramMedia


def index(request):
    image_list = InstagramMedia.objects.all()
    if not image_list.exists():
        return render(request, 'empty.html', {})

    paginator = Paginator(image_list, IMAGES_PER_PAGE)

    page_number = request.GET.get('page', 1)
    try:
        images = paginator.page(page_number)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    context = {
        'images': images,
    }
    return render(request, 'index.html', context)
