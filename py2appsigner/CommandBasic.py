from abc import ABCMeta
from logging import Logger
from logging import getLogger

from sys import stdout

from subprocess import run as subProcessRun
from subprocess import check_call as subProcessCheckCall

from subprocess import STDOUT

from abc import abstractmethod

from click import secho

from py2appsigner.BaseCommand import BaseCommand
from py2appsigner.environment.BasicEnvironment import BasicEnvironment

BUILD_DIR:  str = '/dist/'
ZIP_SUFFIX: str = 'zip'

CODE_SIGN_TOOL:            str = '/usr/bin/codesign'
DITTO_TOOL:                str = '/usr/bin/ditto'

COPY_OPTIONS_VERBOSE:          str = '-vp'
COPY_OPTIONS_QUIET:            str = '-p'
REMOVE_OPTIONS_VERBOSE:        str = '-vrf'
REMOVE_OPTIONS_QUIET:          str = '-rf'
CODE_SIGN_OPTIONS_VERBOSE:     str = '-vvvv --force --timestamp --options=runtime'
CODE_SIGN_OPTIONS_QUIET:       str = '--force --timestamp --options=runtime'


class MetaBaseCommand(ABCMeta, type(BaseCommand)):      # type: ignore
    """
    I have know idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class CommandBasic(BaseCommand):
    __metaclass = MetaBaseCommand

    def __init__(self, environment: BasicEnvironment):

        super().__init__(verbose=environment.verbose)
        self._basicEnvironment: BasicEnvironment = environment

        self.baseLogger: Logger = getLogger(__name__)

        self._fullPath:        str = f'{self._basicEnvironment.projectsBase}/{self._basicEnvironment.projectDirectory}'
        self._applicationName: str = f'{self._fullPath}{BUILD_DIR}{self._basicEnvironment.applicationName}.app'

    @abstractmethod
    def execute(self):
        pass
