from typing import List

from logging import Logger
from logging import getLogger

from pathlib import Path

from click import secho

from tqdm import tqdm

from py2appsigner.CommandBasic import CODE_SIGN_OPTIONS_QUIET
from py2appsigner.CommandBasic import CODE_SIGN_OPTIONS_VERBOSE
from py2appsigner.CommandBasic import CODE_SIGN_TOOL
from py2appsigner.CommandBasic import COPY_OPTIONS_VERBOSE
from py2appsigner.CommandBasic import COPY_OPTIONS_QUIET
from py2appsigner.CommandBasic import REMOVE_OPTIONS_QUIET
from py2appsigner.CommandBasic import REMOVE_OPTIONS_VERBOSE

from py2appsigner.CommandExtended import CommandExtended

from py2appsigner.Common import PROGRESS_BAR_UNITS

from py2appsigner.environment.Environment import Environment


# noinspection SpellCheckingInspection
"""
# https://stackoverflow.com/questions/62095338/py2app-fails-macos-signing-on-liblzma-5-dylib
#
# export GOOD_LIB='/usr/local/Cellar/xz/5.2.5/lib/liblzma.5.dylib'
# if you are on the new Apple Silicon homebrew is now here:
"""

# noinspection SpellCheckingInspection
GOOD_LIB: str = '/opt/homebrew/opt/xz/lib/liblzma.5.dylib'

CLEAN_UP_CRUD: List[str] = [
    'Contents/Resources/lib/python3.10/todoist/.DS_Store',
    'Contents/Resources/lib/python3.10/numpy/f2py/tests/src/assumed_shape/.f2py_f2cmap',
    'Contents/Resources/lib/python3.10/site.pyo'
]

SHARED_OBJECT_LIBRARY_WILDCARD:       str = '*.so'
MACH_OBJECT_DYNAMIC_LIBRARY_WILDCARD: str = '*.dylib'

PRE_FRAMEWORK_PATH: str = '/Contents/Frameworks/Python.framework/Versions'


