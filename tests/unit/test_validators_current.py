import unittest
from pathlib import Path
from typing import List

import xmlrunner

from csbschema.validators import validate_b12_3_1_0_2023_08, validate_b12_xyz_3_1_0_2023_08, \
    validate_b12_3_0_0_2023_08, validate_b12_xyz_3_0_0_2023_08, validate_b12_3_2_0_BETA


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
            (valid, result) = validate_b12_3_0_0_2023_08(doc_path)
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
            (valid, result) = validate_b12_xyz_3_0_0_2023_08(doc_path)
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
        self.assertEqual(9, len(errors))
        error = errors[0]
        self.assertEqual('/properties/trustedNode/convention', error['path'])
        self.assertEqual("'GeoJSON CSB 3.0' is not one of ['GeoJSON CSB 3.1']", error['message'])
        error = errors[1]
        self.assertEqual('/properties/processing/5', error['path'])
        self.assertEqual("{'type': 'VerticalOffsetAnalysis', 'timestamp': '2021-11-22T16:10:09.346821Z', 'name': 'CIDCO Vertical Offset Analysis', 'version': '1.0.0', 'reference': 'DOI:10.47366/sabia.v5n1a3', 'comment': 'FREE TEXT HERE', 'analysis': [{'name': 'Chi2', 'pass': True, 'parameters': {'a': 123.456, 'b': 789.012, 'target': 'Normal', 'df': 15, 'alpha': 0.05, 'pmf': {'centers': [-1.0, -0.5, 0, 0.5, 1.0], 'counts': [0, 24, 50, 120, 23, 0]}}, 'reference': 'DOI:10.47366/sabia.v5n1a3', 'comment': 'FREE TEXT HERE'}]} is not valid under any of the given schemas",
                         error['message'])
        error = errors[2]
        self.assertEqual('/features/1/properties', error['path'])
        self.assertEqual("'depth' is a required property", error['message'])
        error = errors[3]
        self.assertEqual('/features/3/properties', error['path'])
        self.assertEqual("'time' is a required property", error['message'])
        error = errors[4]
        self.assertEqual('/features/4/properties/time', error['path'])
        self.assertEqual("'2016-03-03 18:41:49Z' does not match '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)([.][0-9]+)?[Zz]$'",
                         error['message'])
        error = errors[5]
        self.assertEqual('/properties/platform/IDNumber', error['path'])
        self.assertEqual('IDNumber IMO3699580 is not valid for IDType MMSI.', error['message'])
        error = errors[6]
        self.assertEqual('/properties/platform/dataProcessed', error['path'])
        self.assertEqual("dataProcessed flag is 'false', but 'processing' properties were found.", error['message'])
        error = errors[7]
        self.assertEqual('/properties/platform/uniqueID', error['path'])
        self.assertEqual("uniqueID: SEAID-45f5c322-10f2-4946-802e-d5992ad36727 does not match /properties/trustedNode/uniqueVesselID: SEAID-e8c469f8-df38-11e5-b86d-9a79f06e9478",
                         error['message'])
        # Check error message for missing uncert. metadata
        error = errors[8]
        self.assertEqual('/features/1/properties', error['path'])
        self.assertEqual('Observation uncertainty found, but Uncertainty metadata was not found.',
                         error['message'])

        # Validate an invalid file with an empty processing property array
        b12_filepath_invalid = Path(self.fixtures_dir, 'IHO',
                                    'b12_v3_1_0_example-invalid-emptyprocessing.json')
        (valid, result) = validate_b12_3_1_0_2023_08(b12_filepath_invalid)
        self.assertFalse(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        errors: List[dict] = result['errors']
        self.assertEqual(2, len(errors))
        error = errors[0]
        self.assertEqual('/properties/processing', error['path'])
        self.assertEqual('[] is too short', error['message'])
        # Check error message for missing uncert. metadata
        error = errors[1]
        self.assertEqual('/features/2/properties', error['path'])
        self.assertEqual('Observation uncertainty found, but Uncertainty metadata was not found.',
                         error['message'])

    def test_validate_b12_xyz_3_1_0_valid(self):
        documents = [Path(self.fixtures_dir, 'IHO',
                          'b12_v3_1_0_xyz_example.json')]
        for doc_path in documents:
            (valid, result) = validate_b12_xyz_3_1_0_2023_08(doc_path)
            self.assertTrue(valid)
            self.assertTrue(isinstance(result, dict))
            document: dict = result['document']
            self.assertTrue(isinstance(document, dict))
            with self.assertRaises(KeyError):
                _: dict = result['errors']

    def test_validate_b12_xyz_3_1_0_invalid(self):
        b12_filepath_invalid = Path(self.fixtures_dir, 'IHO',
                                    'b12_v3_1_0_xyz_example-invalid.json')
        (valid, result) = validate_b12_xyz_3_1_0_2023_08(b12_filepath_invalid)
        self.assertFalse(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        errors: List[dict] = result['errors']
        self.assertEqual(5, len(errors))
        error = errors[0]
        self.assertEqual('/trustedNode/convention', error['path'])
        self.assertEqual("'XYZ GeoJSON CSB 3.0' is not one of ['XYZ GeoJSON CSB 3.1']", error['message'])
        error = errors[1]
        self.assertEqual('/processing/5', error['path'])
        self.assertEqual(
            "{'type': 'VerticalOffsetAnalysis', 'timestamp': '2021-11-22T16:10:09.346821Z', 'name': 'CIDCO Vertical Offset Analysis', 'version': '1.0.0', 'reference': 'DOI:10.47366/sabia.v5n1a3', 'comment': 'FREE TEXT HERE', 'analysis': [{'name': 'Chi2', 'pass': True, 'parameters': {'a': 123.456, 'b': 789.012, 'target': 'Normal', 'df': 15, 'alpha': 0.05, 'pmf': {'centers': [-1.0, -0.5, 0, 0.5, 1.0], 'counts': [0, 24, 50, 120, 23, 0]}}, 'reference': 'DOI:10.47366/sabia.v5n1a3', 'comment': 'FREE TEXT HERE'}]} is not valid under any of the given schemas",
            error['message'])
        error = errors[2]
        self.assertEqual('/platform/IDNumber', error['path'])
        self.assertEqual('IDNumber IMO3699580 is not valid for IDType MMSI.', error['message'])
        error = errors[3]
        self.assertEqual('/platform/dataProcessed', error['path'])
        self.assertEqual("dataProcessed flag is 'false', but 'processing' properties were found.", error['message'])
        error = errors[4]
        self.assertEqual('/platform/uniqueID', error['path'])
        self.assertEqual(
            "uniqueID: SEAID-45f5c322-10f2-4946-802e-d5992ad36727 does not match /trustedNode/uniqueVesselID: SEAID-e8c469f8-df38-11e5-b86d-9a79f06e9478",
            error['message'])

    def test_validate_b12_3_2_0_BETA_valid(self):
        # Validate a valid file with processing metadata
        b12_filepath = Path(self.fixtures_dir, 'IHO',
                            'b12_v3_2_0-BETA_example.json')
        (valid, result) = validate_b12_3_2_0_BETA(b12_filepath)
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
