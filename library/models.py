from django.db import models

import bibtexparser


# Create your models here.

class SimpleItem(models.Model):
    file = models.FileField(null=True, blank=True, upload_to="uploads/")
    tex = models.TextField()
    url = models.CharField(max_length=255, null=True, blank=True)

    def parse_bibtex(self):
        bib_database = bibtexparser.loads(self.tex)
        return bib_database.entries[0]
