from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'items'

urlpatterns = [
    path('item/', ItemView.as_view(), name='item-all'),
    path('item/fix/', ItemFixView.as_view(), name='item-fix-each'),
    path('item/<int:id>/', ItemEachView.as_view(), name='item-get-each'),
    path('item/<int:id>/delete/', ItemEachView.as_view(), name='item-delete-each'),
]
