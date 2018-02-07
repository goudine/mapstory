import os

from socket import error as socket_error

from django import db
from django.test import TestCase

from geonode.geoserver.helpers import gs_catalog
from geoserver.catalog import FailedRequestError

from ..MapStoryTestMixin import MapStoryTestMixin


class LayersCreateTest(MapStoryTestMixin):

    def create_datastore(self, connection, catalog):
        connection_settings = connection.settings_dict
        params = {'database': connection_settings['NAME'],
                  'passwd': connection_settings['PASSWORD'],
                  'namespace': 'http://www.geonode.org/',
                  'type': 'PostGIS',
                  'dbtype': 'postgis',
                  'host': connection_settings['HOST'],
                  'user': connection_settings['USER'],
                  'port': connection_settings['PORT'],
                  'enabled': "True"}

        store = catalog.create_datastore(connection_settings['NAME'], workspace=self.workspace)
        store.connection_parameters.update(params)

        try:
            catalog.save(store)
        except FailedRequestError:
            # assuming this is because it already exists
            pass

        return catalog.get_store(connection_settings['NAME'])

    def setUp(self):

        try:
            # Ensure Geoserver is running.
            assert gs_catalog.about()
        except socket_error as e:
            print(e.__dict__)
            self.skipTest('Geoserver must be running for this test.')

        self.username, self.password = self.create_user('admin', 'admin', is_superuser=True)
        self.non_admin, self.non_admin_password = self.create_user('non_admin', 'non_admin', is_superuser=True)
        self.layer_name = 'testz'
        self.workspace = 'geonode'
        self.postgis = db.connections['datastore']
        self.datastore = self.create_datastore(self.postgis, gs_catalog)

        cursor = self.postgis.cursor()
        cursor.execute("drop domain if exists bigdate cascade;")
        cursor.execute("create domain bigdate as bigint;")

    def tearDown(self):

        layer = gs_catalog.get_layer(self.layer_name)

        if layer:
            gs_catalog.delete(layer)

        if self.datastore:
            gs_catalog.delete(self.datastore, recurse=True)


from osgeo_importer.tests.tests_original import ExternalUploaderBase

class TestDefaultSLD(ExternalUploaderBase, TestCase):

    filename = 'railroads.zip'

    def setUp(self):

        self._TEST_FILES_DIR = os.path.realpath('mapstory/tests/sampledata/')
        print 'should have set test dir by now, it is below:'
        print self._TEST_FILES_DIR
        super(ExternalUploaderBase, self).setUp()

        print self.filename
        # self.layer = self.fully_import_file(self.filename, extra_config={'convert_to_date': ['YEAR'], 'start_date': 'YEAR', 'configureTime': True})


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