from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from yachay.forms import LineForm
from yachay.models import Line


class LineListView(ListView):
    model = Line
    template_name = 'lines/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Line.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Lineas'
        context['create_url'] = reverse_lazy('line_create')
        context['list_url'] = reverse_lazy('line_list')
        context['entity'] = 'Line'
        return context


class LineCreateView(CreateView):
    model = Line
    form_class = LineForm
    template_name = 'lines/create.html'
    success_url = reverse_lazy('line_list')

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
        context['title'] = 'Creación una Linea'
        context['entity'] = 'Lineas'
        context['list_url'] = reverse_lazy('line_list')
        context['action'] = 'add'
        return context

class LineUpdateView(UpdateView):
    model = Line
    form_class = LineForm
    template_name = 'lines/create.html'
    success_url = reverse_lazy('line_list')

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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Linea'
        context['entity'] = 'Line'
        context['list_url'] = reverse_lazy('line_list')
        context['action'] = 'edit'
        return context

class LineDeleteView(DeleteView):
    model = Line
    template_name = 'lines/delete.html'
    success_url = reverse_lazy('line_list')

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
        context['title'] = 'Eliminación de Linea'
        context['entity'] = 'Line'
        context['list_url'] = self.success_url
        return context

