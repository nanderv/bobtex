from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm
from django.shortcuts import render, redirect

# Create your views here.
from library.models import Item
from projects.models import UserToProject, Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']


@permission_required('projects.view_project')
def show_all(request):
    projs = UserToProject.objects.filter(user=request.user)
    projects = Project.objects.filter(usertoproject__in=projs)
    return render(request, 'projects.html', {"data": projects, "dcount": Item.objects.filter(project=None)})


@permission_required('projects.change_project')
def set_default(request, id):
    if id == "None":
        request.user.default_project = None
    else:
        request.user.default_project = Project.objects.get(pk=id)
    request.user.save()
    return show_all(request)


@permission_required('projects.add_project')
def new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print(instance)
            UserToProject.objects.create(user=request.user, project=instance, is_owner=True, can_edit=True)
            return redirect('/projects')
    else:
        form = ProjectForm()

    return render(request, 'project_new.html', {"form": form})
