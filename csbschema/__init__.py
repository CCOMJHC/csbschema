from pathlib import Path
from typing import Tuple, Union

from csbschema import validators


__version__ = '1.1.2'

# Current versions
B12_VERSION_3_1_0_2024_04 = '3.1.0-2024-04'
B12_VERSION_3_0_0_2023_08 = '3.0.0-2023-08'
XYZ_B12_VERSION_3_1_0_2024_04 = 'XYZ-3.1.0-2024-04'
XYZ_B12_VERSION_3_0_0_2023_08 = 'XYZ-3.0.0-2023-08'
# Previous versions
B12_VERSION_3_0_0_2023_03 = '3.0.0-2023-03'
XYZ_B12_VERSION_3_0_0_2023_03 = 'XYZ-3.0.0-2023-03'
XYZ_B12_VERSION_3_1_0_2023_08 = 'XYZ-3.1.0-2023-08'
B12_VERSION_3_1_0_2023_03 = '3.1.0-2023-03'
B12_VERSION_3_1_0_2023_08 = '3.1.0-2023-08'
# Development versions
B12_VERSION_3_2_0_BETA = '3.2.0-BETA'

DEFAULT_VALIDATOR_VERSION = B12_VERSION_3_1_0_2024_04
VALIDATORS = {
    # Current versions
    B12_VERSION_3_1_0_2024_04: validators.validate_b12_3_1_0_2024_04,
    XYZ_B12_VERSION_3_1_0_2024_04: validators.validate_b12_xyz_3_1_0_2024_04,
    B12_VERSION_3_0_0_2023_08: validators.validate_b12_3_0_0_2023_08,
    XYZ_B12_VERSION_3_0_0_2023_08: validators.validate_b12_xyz_3_0_0_2023_08,
    # Previous versions
    B12_VERSION_3_0_0_2023_03: validators.validate_b12_3_0_0_2023_03,
    XYZ_B12_VERSION_3_0_0_2023_03: validators.validate_b12_xyz_3_0_0_2023_03,
    XYZ_B12_VERSION_3_1_0_2023_08: validators.validate_b12_xyz_3_1_0_2023_08,
    B12_VERSION_3_1_0_2023_03: validators.validate_b12_3_1_0_2023_03,
    B12_VERSION_3_1_0_2023_08: validators.validate_b12_3_1_0_2023_08,
    # Development versions
    B12_VERSION_3_2_0_BETA: validators.validate_b12_3_2_0_BETA
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
