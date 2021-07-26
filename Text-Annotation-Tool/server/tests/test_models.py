from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mixer.backend.django import mixer


class TestProject(TestCase):

    def test_project_type(self):
        project = mixer.blend('server.Project')
        project.is_type_of(project.project_type)

    def test_get_progress(self):
        project = mixer.blend('server.Project')
        res = project.get_progress()
        self.assertEqual(res['total'], 0)
        self.assertEqual(res['remaining'], 0)


class TestLabel(TestCase):

    def test_shortcut_uniqueness(self):
        label = mixer.blend('server.Label')
        mixer.blend('server.Label', shortcut=label.shortcut)
        with self.assertRaises(IntegrityError):
            mixer.blend('server.Label',
                        project=label.project,
                        shortcut=label.shortcut)

    def test_text_uniqueness(self):
        label = mixer.blend('server.Label')
        mixer.blend('server.Label', text=label.text)
        with self.assertRaises(IntegrityError):
            mixer.blend('server.Label',
                        project=label.project,
                        text=label.text)


class TestDocumentAnnotation(TestCase):

    def test_uniqueness(self):
        annotation1 = mixer.blend('server.DocumentAnnotation')
        with self.assertRaises(IntegrityError):
            mixer.blend('server.DocumentAnnotation',
                        document=annotation1.document,
                        user=annotation1.user,
                        label=annotation1.label)


