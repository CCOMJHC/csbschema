import unittest
import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Optional

import xmlrunner

from csbschema.validators import ID_NUMBER_IMO_RE, ID_NUMBER_MMSI_RE

logger = logging.getLogger(__name__)


class TestRegexes(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_epsg_regex(self) -> None:
        # Regex to validate EPSG identifier for EPSG codes between 1024 to 32767 (inclusive)
        patt = r'^EPSG:(3276[0-7]$|327[0-5]\d$|32[0-6]\d\d$|3[0-1]\d\d\d$|[1-2][0-9]{4}$|102[4-9]|10[3-9][0-9]$|1[1-9][0-9][0-9]$|[2-9][0-9][0-9][0-9]$)'
        regex = re.compile(patt)

        # First, test invalid numbers less than 1023
        epsg_num = 0
        while epsg_num < 1024:
            epsg_str = f"EPSG:{epsg_num}"
            self.assertIsNone(regex.match(epsg_str))
            epsg_num += 1

        # Next, test valid numbers from 1024 to 32767
        while epsg_num < 32768:
            epsg_str = f"EPSG:{epsg_num}"
            m = regex.match(epsg_str)
            self.assertIsNotNone(m, f"Pattern not matched for epsg_num: {epsg_num}")
            matched_num = int(m.group(1))
            self.assertEqual(epsg_num, matched_num)
            epsg_num += 1

        # Finally, test some invalid numbers greater than 32767 but less than 10,001
        while epsg_num < 10_001:
            epsg_str = f"EPSG:{epsg_num}"
            self.assertIsNone(regex.match(epsg_str))
            epsg_num += 1

    @staticmethod
    def _parse_rfc3339_utc(timestamp: str) -> Optional[datetime]:
        FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        FMT_NO_MICRO = "%Y-%m-%dT%H:%M:%SZ"
        try:
            # First try to parse time with microseconds
            return datetime.strptime(timestamp.upper(), FMT).replace(tzinfo=timezone.utc)
        except ValueError as e:
            # Try to parse time without microseconds before failing
            try:
                return datetime.strptime(timestamp.upper(), FMT_NO_MICRO).replace(tzinfo=timezone.utc)
            except ValueError:
                return None

    def test_RFC3339_time(self) -> None:
        patt = r'^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)([.][0-9]+)?[Zz]$'
        regex = re.compile(patt)

        time_1 = '2016-03-03T18:41:49Z'
        self.assertIsNotNone(regex.match(time_1))
        dt_1 = self._parse_rfc3339_utc(time_1)
        self.assertIsNotNone(dt_1)
        self.assertEqual(datetime(2016, 3, 3, 18, 41, 49, tzinfo=timezone.utc), dt_1)

        time_2 = '2016-03-03t18:41:50z'
        self.assertIsNotNone(regex.match(time_2))
        dt_2 = self._parse_rfc3339_utc(time_2)
        self.assertIsNotNone(dt_2)
        self.assertEqual(datetime(2016, 3, 3, 18, 41, 50, tzinfo=timezone.utc), dt_2)

        time_3 = '2016-03-03t18:41:51Z'
        self.assertIsNotNone(regex.match(time_3))
        dt_3 = self._parse_rfc3339_utc(time_3)
        self.assertIsNotNone(dt_3)
        self.assertEqual(datetime(2016, 3, 3, 18, 41, 51, tzinfo=timezone.utc), dt_3)

        time_4 = '2016-03-03T18:41:52z'
        self.assertIsNotNone(regex.match(time_4))
        dt_4 = self._parse_rfc3339_utc(time_4)
        self.assertIsNotNone(dt_4)
        self.assertEqual(datetime(2016, 3, 3, 18, 41, 52, tzinfo=timezone.utc), dt_4)

        time_5 = '2016-03-03T18:41:52.2342z'
        self.assertIsNotNone(regex.match(time_5))
        dt_5 = self._parse_rfc3339_utc(time_5)
        self.assertIsNotNone(dt_5)
        self.assertEqual(datetime(2016, 3, 3, 18, 41, 52, 234200, tzinfo=timezone.utc), dt_5)

        time_6 = '2017-02-05T21:13:30.000Z'
        self.assertIsNotNone(regex.match(time_6))
        dt_6 = self._parse_rfc3339_utc(time_6)
        self.assertIsNotNone(dt_6)
        self.assertEqual(datetime(2017, 2, 5, 21, 13, 30, 0, tzinfo=timezone.utc), dt_6)

        # B-12 timestamps must be expressed in UTC, not in local time offsets
        invalid_time_1 = '1996-12-19T16:39:57-08:00'
        self.assertIsNone(regex.match(invalid_time_1))
        invalid_time_2 = '1985-04-12'
        self.assertIsNone(regex.match(invalid_time_2))
        invalid_time_3 = 'whatyearisthis?'
        self.assertIsNone(regex.match(invalid_time_3))

    def test_IDNumber_IMO(self) -> None:
        regex = re.compile(ID_NUMBER_IMO_RE)

        self.assertIsNone(regex.match('369958000'))
        self.assertIsNotNone(regex.match('IMO3699580'))

    def test_IDNumber_MMSI(self) -> None:
        regex = re.compile(ID_NUMBER_MMSI_RE)

        self.assertIsNone(regex.match('IMO3699580'))
        self.assertIsNotNone(regex.match('369958000'))

    def test_uniqueVesselID(self) -> None:
        patt = r'^[a-zA-Z][a-zA-Z0-9]*-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        regex = re.compile(patt)

        test_uuid = str(uuid.uuid4())
        self.assertIsNone(regex.match(test_uuid))
        valid_id_1 = f"CCOM-{test_uuid}"
        self.assertIsNotNone(regex.match(valid_id_1))
        valid_id_2 = f"CCOM1-{test_uuid}"
        self.assertIsNotNone(regex.match(valid_id_2))
        invalid_id_1 = f"1234-{test_uuid}"
        self.assertIsNone(regex.match(invalid_id_1))
        invalid_id_2 = f"-{test_uuid}"
        self.assertIsNone(regex.match(invalid_id_2))
        invalid_id_3 = f".!@3a-{test_uuid}"
        self.assertIsNone(regex.match(invalid_id_3))

    def test_providerEmail(self) -> None:
        patt = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$'
        regex = re.compile(patt)
        # Valid e-mails
        email_1 = 'test+mailbox@example.com'
        self.assertIsNotNone(regex.match(email_1))
        email_2 = 'support@sea-id.org'
        self.assertIsNotNone(regex.match(email_2))
        email_3 = 'support@example.com'
        self.assertIsNotNone(regex.match(email_3))
        # Invalid e-mails
        email_4 = 'sketchy@128.2.192.168'
        self.assertIsNone(regex.match(email_4))
        not_email = 'hello, world!'
        self.assertIsNone(regex.match(not_email))


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False
    )
