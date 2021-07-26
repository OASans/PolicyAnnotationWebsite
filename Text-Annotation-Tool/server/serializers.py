from rest_framework import serializers

from .models import Label, Project, Document
from .models import DocumentAnnotation


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'text', 'shortcut', 'background_color', 'text_color')


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'text')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'guideline', 'users', 'project_type', 'image', 'updated_at')


class ProjectFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        view = self.context.get('view', None)
        request = self.context.get('request', None)
        queryset = super(ProjectFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset or not view:
            return None
        return queryset.filter(project=view.kwargs['project_id'])


class DocumentAnnotationSerializer(serializers.ModelSerializer):
    label = ProjectFilteredPrimaryKeyRelatedField(queryset=Label.objects.all())

    class Meta:
        model = DocumentAnnotation
        fields = ('id', 'prob', 'label')

    def create(self, validated_data):
        annotation = DocumentAnnotation.objects.create(**validated_data)
        return annotation


class ClassificationDocumentSerializer(serializers.ModelSerializer):
    annotations = serializers.SerializerMethodField()

    def get_annotations(self, instance):
        request = self.context.get('request')
        if request:
            annotations = instance.doc_annotations.filter(user=request.user)
            serializer = DocumentAnnotationSerializer(annotations, many=True)
            return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'text', 'annotations')

