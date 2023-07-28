import unittest
from pathlib import Path
from typing import List

import xmlrunner

from csbschema.validators import validate_b12_3_1_0_2023_03, \
    validate_b12_3_0_0_2023_03, validate_b12_xyz_3_0_0_2023_03


class TestValidatorsPrevious(unittest.TestCase):
    def setUp(self) -> None:
        self.fixtures_dir = Path(Path(__file__).parent.parent.parent, 'docs')

    def tearDown(self) -> None:
        pass

    def test_validate_b12_3_0_0_2023_03_valid(self):
        documents = [Path(self.fixtures_dir, 'NOAA',
                          'noaa_b12_v3_0_0_suggested-2023-03.json')]
        for doc_path in documents:
            (valid, result) = validate_b12_3_0_0_2023_03(doc_path)
            self.assertTrue(valid)
            self.assertTrue(isinstance(result, dict))
            document: dict = result['document']
            self.assertTrue(isinstance(document, dict))
            with self.assertRaises(KeyError):
                _: dict = result['errors']

    def test_validate_b12_xyz_3_0_0_2023_03_valid(self):
        documents = [Path(self.fixtures_dir, 'NOAA',
                          'noaa_b12_v3_0_0_xyz_suggested-2023-03.json')]
        for doc_path in documents:
            (valid, result) = validate_b12_xyz_3_0_0_2023_03(doc_path)
            self.assertTrue(valid)
            self.assertTrue(isinstance(result, dict))
            document: dict = result['document']
            self.assertTrue(isinstance(document, dict))
            with self.assertRaises(KeyError):
                _: dict = result['errors']

    def test_validate_b12_3_1_0_2023_03_valid(self):
        # Validate a valid file with processing metadata
        b12_filepath = Path(self.fixtures_dir, 'IHO',
                            'b12_v3_1_0_example-2023-03.json')
        (valid, result) = validate_b12_3_1_0_2023_03(b12_filepath)
        self.assertTrue(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        with self.assertRaises(KeyError):
            _: dict = result['errors']


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False
    )
