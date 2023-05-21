
from logging import Logger
from logging import getLogger

from os import sep as osSep
from os import system as osSystem
from pathlib import Path

from click import secho

from py2appsigner.CommandBase import CommandBase
from py2appsigner.Environment import Environment

ZIP_DIRECTORY_SNIPPET: str = '/Contents/Resources/lib'
TMP_DIR_PATH:          str = '/tmp'
BUILD_DIR:             str = '/dist/'

CODE_SIGN_TOOL:            str = 'codesign'
DITTO_TOOL:                str = '/usr/bin/ditto'

COPY_OPTIONS_VERBOSE:          str = '-vp'
COPY_OPTIONS_QUIET:            str = '-p'
REMOVE_OPTIONS_VERBOSE:        str = '-vrf'
REMOVE_OPTIONS_QUIET:          str = '-rf'
CODE_SIGN_OPTIONS_VERBOSE:     str = '--force --timestamp --options=runtime -v '
CODE_SIGN_OPTIONS_QUIET:       str = '--force --timestamp --options=runtime'
DITTO_EXTRACT_OPTIONS_VERBOSE: str = '-x -k -v'
DITTO_EXTRACT_OPTIONS_QUIET:   str = '-x -k'
DITTO_CREATE_OPTIONS_VERBOSE:  str = '-c -k -v'
DITTO_CREATE_OPTIONS_QUIET:    str = '-c -k'


class ZipSign(CommandBase):

    def __init__(self, environment: Environment):

        super().__init__(environment=environment)

        self.logger: Logger = getLogger(__name__)

    def execute(self):
        self.logger.debug(f'{self._environment.pythonVersion=} {self._environment.applicationName=}')

        fullPath:        str = f'{self._environment.projectsBase}/{self._environment.projectDirectory}'
        pythonVersion:   str = self._removeDecimalSeparator(self._environment.pythonVersion)
        applicationName: str = f'{fullPath}{BUILD_DIR}{self._environment.applicationName}.app'

        originalZipDir: str = f'{applicationName}{ZIP_DIRECTORY_SNIPPET}'
        unzipDir:       str = f'{TMP_DIR_PATH}/python{pythonVersion}'
        zipName:        str = f'python{pythonVersion}.zip'

        self._cleanupTemporaryDirectory(unzipDir=unzipDir, zipName=zipName)
        self._getUnsignedZipCopy(originalZipDir=originalZipDir, zipName=zipName)
        self._unzipCopy(unzipDir=unzipDir, zipName=zipName)
        self._signLibs(unzipDir=unzipDir)
        self._removeOldUnSignedZip(zipName=zipName)
        self._recreateSignedZip(unzipDir=unzipDir, zipName=zipName)
        self._moveSignedZipBack(originalZipDir=originalZipDir, zipName=zipName)

    def _cleanupTemporaryDirectory(self, unzipDir: str, zipName: str):
        # rm - rf "${TEMP_DIR}/${ZIP_NAME}"
        # rm - rf ${PYTHON_UNZIP_DIR}

        deleteUnzipDir: str = f'rm -rf {unzipDir}'
        self._runCommand(deleteUnzipDir)
        deleteZipCopy: str = f'rm -rf {TMP_DIR_PATH}{osSep}{zipName}'
        self._runCommand(deleteZipCopy)

    def _getUnsignedZipCopy(self, originalZipDir: str, zipName: str):
        # echo "Get copy of unsigned zip file"
        # cp - vp ${PYTHON_ZIP} ${TEMP_DIR}
        # export PYTHON_ZIP="${ORIGINAL_ZIP_DIR}/${ZIP_NAME}"
        # export PYTHON_UNZIP_DIR="${TEMP_DIR}/${UNZIP_DIR}"
        pythonZip: str = f'{originalZipDir}/{zipName}'

        options:  str = self._getToolOptions(verboseOptions=COPY_OPTIONS_VERBOSE, quiteOptions=COPY_OPTIONS_QUIET)
        makeCopy: str = f'cp {options} {pythonZip} {TMP_DIR_PATH}'

        self._runCommand(makeCopy)

    def _unzipCopy(self, unzipDir: str, zipName: str):
        # echo "Unzip it"
        # /usr/bin/ditto -v -x -k "${TEMP_DIR}/${ZIP_NAME}" "${TEMP_DIR}/${UNZIP_DIR}"
        options: str = self._getToolOptions(verboseOptions=DITTO_EXTRACT_OPTIONS_VERBOSE, quiteOptions=DITTO_EXTRACT_OPTIONS_QUIET)
        unZipIt: str = f'{DITTO_TOOL} {options} {TMP_DIR_PATH}/{zipName} {unzipDir}'

        self._runCommand(unZipIt)

    def _signLibs(self, unzipDir: str):
        # noinspection SpellCheckingInspection
        """
        export  OPTIONS = "--force --verbose --timestamp --options=runtime "
        find "${PYTHON_UNZIP_DIR}/PIL/.dylibs" -iname '*.dylib' |

        Args:
            unzipDir:
        """
        # noinspection SpellCheckingInspection
        p:        Path = Path(f'{unzipDir}/PIL/.dylibs')
        identity: str  = self._environment.identity
        options:  str  = self._getToolOptions(verboseOptions=CODE_SIGN_OPTIONS_VERBOSE, quiteOptions=CODE_SIGN_OPTIONS_QUIET)
        for lib in p.iterdir():

            signIt: str = f'{CODE_SIGN_TOOL} --sign "{identity}" {options} {lib}'
            self._runCommand(signIt)

    def _removeOldUnSignedZip(self, zipName: str):
        options:    str  = self._getToolOptions(verboseOptions=REMOVE_OPTIONS_VERBOSE, quiteOptions=REMOVE_OPTIONS_QUIET)
        path:       Path = Path(TMP_DIR_PATH) / zipName
        removeCopy: str  = f'rm {options} {path}'

        self._runCommand(removeCopy)

    def _recreateSignedZip(self, unzipDir: str, zipName: str):
        options:    str = self._getToolOptions(verboseOptions=DITTO_CREATE_OPTIONS_VERBOSE, quiteOptions=DITTO_CREATE_OPTIONS_QUIET)
        tmpDirPath: Path = Path(TMP_DIR_PATH) / zipName
        zipIt:   str = f'{DITTO_TOOL} {options} {unzipDir} {tmpDirPath}'

        self._runCommand(zipIt)

    def _moveSignedZipBack(self, originalZipDir: str, zipName: str):

        signedZip: Path = Path(TMP_DIR_PATH) / zipName

        options:   str  = self._getToolOptions(verboseOptions=COPY_OPTIONS_VERBOSE, quiteOptions=COPY_OPTIONS_QUIET)

        moveItBack: str = f'cp {options} {signedZip} {originalZipDir}'

        self._runCommand(moveItBack)

    def _getToolOptions(self, verboseOptions: str, quiteOptions: str) -> str:
        if self._environment.verbose is True:
            return verboseOptions
        else:
            return quiteOptions

    def _runCommand(self,  command: str):
        status: int = osSystem(command)
        self._echoCommandAndStatus(command, status)

    def _echoCommandAndStatus(self, command: str, status: int):
        if self._environment.verbose is True:
            secho(command)
            secho(f'{status=}')

    def _removeDecimalSeparator(self, pythonVersion: str):
        return pythonVersion.replace('.', '')

    # def _echo(self, message: str):
    #     if self._environment.verbose is True:
    #         secho(message)
