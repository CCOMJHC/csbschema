from pathlib import Path
from typing import Tuple, Union

from csbschema import validators


__version__ = '1.0.2.dev0'



B12_VERSION_3_0_0_2023_02 = '3.0.0-2023-02'
B12_VERSION_3_0_0bis_2023_02 = '3.0.0bis-2023-02'
B12_VERSION_3_0_0_2022_12 = '3.0.0-2022-12'
B12_VERSION_3_0_0bis_2022_12 = '3.0.0bis-2022-12'

DEFAULT_VALIDATOR_VERSION = B12_VERSION_3_0_0_2023_02
VALIDATORS = {
    B12_VERSION_3_0_0_2023_02: validators.validate_b12_3_0_0_2023_02,
    B12_VERSION_3_0_0bis_2023_02: validators.validate_b12_3_0_0bis_2023_02,
    B12_VERSION_3_0_0_2022_12: validators.validate_b12_3_0_0_2022_12,
    B12_VERSION_3_0_0bis_2022_12: validators.validate_b12_3_0_0bis_2022_12
}


def validate_data(document_path: Union[Path, str], *,
                  version=DEFAULT_VALIDATOR_VERSION) -> Tuple[bool, dict]:
    """
    Dispatch to a version-specific validator for CSB data.
    :param document_path: Path to document to be validated
    :param version: Version of schema validator
    :return: Tuple[bool, dict]. If bool is True (which signals that validation succeeded), then dict represents the
        document that was validated. If bool is False (which signals that validation failed), then dict will contain
        a mapping of JSON path element to error encountered at that element.
    """
    if version not in VALIDATORS:
        raise ValueError(f"Unknown validator version: {version}")

    return VALIDATORS[version](document_path)
