
from logging import Logger
from logging import getLogger

from os import sep as osSep
from os import system as osSystem

from click import secho

from py2appsigner.CommandBase import CommandBase
from py2appsigner.Environment import Environment

ZIP_DIRECTORY_SNIPPET: str = '/Contents/Resources/lib'
TMP_DIR_PATH:          str = '/tmp'
BUILD_DIR:             str = '/dist/'


class ZipSign(CommandBase):

    def __init__(self, environment: Environment):

        super().__init__(environment=environment)

        self.logger: Logger = getLogger(__name__)

    def execute(self):
        self.logger.debug(f'{self._environment.pythonVersion=} {self._environment.applicationName=}')

        fullPath:        str = f'{self._environment.projectsBase}/{self._environment.projectDirectory}'
        pythonVersion:   str = self._removeDots(self._environment.pythonVersion)
        applicationName: str = f'{fullPath}{BUILD_DIR}{self._environment.applicationName}.app'

        originalZipDir: str = f'{applicationName}{ZIP_DIRECTORY_SNIPPET}'
        unzipDir:       str = f'python{pythonVersion}'
        zipName:        str = f'python{pythonVersion}.zip'

        self.logger.debug(f'{unzipDir=} {zipName=}')

        self._cleanupTemporaryDirectory(unzipDir=unzipDir, zipName=zipName)
        self._getUnsignedCopy(originalZipDir=originalZipDir, zipName=zipName)

    def _removeDots(self, pythonVersion: str):
        return pythonVersion.replace('.', '')

    def _cleanupTemporaryDirectory(self, unzipDir: str, zipName: str):
        # rm - rf "${TEMP_DIR}/${ZIP_NAME}"
        # rm - rf ${PYTHON_UNZIP_DIR}

        deleteUnzipDir: str = f'rm -rf {TMP_DIR_PATH}{osSep}{unzipDir}'
        self._echo(deleteUnzipDir)
        status: int = osSystem(deleteUnzipDir)
        secho(f'{status=}')

        deleteZipCopy: str = f'rm -rf {TMP_DIR_PATH}{osSep}{zipName}'
        self._echo(deleteZipCopy)
        status = osSystem(deleteUnzipDir)
        secho(f'{status=}')

    def _getUnsignedCopy(self, originalZipDir: str, zipName: str):
        # echo "Get copy of unsigned zip file"
        # cp - vp ${PYTHON_ZIP} ${TEMP_DIR}
        # export PYTHON_ZIP="${ORIGINAL_ZIP_DIR}/${ZIP_NAME}"
        # export PYTHON_UNZIP_DIR="${TEMP_DIR}/${UNZIP_DIR}"
        pythonZip: str = f'{originalZipDir}/{zipName}'
        makeCopy: str = f'cp -vp {pythonZip} {TMP_DIR_PATH}'
        self._echo(makeCopy)
        status = osSystem(makeCopy)
        secho(f'{status=}')

    def _echo(self, message: str):
        if self._environment.verbose is True:
            secho(message)
