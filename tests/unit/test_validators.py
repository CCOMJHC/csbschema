import unittest
from pathlib import Path
from typing import List

import xmlrunner

from csbschema.validators import validate_b12_3_0_0


class TestValidators(unittest.TestCase):
    def setUp(self) -> None:
        self.fixtures_dir = Path(Path(__file__).parent.parent.parent, 'docs/IHO')

    def tearDown(self) -> None:
        pass

    def test_validate_b12_3_0_0(self):
        # Validate a valid file
        b12_filepath = Path(self.fixtures_dir,
                            'b12_v3_example.json')
        (valid, result) = validate_b12_3_0_0(b12_filepath)
        self.assertTrue(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        with self.assertRaises(KeyError):
            errors: dict = result['errors']
        # Validate an invalid file
        b12_filepath_invalid = Path(self.fixtures_dir,
                                    'b12_v3_example-invalid.json')
        (valid, result) = validate_b12_3_0_0(b12_filepath_invalid)
        self.assertFalse(valid)
        self.assertTrue(isinstance(result, dict))
        document: dict = result['document']
        self.assertTrue(isinstance(document, dict))
        errors: List[dict] = result['errors']
        self.assertTrue(1, len(errors))
        e1 = errors[0]
        self.assertEqual('/features/1/properties', e1['path'])
        self.assertEqual("'depth' is a required property", e1['message'])
        e2 = errors[1]
        self.assertEqual('/features/3/properties', e2['path'])
        self.assertEqual("'time' is a required property", e2['message'])
        e3 = errors[2]
        self.assertEqual('/features/4/properties/time', e3['path'])
        self.assertEqual("'2016-03-03 18:41:49Z' does not match '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)([.][0-9]+)?[Zz]$'",
                         e3['message'])
        e4 = errors[3]
        self.assertEqual('/properties/platform/IDNumber', e4['path'])
        self.assertEqual('IDNumber IMO3699580 is not valid for IDType MMSI.', e4['message'])
        e5 = errors[4]
        self.assertEqual('/properties/platform/dataProcessed', e5['path'])
        self.assertEqual("dataProcessed flag is 'false', but 'processing' properties were found.", e5['message'])


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False
    )
