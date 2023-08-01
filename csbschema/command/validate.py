import sys
from typing import Union
import argparse
import logging

from csbschema.command import EXIT_DATAERR, EXIT_OK
from csbschema import DEFAULT_VALIDATOR_VERSION, VALIDATORS, validate_data

logger = logging.getLogger(__name__)


def validate() -> Union[int, str]:
    parser = argparse.ArgumentParser(
        description='Validate CSB observation data and metadata using an IHO B12 schema.'
    )
    parser.add_argument('-f', '--file', help='CSB JSON data file to validate', required=True)
    parser.add_argument('--version',
                        choices=VALIDATORS.keys(), default=DEFAULT_VALIDATOR_VERSION,
                        help=f"CSB schema version to validate against. Default: {DEFAULT_VALIDATOR_VERSION}")
    args = parser.parse_args(sys.argv[2:])

    (valid, result) = validate_data(args.file, version=args.version)
    if not valid:
        print(f"Validation of {args.file} against schema {args.version} failed due to the following errors: ")
        for e in result['errors']:
            print(f"Path: {e['path']}, error: {e['message']}")
        return EXIT_DATAERR
    else:
        print(f"CSB data file '{args.file}' successfully validated against schema '{args.version}'.")
        return EXIT_OK
