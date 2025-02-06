from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from yachay.forms import AuthorForm
from yachay.models import Author

class AuthorListView(ListView):
    model = Author
    template_name = 'author/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Author.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Autores'
        context['create_url'] = reverse_lazy('author_create')
        context['list_url'] = reverse_lazy('author_list')
        context['entity'] = 'Author'
        return context


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author/create.html'
    success_url = reverse_lazy('author_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                print(form)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Autor'
        context['entity'] = 'Author'
        context['list_url'] = reverse_lazy('author_list')
        context['action'] = 'add'
        return context

class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author/create.html'
    success_url = reverse_lazy('author_list')

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
        context['title'] = 'Edición un Autor'
        context['entity'] = 'Author'
        context['list_url'] = reverse_lazy('author_list')
        context['action'] = 'edit'
        return context


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author/delete.html'
    success_url = reverse_lazy('author_list')

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
        context['title'] = 'Eliminación de un Autor'
        context['entity'] = 'Author'
        context['list_url'] = self.success_url
        return context
