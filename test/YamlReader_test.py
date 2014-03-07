import unittest
import logging
from yaml_server.YamlReader import YamlReader
from yaml_server.YamlServerException import YamlServerException
from yaml_server.YamlReader import dict_merge


class Test(unittest.TestCase):

    data1_data = {'data1': 'test5', 'data2': [{'test3': 'data4', 'test5': 'data5'}]}

    data2_data = {
                   'data1': 'test1',
                   'data2': [
                            {
                                'test3': 'data4',
                                'test5': 'data5'
                            },
                            {
                                'test6': 'data6'
                            }
                            ],
                    'data3': 'foo'
                  }

    logger = logging.getLogger()
    loghandler = logging.StreamHandler()
    loghandler.setFormatter(logging.Formatter('yaml_server[%(filename)s:%(lineno)d]: %(levelname)s: %(message)s'))
    logger.addHandler(loghandler)
    logger.setLevel(logging.DEBUG)

    def test_should_correctly_merge_single_yaml_file(self):
        self.assertEqual(YamlReader("testdata/data1/test1.yaml", displayname=self.id()).get(), self.data1_data)

    def test_should_correctly_merge_yaml_files_from_dir(self):
        self.assertEqual(YamlReader("testdata/data1", defaultdata={"data3": "foo"}, displayname=self.id()).get(), self.data2_data)

    def test_should_fail_on_invalid_yaml_dir(self):
        self.assertRaises(YamlServerException, YamlReader, "/dev/null", displayname=self.id())

    def test_should_return_default_data_if_invalid_file_given(self):
        self.assertEqual(YamlReader("/dev/null", defaultdata={"foo": "bar"}, displayname=self.id()).get(), {"foo": "bar"})

    def test_should_fail_on_invalid_yaml_file(self):
        self.assertRaises(YamlServerException, YamlReader, "setup.cfg", displayname=self.id())

    def test_should_return_default_data_if_invalid_dir_given(self):
        self.assertEqual(YamlReader("/", defaultdata={"foo": "bar"}, displayname=self.id()).get(), {"foo": "bar"})
    
    def test_should_ignore_an_empty_yaml_file_in_dir(self):
        self.assertEqual(YamlReader("testdata/data_with_empty_file", displayname=self.id()).get(), self.data1_data)
        
    def test_should_merge_dict_of_dict(self):
        self.assertEqual(
            dict_merge(
                {"one": {"one": 1, "two": 2}},
                {"one": {"one": 1, "three": 3}}),
            { "one": {"one": 1, "two": 2, "three": 3}})

if __name__ == "__main__":
    unittest.main()
