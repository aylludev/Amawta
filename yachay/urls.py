from django.urls import path
from yachay.views.yachay.views import YachayView
from yachay.views.notes.views import *
from yachay.views.tags.views import *

urlpatterns = [
    path("", YachayView.as_view(), name='index'),
    #tag
    path('tags/list/', TagListView.as_view(), name='tag_list'),
    path('tags/add/', TagCreateView.as_view(), name='tag_create'),
    path('tags/update/<int:pk>/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/delete/<int:pk>/', TagDeleteView.as_view(), name='tag_delete'),
    #tag
    path('notes/list/', NoteListView.as_view(), name='note_list'),
    path('notes/add/', NoteCreateView.as_view(), name='note_create'),
    path('notes/update/<int:pk>/', NoteUpdateView.as_view(), name='note_update'),
    path('notes/delete/<int:pk>/', NoteDeleteView.as_view(), name='note_delete'),
    path('tags/autocomplete/', tag_autocomplete, name='tag_autocomplete'),
]
