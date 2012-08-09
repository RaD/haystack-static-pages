# -*- coding: utf-8 -*-

import urllib2

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.html import escape
from optparse import make_option

from BeautifulSoup import BeautifulSoup

from haystack_static_pages.models import StaticPage


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-l', '--language', action='store', dest='language', default=None,
            help='The language to use when requesting the page'),
    )
    help = 'Setup static pages defined in HAYSTACK_STATIC_PAGES for indexing by Haystack'
    cmd = 'local_static_pages [-l LANG]'

    def handle(self, *args, **options):
        if args:
            raise CommandError('Usage is: %s' % self.cmd)

        count = 0

        self.language = options.get('language')

        if self.language:
            translation.activate(self.language)

        for item in settings.HAYSTACK_STATIC_PAGES:
            print 'Analyzing %s...' % item

            try:
                page = StaticPage.objects.get(url=item)
                print '%s already exists in the index, updating...' % item
            except StaticPage.DoesNotExist:
                print '%s is new, adding...' % item
                page = StaticPage(url=item)
                pass

            html = open(item)

            soup = BeautifulSoup(html)
            try:
                page.title = escape(soup.head.title.string)
            except AttributeError:
                page.title = 'Untitled'
            meta = soup.find('meta', attrs={'name': 'description'})
            if meta:
                page.description = meta.get('content', '')
            else:
                page.description = ''
            page.language = soup.html.get('lang') or self.language
            page.content = soup.prettify()
            page.save()
            count += 1

        print 'Loaded %d static pages' % count
