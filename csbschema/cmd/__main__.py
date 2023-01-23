import sys
import argparse
from typing import Union

from csbschema import __version__ as version
from csbschema.cmd import EXIT_USAGE
from csbschema.cmd.validate import validate


class CSBSchema:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='CSB schema tools',
            usage='''csbschema <command> [<arguments>]

    Commands include:
        validate    Validate CSB observation data and metadata using an IHO B12 schema.
                '''
        )
        parser.add_argument('--version', help='print version and exit',
                            action='version', version=f"%(prog)s {version}")
        parser.add_argument('command', help='Subcommand to run')
        # Only consume the command argument here, let sub-commands consume the rest
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print(f"Unrecognized command: {args.command}")
            parser.print_help()
            sys.exit(EXIT_USAGE)
        # Set the subcommand to run
        self.sub_command = args.command

    @staticmethod
    def validate() -> Union[int, str]:
        return validate()

    def run_subcommand(self) -> Union[int, str]:
        return getattr(self, self.sub_command)()


def main():
    csbschema = CSBSchema()
    sys.exit(csbschema.run_subcommand())
