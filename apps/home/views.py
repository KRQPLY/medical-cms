from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.forms import modelform_factory
from django.contrib.auth.models import User
from client.models import Page
from django.contrib import messages
from . import forms

def get_form_class(model):
    try:
        return getattr(forms, model.__name__ + 'Form')
    except (ImportError, AttributeError):
        pass
    
    parent_model = model.__bases__[0] if model.__bases__ else None
    if parent_model:
        try:
            return getattr(forms, parent_model.__name__ + 'Form')
        except (ImportError, AttributeError):
            pass

    return None


@login_required(login_url="/administration/login/")
def index(request):
    return redirect("/administration/profile.html")


@login_required(login_url="/administration/login/")
def pages(request):
    context = {}

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
    Page = apps.get_model(app_label="client", model_name="page")
    root_pages = Page.objects.filter(parent=None)
    return render(request, 'home/pages.html', {'root_pages': root_pages})
    
@login_required(login_url="/administration/login/")
def components_view(request, pk):
    model = apps.get_model(app_label='client', model_name='page')
    object = get_object_or_404(model, pk=pk)
   
    components = object.get_components()

    return render(request, 'home/components.html', {'components': components})

@login_required(login_url="/administration/login/")
def common_components_view(request):
    Header = apps.get_model(app_label='client', model_name='header')
    Footer = apps.get_model(app_label='client', model_name='footer')

    header, _ = Header.objects.get_or_create(name='Header')
    footer, _ = Footer.objects.get_or_create(name='Footer')

    return render(request, 'home/common-components.html', {'components': [header, footer]})


@login_required(login_url="/administration/login/")
def components_all_view(request):
    models_list = apps.get_app_config('client').get_models()

    unique_components = set()

    for model in models_list:
        if hasattr(model, 'isComponent'):
            unique_components.add(model.__name__)

    sorted_components = sorted(unique_components)

    return render(request, 'home/components-all.html', {'components': sorted_components})

@login_required(login_url="/administration/login/")
def components_browse_view(request, model_name):
    models_list = apps.get_app_config('client').get_models()

    filtered_models = [model for model in models_list if hasattr(model, 'isComponent')]

    components = []

    for model in filtered_models:
        if model.__name__ == model_name:
            components += model.objects.all()

    return render(request, 'home/components.html', {'components': components})


@login_required(login_url="/administration/login/")
def edit_object(request, model_name, pk):
    excluded_fields = ['created_by', 'modified_by']
    
    model = apps.get_model(app_label='client', model_name=model_name)
    object = get_object_or_404(model, pk=pk)

    modelForm = modelform_factory(model, fields='__all__', exclude=excluded_fields)

    form_class = get_form_class(model)

    if form_class is not None:
        modelForm = modelform_factory(model, form=form_class, exclude=excluded_fields)

    if request.method == 'POST':
        form = modelForm(request.POST, request.FILES, instance=object)
        if form.is_valid():
            uid = User.objects.get(username=request.user.username)
            form.instance.modified_by = uid
            form.save()

            next = request.POST.get('next')

            return HttpResponseRedirect(next) if next else redirect(pages_view)
        else:
            messages.error(request, f'Form is not valid. Errors: {form.errors}')
    else:
        form = modelForm(instance=object)

    return render(request, 'home/edit.html', {'form': form})


@login_required(login_url="/administration/login/")
def add_object(request, model_name):
    excluded_fields = ['created_by', 'modified_by']

    model = apps.get_model(app_label='client', model_name=model_name)
    
    modelForm = modelform_factory(model, fields='__all__', exclude=excluded_fields)

    initial_data = {}

    form_class = get_form_class(model)

    if form_class is not None:
        modelForm = modelform_factory(model, form=form_class, exclude=excluded_fields)

    if model_name == 'page' and 'parent' in request.GET:
        try:
            parent_page = Page.objects.get(pk=request.GET['parent'])
            initial_data = {'parent': parent_page}
        except Page.DoesNotExist:
            initial_data = {}
    else:
        initial_data = {}

    if request.method == 'POST':
        form = modelForm(request.POST, request.FILES)

        if form.is_valid():
            uid = User.objects.get(username=request.user.username)
            form.instance.created_by = uid
            form.instance.modified_by = uid
            form.save()

            next = request.POST.get('next')

            return HttpResponseRedirect(next) if next else redirect(pages_view)
        else:
            messages.error(request, f'Form is not valid. Errors: {form.errors}')
    else:
        form = modelForm(initial=initial_data)

    return render(request, 'home/edit.html', {'form': form})


@login_required(login_url="/administration/login/")
def delete_object(request, model_name, pk):
    model = apps.get_model(app_label='client', model_name=model_name)
    object = get_object_or_404(model, pk=pk)
    object.delete()
    next = request.GET.get('next')
            
    return HttpResponseRedirect(next) if next else redirect(pages_view)

@login_required(login_url="/administration/login/")
def copy_object(request, model_name, object_id):
    model = apps.get_model(app_label='client', model_name=model_name)

    original_object = get_object_or_404(model, pk=object_id)

    new_object = model()
    for field in original_object._meta.fields:
        if field.name not in ['id', 'created_by', 'modified_by']:
            setattr(new_object, field.name, getattr(original_object, field.name))

    uid = User.objects.get(username=request.user.username)
    new_object.created_by = uid
    new_object.modified_by = uid

    new_object.save()

    next = request.GET.get('next')
    return HttpResponseRedirect(next) if next else redirect(pages_view)