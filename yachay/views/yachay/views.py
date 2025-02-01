
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from yachay.models import Note, NoteLink
from django.shortcuts import render

# Create your views here.
class YachayView(TemplateView):
    template_name = 'yachay.html'

@api_view(['GET'])
def note_graph(request):
    notes = Note.objects.all()
    nodes = []
    links = []

    for note in notes:
        nodes.append({"id": note.id, "title": note.title})

        for prev_note in NoteLink.objects.all():
            links.append({"source": prev_note.source.id, "target": prev_note.target.id})

    return Response({"nodes": nodes, "links": links})


def graph_view(request):
    return render(request, 'graph.html')
