from yaml_server.YamlServerRequestHandler import YamlServerRequestHandler
import yaml_server
from unittest2 import TestCase
from mock import MagicMock
import mock
import __builtin__


class YamlServerRequestHandler_tests(TestCase):

    TEST_YAML ="""my super test yaml"""

    TEST_LOCATIONS = """
        locations:
            - monitoring
            - service-monitoring"""

    def setUp(self):
        mock_yaml_locations = MagicMock()
        mock_yaml_locations.get_yaml.return_value = self.TEST_YAML
        mock_yaml_locations.get_locations_as_yaml.return_value = self.TEST_LOCATIONS
        yaml_server.__config__["locations"] = mock_yaml_locations
        self.patcher = mock.patch('SimpleHTTPServer.SimpleHTTPRequestHandler')
        self.patcher.start()
        self.request_handler = YamlServerRequestHandler()
        self.request_handler.send_response = MagicMock()
        self.request_handler.headers = ""
        self.request_handler.send_header = MagicMock()
        self.request_handler.wfile = MagicMock()
        self.request_handler.date_time_string = MagicMock()
        self.request_handler.date_time_string.return_value = "NOW"

    def tearDown(self):
        self.patcher.stop()

    def test_get_locations(self):
        self.request_handler.path ="/"
        self.request_handler.do_GET()

        self.request_handler.send_header.assert_any_call('ETag', 'e363ed10bccdb2842e14498ef956a346a83f0617ddeeb8e991a654691c0ea836')
        self.request_handler.send_header.assert_any_call('Content-length', len(self.TEST_LOCATIONS))
        self.request_handler.send_header.assert_any_call('Content-type', 'application/yaml')
        self.request_handler.wfile.write.assert_any_call(self.TEST_LOCATIONS)

    def test_get_yaml(self):
        self.request_handler.path ="/unittest"
        self.request_handler.do_GET()

        self.request_handler.send_header.assert_any_call('ETag', '6ee9c999bead9a4015de1b5108e3ac005a4893aa6e79e207b3be403063f1a296')
        self.request_handler.send_header.assert_any_call('Content-length', len(self.TEST_YAML))
        self.request_handler.send_header.assert_any_call('Content-type', 'application/yaml')
        self.request_handler.send_header.assert_any_call('Last-Modified', 'NOW')
        self.request_handler.wfile.write.assert_any_call(self.TEST_YAML)
