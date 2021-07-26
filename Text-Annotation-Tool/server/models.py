import string
from collections import Counter
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage


class Project(models.Model):
    DOCUMENT_CLASSIFICATION = 'DocumentClassification'

    PROJECT_CHOICES = (
        (DOCUMENT_CLASSIFICATION, 'document classification'),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    guideline = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='projects')
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)

    def get_absolute_url(self):
        return reverse('upload', args=[self.id])

    def is_type_of(self, project_type):
        return project_type == self.project_type

    def get_progress(self, user):
        docs = self.get_documents(is_null=True, user=user)
        total = self.documents.count()
        remaining = docs.count()
        return {'total': total, 'remaining': remaining}

    @property
    def image(self):
        url = staticfiles_storage.url('images/cat-1045782_640.jpg')
        return url

    def get_template_name(self):
        template_name = 'annotation/document_classification.html'
        return template_name

    def get_documents(self, is_null=True, user=None):
        docs = self.documents.all()
        if user:
            docs = docs.exclude(doc_annotations__user=user)
        else:
            docs = docs.filter(doc_annotations__isnull=is_null)
        return docs

    def get_document_serializer(self):
        from .serializers import ClassificationDocumentSerializer
        if self.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return ClassificationDocumentSerializer
        else:
            raise ValueError('Invalid project_type')

    def get_annotation_serializer(self):
        from .serializers import DocumentAnnotationSerializer
        if self.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return DocumentAnnotationSerializer

    def get_annotation_class(self):
        return DocumentAnnotation

    def __str__(self):
        return self.name


class Label(models.Model):
    KEY_CHOICES = ((u, c) for u, c in zip(
        string.ascii_lowercase, string.ascii_lowercase))
    COLOR_CHOICES = ()

    text = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10, choices=KEY_CHOICES)
    project = models.ForeignKey(
        Project, related_name='labels', on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#209cee')
    text_color = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return self.text

    class Meta:
        unique_together = (
            ('project', 'text'),
            ('project', 'shortcut')
        )


# class PolicyFile(models.Model):
#     raw_text = models.TextField()
#     project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)


class Document(models.Model):
    text = models.TextField()
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)

    def get_annotations(self):
        if self.project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return self.doc_annotations.all()

    def to_csv(self):
        return self.make_dataset_for_classification()

    def make_dataset_for_classification(self):
        annotations = self.get_annotations()
        dataset = [[a.document.id, a.document.text, a.label.text, a.user.username]
                   for a in annotations]
        return dataset

    def to_json(self):
        return self.make_dataset_json()

    def make_dataset_json(self):
        return self.make_dataset_for_classification_json()

    def make_dataset_for_classification_json(self):
        annotations = self.get_annotations()
        labels = [a.label.text for a in annotations]
        username = annotations[0].user.username
        dataset = {'doc_id': self.id, 'text': self.text,
                   'labels': labels, 'username': username}
        return dataset

    def __str__(self):
        return self.text[:50]


class Annotation(models.Model):
    prob = models.FloatField(default=0.0)
    manual = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class DocumentAnnotation(Annotation):
    document = models.ForeignKey(
        Document, related_name='doc_annotations', on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('document', 'user', 'label')


