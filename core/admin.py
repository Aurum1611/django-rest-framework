from django.contrib import admin
from .models import Customer, Document, Profession, DataSheet

admin.site.register(Customer)
admin.site.register(Document)
admin.site.register(Profession)
admin.site.register(DataSheet)
