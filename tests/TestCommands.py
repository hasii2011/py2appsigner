
from typing import List

from py2appsigner.Commands import zipsign

from click.testing import CliRunner


def testZipSignHelp():

    runner: CliRunner = CliRunner()

    result = runner.invoke(zipsign, ['--help'])

    assert result.exit_code == 0

    # noinspection PyUnusedLocal
    expectedOutput: str = (
        'Usage: zipsign[OPTIONS]\n\n'
        'Options:\n'
        '  --version                     Show the version and exit.\n'
        '  -p, --pyversion TEXT          Identify the python version  [required]\n'
        '  -b, --projects-base TEXT      Projects base, overrides environment variables\n'
        '  -d, --project-directory TEXT  Project directory, overrides environment\n'
        '                                variables\n'
        '  -a, --app-name TEXT           The application name that py2app built\n'
        '                                [required]\n'
        '  --help                        Show this message and exit.'
    )
    actualOutputList: List[str] = result.output.split('\n')
    assert len(actualOutputList) == 12, 'Help output mismatch'

    assert actualOutputList[5] == '  -b, --projects-base TEXT      Projects base, overrides environment variables', 'Help line does not match'


if __name__ == "__main__":

    testZipSignHelp()
