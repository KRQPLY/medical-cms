from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.forms import modelform_factory


@login_required(login_url="/administration/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/administration/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/administration/login/")
def pages_view(request):
    pages = apps.get_model(app_label="client", model_name="page").objects.all()

    return render(request, 'home/pages.html', {'pages': pages})
    
@login_required(login_url="/administration/login/")
def components_view(request, pk):
    model = apps.get_model(app_label='client', model_name='Page')
    object = get_object_or_404(model, pk=pk)
   
    components = object.get_components()

    return render(request, 'home/components.html', {'components': components})


@login_required(login_url="/administration/login/")
def edit_object(request, model_name, pk):
    model = apps.get_model(app_label='client', model_name=model_name)
    object = get_object_or_404(model, pk=pk)

    modelForm = modelform_factory(model, fields='__all__')

    if request.method == 'POST':
        form = modelForm(request.POST, request.FILES, instance=object)
        if form.is_valid():
            form.save()
            next = request.POST.get('next')

            return HttpResponseRedirect(next) if next else redirect(pages_view)
    else:
        form = modelForm(instance=object)

    return render(request, 'home/edit.html', {'form': form})


@login_required(login_url="/administration/login/")
def add_object(request, model_name):
    model = apps.get_model(app_label='client', model_name=model_name)
    modelForm = modelform_factory(model, fields='__all__')

    if request.method == 'POST':
        form = modelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next = request.POST.get('next')
            
            return HttpResponseRedirect(next) if next else redirect(pages_view)
    else:
        form = modelForm()

    return render(request, 'home/edit.html', {'form': form})


@login_required(login_url="/administration/login/")
def delete_object(request, model_name, pk):
    model = apps.get_model(app_label='client', model_name=model_name)
    object = get_object_or_404(model, pk=pk)
    object.delete()
    next = request.GET.get('next')
            
    return HttpResponseRedirect(next) if next else redirect(pages_view)