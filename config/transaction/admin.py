from django.contrib import admin
from transaction.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Transaction)
admin.site.register(Status)
admin.site.register(Type)




