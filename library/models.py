from django.db import models

import bibtexparser

# Create your models here.
import django_tables2 as tables
from django.utils.html import format_html


class SimpleItem(models.Model):
    file = models.FileField(null=True, blank=True, upload_to="uploads/")
    tex = models.TextField()
    url = models.CharField(max_length=255, null=True, blank=True)

    def parse_bibtex(self):
        bib_database = bibtexparser.loads(self.tex)
        return bib_database.entries[0]

    @property
    def authors(self):
        return self.parse_bibtex()["author"]

    @property
    def year(self):
        return self.parse_bibtex()["year"]

    @property
    def title(self):
        return self.parse_bibtex()["title"]

    @property
    def ID(self):
        return self.parse_bibtex()["ID"]


class SimpleItemTable(tables.Table):
    authors = tables.Column(empty_values=())
    title = tables.Column(empty_values=())
    year = tables.Column(empty_values=())
    ID = tables.Column()
    options = tables.Column(empty_values=(), orderable=False)

    def order_title(self, queryset, is_descending):
        return sorted(queryset, key=lambda q: q.title.replace("{", ""), reverse=is_descending), True

    def order_year(self, queryset, is_descending):
        return sorted(queryset, key=lambda q: q.year, reverse=is_descending), True

    def order_authors(self, queryset, is_descending):
        return sorted(queryset, key=lambda q: q.authors.replace("{", ""), reverse=is_descending), True

    def order_ID(self, queryset, is_descending):
        return sorted(queryset, key=lambda q: q.ID, reverse=is_descending), True

    def render_options(self, record):
        print(record)
        if record.file:
            return format_html('<a><a href="/lib/{}">download</a><a href="/lib/delete-maybe/{}">Delete</a>', record.file, record.pk)
        if record.url:
                return format_html('<a><a href="{}">goto</a><a href="/lib/delete-maybe/{}">Delete</a>', record.url, record.pk)