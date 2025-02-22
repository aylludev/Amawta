from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from yachay.forms import NoteLinkForm
from yachay.models import NoteLink, Note
from django.views import View
import json

class NoteLinkListView(ListView):
    model = NoteLink
    template_name = 'noteslink/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in NoteLink.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Notas'
        context['create_url'] = reverse_lazy('note_create')
        context['list_url'] = reverse_lazy('note_list')
        context['entity'] = 'Note'
        return context

class NoteLinkCreateView(CreateView):
    model = NoteLink
    form_class = NoteLinkForm
    template_name = 'notes/notelinks.html'
    success_url = reverse_lazy('note_list')

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
        context['title'] = 'Creación una Nota'
        context['entity'] = 'Etiquetas'
        context['list_url'] = reverse_lazy('note_list')
        context['action'] = 'add'
        return context

class NoteUpdateView(UpdateView):
    model = NoteLink
    form_class = NoteLinkForm
    template_name = 'tags/create.html'
    success_url = reverse_lazy('note_list')

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
        context['title'] = 'Edición una Etiqueta'
        context['entity'] = 'Note'
        context['list_url'] = reverse_lazy('note_list')
        context['action'] = 'edit'
        return context

class NoteDeleteView(DeleteView):
    model = NoteLink
    template_name = 'notes/delete.html'
    success_url = reverse_lazy('note_list')

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
        context['title'] = 'Eliminación de Etiqueta'
        context['entity'] = 'Note'
        context['list_url'] = self.success_url
        return context


@csrf_exempt
def add_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            source_id = data.get('source')
            target_id = data.get('target')

            # Verificar que ambas notas existan
            source_note = Note.objects.get(id=source_id)
            target_note = Note.objects.get(id=target_id)

            # Crear el enlace
            NoteLink.objects.create(source=source_note, target=target_note)

            return JsonResponse({'success': True})
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Una de las notas no existe'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@csrf_exempt
def delete_link(request, link_id):
    if request.method == "DELETE":
        try:
            link = NoteLink.objects.get(id=link_id)
            link.delete()
            return JsonResponse({"message": "Relación eliminada"}, status=200)
        except NoteLink.DoesNotExist:
            return JsonResponse({"error": "Relación no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

class AutoNoteLinkView(View):
    def get(self, request, *args, **kwargs):
        data = {}

        # Extraer los parámetros de la URL
        source_id = request.GET.get('source_id')
        target_id = request.GET.get('target_id')
        note_id = request.GET.get('note_id')  # ID de la nueva nota

        if source_id and target_id and note_id:
            try:
                # Crear enlaces en ambas direcciones
                NoteLink.objects.create(source_id=source_id, target_id=note_id)
                NoteLink.objects.create(source_id=note_id, target_id=target_id)

                data['success'] = f"Enlace creado entre {source_id} <-> {note_id} <-> {target_id}"
            except Exception as e:
                data['error'] = str(e)
        else:
            data['error'] = "Faltan parámetros en la URL."

        return JsonResponse(data)
