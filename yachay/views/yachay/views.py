
from rest_framework.response import Response
from rest_framework.decorators import api_view
from yachay.models import Note, NoteLink
from yachay.serializers import NoteSerializer

@api_view(['GET'])
def note_graph(request):
    """Devuelve todas las notas en formato de grafo JSON"""
    notes = Note.objects.all()
    nodes = []
    links = []

    for note in notes:
        nodes.append({"id": note.id, "title": note.title})
        for related_note in note.related_notes.all():
            links.append({"source": note.code, "target": related_note.code})

    return Response({"nodes": nodes, "links": links})
