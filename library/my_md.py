# Source code for article:
# https://hakibenita.com/django-markdown
import urllib
from typing import Optional
import re
import markdown
from markdown.inlinepatterns import LinkInlineProcessor, LINK_RE, ImageReferenceInlineProcessor, IMAGE_REFERENCE_RE, IMAGE_LINK_RE, ImageInlineProcessor
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.urls import reverse, resolve, Resolver404, NoReverseMatch

from django.conf import settings


class Error(Exception):
    pass


class InvalidMarkdown(Error):

    def __init__(self, error: str, value: Optional[str] = None) -> None:
        self.error = error
        self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return self.error
        return str(self.error)+"::"+ str(self.value)


def clean_link(href: str) -> str:
    if href.startswith('mailto:'):
        email_match = re.match('^(mailto:)?([^?]*)', href)
        if not email_match:
            raise InvalidMarkdown('Invalid mailto link', value=href)

        email = email_match.group(2)
        if email:
            try:
                EmailValidator()(email)
            except ValidationError:
                raise InvalidMarkdown('Invalid email address', value=email)

        return href

    # Remove fragments or query params before trying to match the url name


    z = href.split("|")
    href = z[0]
    args = []

    for part in z:
        if part != href:
            prt = urllib.parse.urlencode({'q':part})
            args.append(prt)
    href_parts = re.search(r'#|\?', href)
    if href_parts:
        start_ix = href_parts.start()
        url_name, url_extra = href[:start_ix], href[start_ix:]
    else:
        url_name, url_extra = href, ''

    try:
        print(args)
        url = reverse(url_name, args=args)
        print(url)
    except NoReverseMatch:
        print(url_name)
        pass
    else:
        print(url)

        return url + url_extra

    print(href)
    return href


class DjangoLinkInlineProcessor(LinkInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        href = clean_link(href)
        return href, title, index, handled


class CustomImageLinkProcessor(ImageInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        print(href, title, index)
        href = clean_link(href)
        return href, title, index, handled


class DjangoUrlExtension(markdown.Extension):
    def extendMarkdown(self, md, *args, **kwrags):
        md.inlinePatterns.register(DjangoLinkInlineProcessor(LINK_RE, md), 'link', 160)
        md.inlinePatterns.register(CustomImageLinkProcessor(IMAGE_LINK_RE, md), 'image_link', 140)


def render_md(markdown_text: str):
    md = markdown.Markdown(extensions=[DjangoUrlExtension(), 'tables'])
    return md.convert(markdown_text)