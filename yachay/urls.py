from django.urls import path
from yachay.views.tags.views import *

urlpatterns = [
    path('tags/list/', TagListView.as_view(), name='tag_list'),
    path('tags/add/', TagCreateView.as_view(), name='tag_create'),
    path('tags/update/<int:pk>/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/delete/<int:pk>/', TagDeleteView.as_view(), name='tag_create_delete'),
]
