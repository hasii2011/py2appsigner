from logging import Logger
from logging import getLogger

from os import symlink
from os import linesep as osLineSep

from pathlib import Path

from shutil import copytree

from subprocess import CompletedProcess
from subprocess import run as subProcessRun

from click import ClickException
from click import secho

from py2appsigner.environment.DiskImageEnvironment import DiskImageEnvironment

APP_SUFFIX: str = 'app'
DMG_SUFFIX: str = 'dmg'
STAGE_SUFFIX: str = '_dmg_stage'

class DiskImageCreate:
    def __init__(self, environment: DiskImageEnvironment):

        self.logger: Logger = getLogger(__name__)

        self._environment: DiskImageEnvironment = environment

    def createDiskImage(self):

        appName:          str  = self._environment.applicationName
        distDir:          Path = self._environment.distDirectory
        # projectsBase:     Path = Path(self._environment.projectsBase)
        # projectDirectory: str  = self._environment.projectDirectory

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

        # Build compressed UDZO .dmg using native macOS hdiutil
        hdiUtilCmd: list[str] = [
            'hdiutil', 'create',
            '-volname', appName,
            '-srcfolder', str(tempStageDir),
            '-ov',
            '-format', 'UDZO',
            '-verbose',
            str(dmgPath)
        ]
        secho(f'Start the disk image creation')
        hdiUtilResult: CompletedProcess[str] = subProcessRun(hdiUtilCmd, check=True, capture_output=True, text=True)
        secho(f'{osLineSep}{hdiUtilResult.stdout}')

        # Cleanup staging directory in /tmp using pathlib
        self._removeDirectoryTree(tempStageDir)

        assert dmgPath.exists(), f'Error: Failed to create `.dmg` file at `{dmgPath}`'
        secho(f'Successfully created DMG at: {dmgPath}')

    def signDiskImage(self):
        pass

    def _computePath(self, distDir: Path, baseName: str, suffix: str) -> Path:

        projectsBase:     Path = Path(self._environment.projectsBase)
        projectDirectory: str  = self._environment.projectDirectory

        fullPath: Path
        fullName: str = f'{baseName}.{suffix}'
        if distDir.is_absolute():
            fullPath = distDir / fullName
        else:
            fullProjectPath: Path = projectsBase / projectDirectory
            fullPath = fullProjectPath / distDir / fullName

        return fullPath

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
