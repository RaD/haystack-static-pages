# -*- coding: utf-8 -*-

import os
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
        make_option('-p', '--port', action='store', dest='port', default=None,
            help='The port number to use for internal urls.'),
        make_option('-l', '--language', action='store', dest='language', default=None,
            help='The language to use when requesting the page'),
    )
    help = 'Setup static pages defined in HAYSTACK_STATIC_PAGES for indexing by Haystack'
    cmd = 'crawl_static_pages [-p PORT] [-l LANG]'

    def handle(self, *args, **options):
        if args:
            raise CommandError('Usage is: %s' % self.cmd)

        self.port = options.get('port')

        if self.port:
            if not self.port.isdigit():
                raise CommandError('%r is not a valid port number.' % self.port)
            else:
                self.port = int(self.port)

        count = 0

        self.language = options.get('language')

        if self.language:
            translation.activate(self.language)

        for resource in settings.HAYSTACK_STATIC_PAGES:
            if resource.startswith('/') and os.path.isfile(resource):
                html = open(resource, 'r')
                url = None
                for key in settings.HAYSTACK_STATIC_MAPPING.keys():
                    if resource.startswith(key):
                        tail = resource.split(key + '/')[1]
                        head = settings.HAYSTACK_STATIC_MAPPING[key]
                        url = u'%s/%s' % (head, tail)
            else:
                if resource.startswith('http://'):
                    url = resource
                else:
                    if self.port:
                        url = 'http://%s:%r%s' % (Site.objects.get_current().domain, self.port, reverse(resource))
                    else:
                        url = 'http://%s%s' % (Site.objects.get_current().domain, reverse(resource))

                try:
                    html = urllib2.urlopen(url)
                except urllib2.URLError:
                    print "Error while reading '%s'" % url
                    continue

            print 'Analyzing %s...' % url

            try:
                page = StaticPage.objects.get(url=url)
                print '%s already exists in the index, updating...' % url
            except StaticPage.DoesNotExist:
                print '%s is new, adding...' % url
                page = StaticPage(url=url)
                pass

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

            # save only body without scripts
            body = soup.find('body')
            [x.extract() for x in body.findAll('script')]
            page.content = body.text

            page.language = soup.html.get('lang') or self.language
            page.save()
            count += 1

        print 'Crawled %d static pages' % count
