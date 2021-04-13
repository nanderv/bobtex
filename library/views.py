import urllib

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_tables2 import RequestConfig, LazyPaginator

from library.models import Item, ItemTable, Tag

from django import forms

from library.my_md import render_md


class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['url'].required = False

    class Meta:
        model = Item
        fields = ['tex', 'summary', 'file', 'tags', 'url']


@permission_required('library.view_item')
def show_all(request):
    special = ""
    form = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        doi = request.POST["tex"]
        if form.is_valid():
            form.save()
            special = "Succesful upload!"
    else:
        form = UploadFileForm()
    t = Item.objects.filter(project=request.user.default_project)
    if request.GET.get('tag'):
        t = t.filter(tags__name=request.GET.get('tag'))
    if request.GET.get('order'):
        t = t.order_by(request.GET['order'])
        if request.GET.get('reversed'):
            t = t.reverse()

    return render(request, 'main_page.html', {"data": t, "form": form, "special": special})


@permission_required('library.delete_item')
def delete_maybe(request, id):
    return render(request, 'delete_maybe.html', {"id": id})


@permission_required('library.delete_item')
def delete(request, id):
    Item.objects.filter(pk=id).delete()
    return show_all(request)


@permission_required('library.view_item')
def full_tex(request):
    tex = ""
    for item in Item.objects.all():
        tex = tex + "\n\n" + item.tex

    return HttpResponse(tex, content_type="text")


@permission_required('library.change_item')
def form_edit(request, id):
    special = ""
    my_summary = ""

    obj = Item.objects.get(pk=id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, instance=obj)

        doi = request.POST["tex"]
        if form.is_valid():
            instance = form.save()
            my_summary = instance.summary
            special = "Succesful upload!"
            obj = Item.objects.get(pk=id)
            form = UploadFileForm(instance=obj)
    else:
        obj = Item.objects.get(pk=id)
        form = UploadFileForm(instance=obj)
    rendered = render_md(my_summary)
    return render(request, 'form.html', {"form": form, "special": special, 'rendered': rendered})


@permission_required('library.change_item')
def form_edit2(request, id):
    sstr = urllib.parse.parse_qs(id)['q'][0]
    print(sstr)
    obj = Item.objects.get(doc_ID=sstr)
    return form_edit(request, id=obj.pk)


@permission_required('library.add_item')
def form_new(request):
    special = ""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        doi = request.POST["tex"]
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = request.user.default_project
            instance.save()
            for z in request.POST['tags']:
                print(z)
                instance.tags.add(Tag.objects.get(pk=z))


            instance.save()
            special = "Succesful upload!"
            form = UploadFileForm()
            my_summary = instance.summary
    else:
        form = UploadFileForm()
    rendered = ""
    return render(request, 'form.html', {"form": form, "special": special, 'rendered': rendered})
