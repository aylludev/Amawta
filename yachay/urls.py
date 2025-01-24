from django.urls import path
from yachay.views.tags.views import *

urlpatterns = [
    path('tags/list/', TagListView.as_view(), name='category_list'),
    path('tags/add/', TagCreateView.as_view(), name='category_create'),
    path('tags/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('tags/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
]
