
from logging import Logger
from logging import getLogger
from subprocess import CalledProcessError

from click import secho

from py2appsigner.BaseCommand import BaseCommand
from py2appsigner.environment.NotaryEnvironment import NotaryEnvironment


class Notary(BaseCommand):

    def __init__(self, notaryEnvironment: NotaryEnvironment):

        super().__init__(verbose=notaryEnvironment.verbose)

        self.logger: Logger = getLogger(__name__)

        self._notaryEnvironment: NotaryEnvironment = notaryEnvironment

    def history(self):
        # noinspection SpellCheckingInspection
        """
        xcrun notarytool history --keychain-profile "NOTARY_TOOL_APP_ID"  >> notaryhistory.log
        """
        pass

    def information(self, submissionId: str):
        # noinspection SpellCheckingInspection
        """
        xcrun notarytool log $notarizationId --keychain-profile "NOTARY_TOOL_APP_ID" "notary-${notarizationId}.log"
        """
        outputFile: str = f'notary-${submissionId}.log'

        # noinspection SpellCheckingInspection
        logRequest: str = (
            f'xcrun notarytool log {submissionId} '
            f'--keychain-profile "{self._notaryEnvironment.keyChainProfile}" '
            f'"{outputFile}"'
        )
        try:
            self._runCommand(command=logRequest)
            secho(f'Output is in {outputFile}')
        except CalledProcessError as cpe:
            secho(f'{cpe.stderr}')


