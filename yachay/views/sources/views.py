from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from yachay.forms import SourceForm
from yachay.models import Source


class SourceListView(ListView):
    model = Source
    template_name = 'sources/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Source.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes'
        context['create_url'] = reverse_lazy('source_create')
        context['list_url'] = reverse_lazy('source_list')
        context['entity'] = 'Source'
        return context


class SourceCreateView(CreateView):
    model = Source
    form_class = SourceForm
    template_name = 'sources/create.html'
    success_url = reverse_lazy('source_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Fuente'
        context['entity'] = 'Sources'
        context['list_url'] = reverse_lazy('source_list')
        context['action'] = 'add'
        return context

class SourceUpdateView(UpdateView):
    model = Source
    form_class = SourceForm
    template_name = 'sources/create.html'
    success_url = reverse_lazy('source_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(data)
            print(type(data))
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Fuente'
        context['entity'] = 'Source'
        context['list_url'] = reverse_lazy('source_list')
        context['action'] = 'edit'
        return context

class SourceDeleteView(DeleteView):
    model = Source
    template_name = 'sources/delete.html'
    success_url = reverse_lazy('source_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de Fuente'
        context['entity'] = 'Source'
        context['list_url'] = self.success_url
        return context

