from django.contrib import admin
from items.models import *

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Item)