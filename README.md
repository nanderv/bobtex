# bobtex
BobTex is a simple system for managing bibtex references, and their linked files / urls. The name is work in progress.

## How to install
BobTex is a plain python project based on Django, as well as a library for Bibtex parsing, and Django-Tables. 

Therefore, the installation should go something like the following:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

The server can be run from the develop mode. 

Mind you, the secret key is shared across the internet right now, so you may want to replace that one.

## How to use
BobTex is a tool to collect bibtex references, and link them to pdf files. After logging in, you can add new items by pressing 'new item'.

Then put the bibtex there, and upload a file. If the bibtex is valid enough, a row will be added to the table. If it isn't valid, it will crash in flames.

Entries can also be edited, downloaded and deleted from the table.

By pressing the Download Bibtex button you get a text page that contains the whole bibtex for your BobTex session. 
This simply concatenates all your entries in the table underneath each other. This guarantees that the BibTex will be exactly how you put it in there (tm).

BobTex has some revolutionary features:
1. A you-know-best mentality: it will not try to fix any issues with your BibTex
2. Storing your PDF's and links with your bibtex sources
3. Being totally free and hackable
4. Being cobbled together in under a week of part-time development

## Design considerations
BobTex is designed with local use in mind; the idea is that an instance is created for one small group (ie. a small group within a faculty, or a single person). Therefore, things like user privacy were not taken into account when designing BobTex. Also, features such as password reset were not seen as important, because it's assumed that the user either *is* the administrator, or knows the administrator personally.
