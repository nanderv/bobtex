from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_tables2 import RequestConfig, LazyPaginator

from library.models import SimpleItem, SimpleItemTable

from django import forms


class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['url'].required = False

    class Meta:
        model = SimpleItem
        fields = ['tex', 'file', 'url']


@permission_required('library.view_simpleitem')
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

    table = SimpleItemTable(SimpleItem.objects.all())
    RequestConfig(request, paginate=False).configure(table)
    return render(request, 'main_page.html', {"table": table, "data": SimpleItem.objects.all(), "form": form, "special": special})


@permission_required('library.delete_simpleitem')
def delete_maybe(request, id):
    return render(request, 'delete_maybe.html', {"id": id})


@permission_required('library.delete_simpleitem')
def delete(request, id):
    SimpleItem.objects.filter(pk=id).delete()
    return show_all(request)


@permission_required('library.view_simpleitem')
def full_tex(request):
    tex = ""
    for item in SimpleItem.objects.all():
        tex = tex + "\n\n" + item.tex

    return HttpResponse(tex, content_type="text")


@permission_required('library.change_simpleitem')
def form_edit(request, id):
    special = ""

    obj = SimpleItem.objects.get(pk=id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, instance=obj)
        doi = request.POST["tex"]
        if form.is_valid():
            form.save()
            special = "Succesful upload!"
            obj = SimpleItem.objects.get(pk=id)
            form = UploadFileForm(instance=obj)
    else:
        obj = SimpleItem.objects.get(pk=id)
        form = UploadFileForm(instance=obj)

    return render(request, 'form.html', {"form": form, "special": special})


@permission_required('library.add_simpleitem')
def form_new(request):
    special = ""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        doi = request.POST["tex"]
        if form.is_valid():
            form.save()
            special = "Succesful upload!"
            form = UploadFileForm()
    else:
        form = UploadFileForm()

    return render(request, 'form.html', {"form": form, "special": special})
