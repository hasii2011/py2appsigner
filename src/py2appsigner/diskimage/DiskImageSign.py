
from logging import Logger
from logging import getLogger

from pathlib import Path

from subprocess import PIPE
from subprocess import STDOUT
from subprocess import Popen as subProcessPOpen

from click import ClickException
from click import secho

from py2appsigner.Common import DMG_SUFFIX

from py2appsigner.diskimage.BaseDiskImage import BaseDiskImage
from py2appsigner.environment.DiskImageEnvironment import DiskImageEnvironment


class DiskImageSign(BaseDiskImage):

    def __init__(self, environment: DiskImageEnvironment):

        super().__init__(environment=environment)

        self.logger: Logger = getLogger(__name__)

    def signDiskImage(self):

        codesignIdentity: str = self._environment.identity

        appName: str  = self._environment.applicationName
        distDir: Path = self._environment.distDirectory

        secho(f'Codesigning DMG with identity: {codesignIdentity}')

        dmgPath: Path = self._computePath(distDir=distDir, baseName=appName, suffix=DMG_SUFFIX)

        codeSignCmd: list[str] = [
            'codesign',
            '--force',
            '--display',
            '--sign', codesignIdentity,
            str(dmgPath)
        ]

        codeSignProcess: subProcessPOpen[str]
        with subProcessPOpen(
            codeSignCmd,
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            bufsize=1
        ) as codeSignProcess:
            if codeSignProcess.stdout is not None:
                cmdOutput: str
                for cmdOutput in codeSignProcess.stdout:
                    secho(cmdOutput, nl=False)

            returnCode: int = codeSignProcess.wait()
            if returnCode != 0:
                raise ClickException(f'`codesign` failed with return code {returnCode}')
