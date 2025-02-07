from django.urls import path
from yachay.views.notes.views import *
from yachay.views.tags.views import *
from yachay.views.author.views import *
from yachay.views.yachay.views import *
from yachay.views.sources.views import *
from yachay.views.links.views import *

urlpatterns = [
    #tag
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/add/', TagCreateView.as_view(), name='tag_create'),
    path('tags/update/<int:pk>/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/delete/<int:pk>/', TagDeleteView.as_view(), name='tag_delete'),
    #Source
    path('sources/', SourceListView.as_view(), name='source_list'),
    path('sources/add/', SourceCreateView.as_view(), name='source_create'),
    path('sources/update/<int:pk>/', SourceUpdateView.as_view(), name='source_update'),
    path('sources/delete/<int:pk>/', SourceDeleteView.as_view(), name='source_delete'),
    #note
    path('notes/', NoteListView.as_view(), name='note_list'),
    path('notes/add/', NoteCreateView.as_view(), name='note_create'),
    path('notes/add/<int:source_id>/<int:target_id>/', NoteCreateView.as_view(), name='note_create'),
    path('notes/update/<int:pk>/', NoteUpdateView.as_view(), name='note_update'),
    path('notes/delete/<int:pk>/', NoteDeleteView.as_view(), name='note_delete'),
    #tag
    path('author/', AuthorListView.as_view(), name='author_list'),
    path('author/add/', AuthorCreateView.as_view(), name='author_create'),
    path('author/update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),
    path('author/delete/<int:pk>/', AuthorDeleteView.as_view(), name='author_delete'),
    #notelink
    path('links/add/', add_link, name='notelink_create'),
    #grap
    path('', graph_view, name='graph'),
    path('graph_data/', graph_data, name='graph_data')
]
