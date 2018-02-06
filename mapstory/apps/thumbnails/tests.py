import os
import StringIO

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from .models import ThumbnailImage, ThumbnailImageForm


class TestThumbnailImage(TestCase):
    """
    Thumbnail Image model tests
    """
    def setUp(self):
        self.thumbnailImage = ThumbnailImage()
        self.assertIsInstance(self.thumbnailImage, ThumbnailImage)

    def test_unicode(self):
        self.assertIsNotNone(unicode(self.thumbnailImage))

    def test_upload_gif_thumbnail(self):
        initial_thumbnail_count = ThumbnailImage.objects.all().count()
        # Load a test gif
        image = Image.open(os.path.join('mapstory/apps/thumbnails/test.gif'))

        # Convert the image to text
        string_gif = StringIO.StringIO()
        image.save(string_gif, 'gif')
        string_gif.seek(0)

        # Create a test upload
        test_gif = SimpleUploadedFile(
            "test.gif",
            string_gif.read(),
            content_type="image/gif"
        )
        self.assertIsNotNone(image)

        # Create a thumbnail model object
        test_thumbnail = ThumbnailImage()
        test_thumbnail.thumbnail_image.save(
            'test.gif',
            content=test_gif,
            save=True
        )
        self.assertIsInstance(test_thumbnail, ThumbnailImage)

        # Should update the Thumbnail object count
        test_thumbnail.save()
        final_thumbnail_count = ThumbnailImage.objects.all().count()
        self.assertEqual(final_thumbnail_count, initial_thumbnail_count + 1)

    def test_upload_png_thumbail(self):
        initial_thumbnail_count = ThumbnailImage.objects.all().count()
        # Load a test gif
        image = Image.open(os.path.join('mapstory/apps/thumbnails/map-marker-icon.png'))

        # Convert the image to text
        image_as_string = StringIO.StringIO()
        image.save(image_as_string, 'png')
        image_as_string.seek(0)

        # Create a test upload
        test_png = SimpleUploadedFile(
            "test.png",
            image_as_string.read(),
            content_type="image/png"
        )
        self.assertIsNotNone(image)

        # Create a thumbnail model object
        test_thumbnail = ThumbnailImage()
        test_thumbnail.thumbnail_image.save(
            'test.png',
            content=test_png,
            save=True
        )
        self.assertIsInstance(test_thumbnail, ThumbnailImage)

        # Should update the Thumbnail object count
        test_thumbnail.save()
        final_thumbnail_count = ThumbnailImage.objects.all().count()
        self.assertEqual(final_thumbnail_count, initial_thumbnail_count + 1)


class TestThumbnailImageForm(TestCase):
    """
    ThumbnailImageForm model tests
    """
    def setUp(self):
        self.tif = ThumbnailImageForm()
        self.assertIsInstance(self.tif, ThumbnailImageForm)

    def test_unicode(self):
        self.assertIsNotNone(unicode(self.tif))


from osgeo_importer.tests.tests_original import ExternalUploaderBase

class TestDefaultSLD(ExternalUploaderBase, TestCase):

    filename = 'railroads.zip'

    def setUp(self):

        self._TEST_FILES_DIR = os.path.realpath('mapstory/tests/sampledata/')
        super(ExternalUploaderBase, self).setUp()

        print self.filename
        self.layer = self.fully_import_file(self.filename, extra_config={'convert_to_date': ['YEAR'], 'start_date': 'YEAR', 'configureTime': True})


    def test_point(self):

        import pydevd
        pydevd.settrace('192.168.0.15', port=65432, stdoutToServer=True, stderrToServer=True,
                        trace_only_current_thread=False, overwrite_prev_trace=True, patch_multiprocessing=True)

        filename = self.get_datafile_path('american_civil_war.zip')

        print self.filename
        result = self.fully_import_file(filename)
        print result
        # self.catalog.get_layer(result.name).default_style.filename == 'Generic_Mapstory_Polygon.sld'
        t=1

    def test_polygon(self):

        filename = self.get_datafile_path('boxes_with_date_iso_date.zip')

        print self.filename
        result = self.fully_import_file(filename)
        print result
        # self.catalog.get_layer(result.name).default_style.filename == 'Generic_Mapstory_Polygon.sld'
        t=1

    def test_line(self):

        filename = self.get_datafile_path('railroads.zip')

        result = self.fully_import_file(filename)
        print result
        # self.catalog.get_layer(result.name).default_style.filename == 'Generic_Mapstory_Polygon.sld'
        t=1

    def test_empty(self):

        filename = self.get_datafile_path('empty_layer.zip')

        result = self.fully_import_file(filename)
        print result
        # self.catalog.get_layer(result.name).default_style.filename == 'Generic_Mapstory_Polygon.sld'
        t=1


