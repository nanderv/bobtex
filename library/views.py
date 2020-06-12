
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from library.models import SimpleItem

from django import forms


class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['url'].required = False
    class Meta:
        model = SimpleItem
        fields=['tex','file', 'url']


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
    return render(request, 'main_page.html', {"data": SimpleItem.objects.all(), "form": form, "special":special})


def delete_maybe(request, id):
    return render(request, 'delete_maybe.html', {"id":id})


def delete(request, id):
    SimpleItem.objects.filter(pk=id).delete()
    return show_all(request)



def full_tex(request):
    tex = ""
    for item in SimpleItem.objects.all():
        tex = tex+"\n\n"+item.tex

    return HttpResponse(tex, content_type="text")