from django.shortcuts import render
from django.http import JsonResponse
from yachay.models import Note, NoteLink

def graph_view(request):
    return render(request, "yachay/graph.html")

def graph_data(request):
    nodes = [
        {
            "id": str(note.id),  # Convertimos a string para Cytoscape.js
            "title": note.title,
            "content": note.content,
            "source": note.source.title if note.source else "Desconocido",  # Evitamos None
            "tags": [tag.name for tag in note.tags.all()]  # Convertimos los tags a una lista
        }
        for note in Note.objects.all()
    ]

    links = [
        {
            "id": link.id,
            "source": str(link.source.id),
            "target": str(link.target.id),
            "relationship": "Enlace"  # Puedes modificarlo para relaciones específicas
        }
        for link in NoteLink.objects.all()
    ]

    return JsonResponse({"nodes": nodes, "links": links})
