from django.shortcuts import render
from django.http import JsonResponse
from yachay.models import Note, NoteLink

def graph_view(request):
    return render(request, "yachay/graph.html")

def graph_data(request):
    nodes = [{"id": note.id, "title": note.title} for note in Note.objects.all()]
    links = [{"source": link.source.id, "target": link.target.id} for link in NoteLink.objects.all()]
    return JsonResponse({"nodes": nodes, "links": links})
