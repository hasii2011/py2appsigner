
from typing import List
from typing import Optional

from logging import Logger
from logging import getLogger

from os import symlink

from pathlib import Path

from shutil import copytree

from subprocess import PIPE
from subprocess import STDOUT
from subprocess import Popen as subProcessPOpen

from click import ClickException
from click import secho

from py2appsigner.diskimage.BaseDiskImage import BaseDiskImage
from py2appsigner.diskimage.BaseDiskImage import DMG_SUFFIX
from py2appsigner.diskimage.HDIUtilPuppetStringOutput import HDIUtilPuppetStringOutput

from py2appsigner.environment.DiskImageEnvironment import DiskImageEnvironment

APP_SUFFIX:   str = 'app'
STAGE_SUFFIX: str = '_dmg_stage'

STANDARD_HDI_UTIL_OPTIONS: List[str] = [
    'hdiutil', 'create',
    '-ov',
    '-format', 'UDZO'
]

class DiskImageCreate(BaseDiskImage):

    def __init__(self, environment: DiskImageEnvironment):

        super().__init__(environment=environment)
        self.logger: Logger = getLogger(__name__)

        self._fancyOutput: Optional[HDIUtilPuppetStringOutput] = None

    def createDiskImage(self):

        appName: str  = self._environment.applicationName
        distDir: Path = self._environment.distDirectory

        tempStageDir: Path = Path('/tmp') / f'{appName}{STAGE_SUFFIX}'

        # Clean up temp staging directory before starting any operation
        self._removeDirectoryTree(tempStageDir)

        appPath: Path = self._computePath(distDir=distDir, baseName=appName, suffix=APP_SUFFIX)
        dmgPath: Path = self._computePath(distDir=distDir, baseName=appName, suffix=DMG_SUFFIX)

        if appPath.exists() is False:
            raise ClickException(f'Application bundle `{appPath}` does not exist')

        # Remove existing dmg if present
        if dmgPath.exists() is True:
            dmgPath.unlink()

        # Create staging directory in /tmp and copy .app bundle
        tempStageDir.mkdir(parents=True, exist_ok=True)
        stagedAppPath: Path = tempStageDir / f'{appName}.app'
        secho('Stage the app')
        copytree(appPath, stagedAppPath, symlinks=True)
        secho('Staging complete')

        # Create /Applications symlink for drag-and-drop installer UX
        applicationsSymlink: Path = tempStageDir / 'Applications'
        symlink('/Applications', applicationsSymlink)

        self._runDiskImageCreationCLI(appName=appName, tempStageDir=tempStageDir, dmgPath=dmgPath)

        # Cleanup staging directory in /tmp using pathlib
        self._removeDirectoryTree(tempStageDir)

        if dmgPath.exists() is False:
            raise ClickException(f'Error: Failed to create `.dmg` file at `{dmgPath}`')

    def _runDiskImageCreationCLI(self, appName: str, tempStageDir: Path, dmgPath: Path):
        """

        Args:
            appName:
            tempStageDir:
            dmgPath:
        """
        # Build compressed UDZO .dmg using native macOS hdiutil
        hdiUtilCmd: List[str] = STANDARD_HDI_UTIL_OPTIONS + [
            '-srcfolder', str(tempStageDir),
            '-volname', appName,
            str(dmgPath)
        ]
        if self._environment.verbose:
            hdiUtilCmd.append('-verbose')
        else:
            hdiUtilCmd.append('-puppetstrings')

        if self._environment.verbose:
            secho('Start the disk image creation')

        hdiProcess: subProcessPOpen[str]
        with subProcessPOpen(
            hdiUtilCmd,
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            bufsize=1
        ) as hdiProcess:
            if hdiProcess.stdout is not None:
                cmdOutput: str
                for cmdOutput in hdiProcess.stdout:
                    self._displayHDIUtilOutput(cmdOutput=cmdOutput)

            returnCode: int = hdiProcess.wait()
            if returnCode != 0:
                raise ClickException(f'`hdiutil` failed with return code {returnCode}')

    def _removeDirectoryTree(self, targetPath: Path):
        """
        Recursively deletes a directory tree using pathlib.Path.

        BTW. I hate recursion

        Args:
            targetPath: The directory or file path to recursively remove
        """
        if targetPath.exists() is False:
            return

        if targetPath.is_symlink() is True or targetPath.is_file() is True:
            targetPath.unlink()
            return

        for itemPath in targetPath.iterdir():
            if itemPath.is_symlink() is True or itemPath.is_file() is True:
                if self._environment.verbose:
                    secho(f'Removing: {itemPath}')
                itemPath.unlink()
            elif itemPath.is_dir() is True:
                if self._environment.verbose:
                    secho(f'Remove subdirectory: {itemPath}')
                self._removeDirectoryTree(itemPath)

        targetPath.rmdir()

    def _displayHDIUtilOutput(self, cmdOutput: str):

        if self._environment.verbose:
            secho(cmdOutput, nl=False)
        else:
            if self._fancyOutput is None:
                self._fancyOutput = HDIUtilPuppetStringOutput()
            assert self._fancyOutput is not None, 'FancyOutput instance must be initialized'
            self._fancyOutput.updateProgress(cmdOutput=cmdOutput)
