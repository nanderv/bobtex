from django.db import models

import bibtexparser

# Create your models here.
import django_tables2 as tables
from django.db.models import CASCADE, SET_NULL
from django.utils.html import format_html

from library.my_md import render_md
from projects.models import Project


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, default='red')
    def __str__(self):
        return self.name

class Item(models.Model):
    file = models.FileField(null=True, blank=True, upload_to="uploads/")
    tex = models.TextField()
    url = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    doc_ID = models.CharField(max_length=255)
    year = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=CASCADE, null=True)
    summary = models.TextField(default="")
    tags = models.ManyToManyField(Tag, blank=True, null=True)
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
        return self.parse_bibtex()["author"][0:40]

    @property
    def my_year(self):
        return self.parse_bibtex()["year"]

    @property
    def my_title(self):
        return self.parse_bibtex()["title"]

    @property
    def my_ID(self):
        return self.parse_bibtex()["ID"]

    def render_authors(record):
        return format_html("<p  data-toggle='tooltip data-placement='top' title='{}'>{}</b>", record.authors, record.authors[0:40])

    def render_item_options(record):
        if record.file:
            return format_html('<a href="/lib/{}"><i class="fa fa-lg fa-download"></i></a>' +
                '<a href="/lib/edit/{}"><i class="fa fa-lg fa-edit"></i></a>' +
                '<a href="/lib/delete-maybe/{}"><i class="fa fa-lg fa-trash"></a></a>', record.file, record.pk, record.pk)
        if record.url:
            return format_html('<a href="{}"><i class="fa  fa-lg fa-plane"></i></a><a href="/lib/edit/{}">' +
                '<i class="fa  fa-lg fa-edit"></i></a><a href="/lib/delete-maybe/{}">' +
                '<i class="fa fa-lg fa-trash"></a>',
                record.url, record.pk, record.pk)
        return format_html('<a href="/lib/edit/{}">  <i class="fa  fa-lg fa-edit"></i></a><a href="/lib/delete-maybe/{}"><i class="fa  fa-lg fa-trash"></a></a>', record.pk, record.pk)

    def render_summary(self):
        return render_md(self.summary)
class ItemTable(tables.Table):
    authors = tables.Column(empty_values=() )
    title = tables.Column(empty_values=())
    year = tables.Column(empty_values=())
    doc_ID = tables.Column(verbose_name="ID")
    options = tables.Column(empty_values=(), orderable=False)

    def render_authors(self, value, record):
        return record.render_authors()

    def render_options(self, record):
        return record.render_item_options()


