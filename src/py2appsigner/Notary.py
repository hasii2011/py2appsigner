
from logging import Logger
from logging import getLogger

from subprocess import CompletedProcess
from subprocess import run as subProcessRun
from subprocess import CalledProcessError

from click import secho

from py2appsigner.BaseCommand import BaseCommand
from py2appsigner.environment.NotaryEnvironment import NotaryEnvironment


# noinspection SpellCheckingInspection
PARTIAL_NOTARY_TOOL_CLI:     str = ' xcrun notarytool '
PARAMETER_KEY_CHAIN_PROFILE: str = ' --keychain-profile '
NOTARY_HISTORY_FILENAME:     str = 'notaryHistory.log'


class Notary(BaseCommand):

    def __init__(self, notaryEnvironment: NotaryEnvironment):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._notaryEnvironment: NotaryEnvironment = notaryEnvironment

    def history(self):
        # noinspection SpellCheckingInspection
        """
        xcrun notarytool history --keychain-profile "NOTARY_TOOL_APP_ID"  >> notaryhistory.log
        """
        historyRequest: str = (
            f'{PARTIAL_NOTARY_TOOL_CLI} history {PARAMETER_KEY_CHAIN_PROFILE} {self._notaryEnvironment.keyChainProfile}'
        )
        # Don't use base command method;  I want to capture the output and write it to a file
        completedProcess: CompletedProcess = subProcessRun([historyRequest], shell=True, capture_output=True, text=True, check=True)
        if completedProcess.returncode == 0:
            with open(NOTARY_HISTORY_FILENAME, 'w') as fd:
                fd.write(completedProcess.stdout)
            secho(f'See: {NOTARY_HISTORY_FILENAME}')

    def information(self, submissionId: str):
        # noinspection SpellCheckingInspection
        """
        xcrun notarytool log $notarizationId --keychain-profile "NOTARY_TOOL_APP_ID" "notary-${notarizationId}.log"
        """
        outputFile: str = f'notary-{submissionId}.log'

        # noinspection SpellCheckingInspection
        logRequest: str = (
            f'{PARTIAL_NOTARY_TOOL_CLI} log {submissionId} '
            f'{PARAMETER_KEY_CHAIN_PROFILE} "{self._notaryEnvironment.keyChainProfile}" '
            f'"{outputFile}"'
        )
        try:
            self._runCommand(command=logRequest)
            secho(f'Output is in {outputFile}')
        except CalledProcessError as cpe:
            secho(f'{cpe.stderr}')