class ApplicationSign(CommandExtended):

    def __init__(self, environment: Environment, fixLib: bool):

        super().__init__(environment=environment)
        self.logger: Logger = getLogger(__name__)

        self._fixLib: bool = fixLib

        self._codeSignCommand: str = self._constructCodeSignCommand()

    def execute(self):

        self._fixLibrary()
        self._cleanupCrud()
        self._signFrameworks()
        self._signLibraries()
        self._signPythonApp()
        self._signApplication()

    def _fixLibrary(self):

        if self._fixLib is True:
            directoryToOverWrite: str = f'{self._applicationName}/Contents/Frameworks'
            options: str = self._getToolOptions(verboseOptions=COPY_OPTIONS_VERBOSE, quietOptions=COPY_OPTIONS_QUIET)
            overwrite: str = f'cp {options} {GOOD_LIB} {directoryToOverWrite}'
            self._runCommand(overwrite)

    def _cleanupCrud(self):
        """
        Ugh code signing will be the death of me
        Either invalid links or something code signing or verifying complains about
        """
        removeOptions: str = self._getToolOptions(verboseOptions=REMOVE_OPTIONS_VERBOSE, quietOptions=REMOVE_OPTIONS_QUIET)
        for partialCrud in CLEAN_UP_CRUD:
            fullCrud: Path = Path(self._applicationName) / partialCrud

            removeIt: str = f'rm {removeOptions} {fullCrud}'

            self._runCommand(removeIt)

    def _signLibraries(self):
        # noinspection SpellCheckingInspection
        """
        find "${FULL_APP_NAME}" -iname '*.so' -or -iname '*.dylib' |
            while read libfile; do
                codesign --sign "${IDENTITY}" ${OPTIONS} "${libfile}" >> ${LOGFILE} 2>&1 ;
            done;
        """
        p: Path = Path(self._applicationName)

        secho(f'Sign Libraries - {SHARED_OBJECT_LIBRARY_WILDCARD}')
        soLibs: List[Path] = sorted(p.rglob(f'{SHARED_OBJECT_LIBRARY_WILDCARD}'))

        if self.verbose is True:
            self._verboseSignSOLibraries(soLibs)
        else:
            self._progressBarSignSOLibraries(soLibs)

        secho(f'Sign Libraries - {MACH_OBJECT_DYNAMIC_LIBRARY_WILDCARD}')
        dyLibs: List[Path] = sorted(p.rglob(f'{MACH_OBJECT_DYNAMIC_LIBRARY_WILDCARD}'))

        if self.verbose is True:
            self._verboseSignDynamicLibraries(dyLibs)
        else:
            self._progressBarSignDynamicLibraries(dyLibs)

    def _signFrameworks(self):
        """
         Assumes Xcode 13 is installed
        """
        #
        # codesign --sign "${IDENTITY}" ${OPTIONS} "${FULL_APP_NAME}/Contents/Frameworks/Python.framework/Versions/3.10/Python"
        #
        secho('Sign Framework')

        framework:     str = (
            f'{self._applicationName}/{PRE_FRAMEWORK_PATH}/{self._pythonVersion}/Python'
        )
        signFramework: str = f'{self._codeSignCommand} {framework}'
        self._runCommand(signFramework)

    def _signPythonApp(self):
        # codesign --sign "${IDENTITY}" ${OPTIONS} "${FULL_APP_NAME}/Contents/MacOS/python"
        pythonApp:  str = f'{self._applicationName}/Contents/MacOS/python'
        signPython: str = f'{self._codeSignCommand} {pythonApp}'

        self._runCommand(signPython)

    def _signApplication(self):
        # codesign --sign "${IDENTITY}" ${OPTIONS} "${FULL_APP_NAME}/Contents/MacOS/${APPLICATION_NAME}"
        application:     str = f'{self._applicationName}/Contents/MacOS/{self._extendedEnvironment.applicationName}'
        signApplication: str = f'{self._codeSignCommand} {application}'

        self._runCommand(signApplication)

    def _constructCodeSignCommand(self) -> str:
        """
        It is up to the caller to append it item that needs to be signed to code sign CLI

        codesign --sign "${IDENTITY}" ${OPTIONS} <CALLER APPENDS TARGET>

        Returns:  The code CLI to invoke with all options correctly set;
        """
        options:  str = self._getToolOptions(verboseOptions=CODE_SIGN_OPTIONS_VERBOSE, quietOptions=CODE_SIGN_OPTIONS_QUIET)
        identity: str = self._extendedEnvironment.identity

        codeSignCommand: str = f'{CODE_SIGN_TOOL} --sign "{identity}" {options}'

        return codeSignCommand

    def _verboseSignSOLibraries(self, soLibs: List[Path]):
        for lib in soLibs:
            signSo: str = f'{self._codeSignCommand} {lib}'
            self._runCommand(signSo)

    def _progressBarSignSOLibraries(self, soLibs: List[Path]):
        pbar: tqdm = tqdm(soLibs, unit=PROGRESS_BAR_UNITS)
        for lib in pbar:
            path: Path = Path(lib)
            pbar.set_description(f'Processing {path.name}')
            signSo: str = f'{self._codeSignCommand} {lib}'
            self._runCommand(signSo)

    def _verboseSignDynamicLibraries(self, dyLibs: List[Path]):
        for lib in dyLibs:
            signDyLibs: str = f'{self._codeSignCommand} {lib}'
            self._runCommand(signDyLibs)

    def _progressBarSignDynamicLibraries(self, dyLibs: List[Path]):
        pbar: tqdm = tqdm(dyLibs, unit=PROGRESS_BAR_UNITS)
        for dylib in pbar:
            path: Path = Path(dylib)
            pbar.set_description(path.name)
            signDyLibs: str = f'{self._codeSignCommand} {dylib}'
            self._runCommand(signDyLibs)
