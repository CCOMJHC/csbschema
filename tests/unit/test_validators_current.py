import unittest
from pathlib import Path
from typing import List

import xmlrunner

from csbschema.validators import validate_b12_3_1_0_2023_08, \
    validate_b12_3_0_0_2023_03, validate_b12_xyz_3_0_0_2023_03


class TestValidatorsCurrent(unittest.TestCase):
    def setUp(self) -> None:
        self.fixtures_dir = Path(Path(__file__).parent.parent.parent, 'docs')

    def tearDown(self) -> None:
        pass

    def test_validate_b12_3_0_0_valid(self):
        documents = [Path(self.fixtures_dir, 'NOAA',
                          'example_csb_geojson_file.geojson'),
                     Path(self.fixtures_dir, 'NOAA',
                          'noaa_b12_v3_0_0_required.json'),
                     Path(self.fixtures_dir, 'NOAA',
                          'noaa_b12_v3_0_0_suggested.json')]
        for doc_path in documents:
            (valid, result) = validate_b12_3_0_0_2023_03(doc_path)
            self.assertTrue(valid)
            self.assertTrue(isinstance(result, dict))
            document: dict = result['document']
            self.assertTrue(isinstance(document, dict))
            with self.assertRaises(KeyError):
                _: dict = result['errors']

    def test_validate_b12_xyz_3_0_0_valid(self):
        documents = [Path(self.fixtures_dir, 'NOAA',
                          'noaa_b12_v3_0_0_xyz_required.json'),
                     Path(self.fixtures_dir, 'NOAA',
                          'noaa_b12_v3_0_0_xyz_suggested.json')]
        for doc_path in documents:
            (valid, result) = validate_b12_xyz_3_0_0_2023_03(doc_path)
            self.assertTrue(valid)
            self.assertTrue(isinstance(result, dict))
            document: dict = result['document']
            self.assertTrue(isinstance(document, dict))
            with self.assertRaises(KeyError):
                _: dict = result['errors']

    def test_validate_b12_3_1_0_valid(self):
        # Validate a valid file with processing metadata
        b12_filepath = Path(self.fixtures_dir, 'IHO',
                            'b12_v3_1_0_example.json')
        (valid, result) = validate_b12_3_1_0_2023_08(b12_filepath)
        self.assertTrue(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        with self.assertRaises(KeyError):
            _: dict = result['errors']

        # Validate a valid file without processing metadata
        b12_filepath = Path(self.fixtures_dir, 'IHO',
                            'b12_v3_1_0_example-noprocessing.json')
        (valid, result) = validate_b12_3_1_0_2023_08(b12_filepath)
        self.assertTrue(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        with self.assertRaises(KeyError):
            _: dict = result['errors']

    def test_validate_b12_3_1_0_invalid(self):
        # Validate an invalid file
        b12_filepath_invalid = Path(self.fixtures_dir, 'IHO',
                                    'b12_v3_1_0_example-invalid.json')
        (valid, result) = validate_b12_3_1_0_2023_08(b12_filepath_invalid)
        self.assertFalse(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        errors: List[dict] = result['errors']
        self.assertEqual(8, len(errors))
        e1 = errors[0]
        self.assertEqual('/properties/trustedNode/convention', e1['path'])
        self.assertEqual("'GeoJSON CSB 3.0' is not one of ['GeoJSON CSB 3.1']", e1['message'])
        e2 = errors[1]
        self.assertEqual('/features/1/properties', e2['path'])
        self.assertEqual("'depth' is a required property", e2['message'])
        e3 = errors[2]
        self.assertEqual('/features/3/properties', e3['path'])
        self.assertEqual("'time' is a required property", e3['message'])
        e4 = errors[3]
        self.assertEqual('/features/4/properties/time', e4['path'])
        self.assertEqual("'2016-03-03 18:41:49Z' does not match '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)([.][0-9]+)?[Zz]$'",
                         e4['message'])
        e5 = errors[4]
        self.assertEqual('/properties/platform/IDNumber', e5['path'])
        self.assertEqual('IDNumber IMO3699580 is not valid for IDType MMSI.', e5['message'])
        e6 = errors[5]
        self.assertEqual('/properties/platform/dataProcessed', e6['path'])
        self.assertEqual("dataProcessed flag is 'false', but 'processing' properties were found.", e6['message'])
        e7 = errors[6]
        self.assertEqual('/properties/platform/uniqueID', e7['path'])
        self.assertEqual("uniqueID: SEAID-45f5c322-10f2-4946-802e-d5992ad36727 does not match /properties/trustedNode/uniqueVesselID: SEAID-e8c469f8-df38-11e5-b86d-9a79f06e9478",
                         e7['message'])
        # TODO: Check error message for missing uncert. metadata

        # Validate an invalid file with an empty processing property array
        b12_filepath_invalid = Path(self.fixtures_dir, 'IHO',
                                    'b12_v3_1_0_example-invalid-emptyprocessing.json')
        (valid, result) = validate_b12_3_1_0_2023_08(b12_filepath_invalid)
        self.assertFalse(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        errors: List[dict] = result['errors']
        self.assertEqual(1, len(errors))
        e1 = errors[0]
        self.assertEqual('/properties/processing', e1['path'])
        self.assertEqual('[] is too short', e1['message'])


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False
    )
