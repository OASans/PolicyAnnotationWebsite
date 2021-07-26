from django.contrib import admin

from .models import Label, Document, Project
from .models import DocumentAnnotation

admin.site.register(DocumentAnnotation)
admin.site.register(Label)
admin.site.register(Document)
admin.site.register(Project)
