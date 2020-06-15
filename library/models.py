from django.db import models

import bibtexparser

# Create your models here.
import django_tables2 as tables
from django.utils.html import format_html


class SimpleItem(models.Model):
    file = models.FileField(null=True, blank=True, upload_to="uploads/")
    tex = models.TextField()
    url = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    doc_ID = models.CharField(max_length=255)
    year = models.IntegerField()

    def save(self, *args, **kwargs):
        self.title = self.my_title
        self.authors = self.my_authors
        self.doc_ID = self.my_ID
        self.year = self.my_year
        super().save(*args, **kwargs)

    def parse_bibtex(self):
        bib_database = bibtexparser.loads(self.tex)
        return bib_database.entries[0]

    @property
    def my_authors(self):
        return self.parse_bibtex()["author"]

    @property
    def my_year(self):
        return self.parse_bibtex()["year"]

    @property
    def my_title(self):
        return self.parse_bibtex()["title"]

    @property
    def my_ID(self):
        return self.parse_bibtex()["ID"]


class SimpleItemTable(tables.Table):
    authors = tables.Column(empty_values=())
    title = tables.Column(empty_values=())
    year = tables.Column(empty_values=())
    doc_ID = tables.Column(verbose_name="ID")
    options = tables.Column(empty_values=(), orderable=False)

    def render_options(self, record):
        if record.file:
            return format_html(
                '<a href="/lib/{}"><i class="fa fa-download"></i></a><a href="/lib/edit/{}"><i class="fa fa-edit"></i></a><a href="/lib/delete-maybe/{}"><i class="fa fa-trash"></a></a>', record.file,
                record.pk, record.pk)
        if record.url:
            return format_html('<a href="{}"><i class="fa fa-plane"></i></a><a href="/lib/edit/{}"><i class="fa fa-edit"></i></a><a href="/lib/delete-maybe/{}"><i class="fa fa-trash"></a>',
                               record.url, record.pk, record.pk)
        return format_html('<a href="/lib/edit/{}">  <i class="fa fa-edit"></i></a><a href="/lib/delete-maybe/{}"><i class="fa fa-trash"></a></a>', record.pk, record.pk)

