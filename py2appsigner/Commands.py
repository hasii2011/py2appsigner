
import logging
import logging.config

from json import load as jsonLoad

from importlib.resources import files
from importlib.abc import Traversable

from click import command
from click import group
from click import pass_context
from click import pass_obj
from click import version_option
from click import option

from py2appsigner import __version__ as version

from py2appsigner.ApplicationNotarize import ApplicationNotarize
from py2appsigner.ApplicationSign import ApplicationSign
from py2appsigner.ApplicationStaple import ApplicationStaple
from py2appsigner.ApplicationVerify import ApplicationVerify
from py2appsigner.Notary import Notary
from py2appsigner.environment.BasicEnvironment import BasicEnvironment

from py2appsigner.environment.Environment import Environment
from py2appsigner.ZipSign import ZipSign
from py2appsigner.environment.NotaryEnvironment import NotaryEnvironment


RESOURCES_PACKAGE_NAME:       str = 'py2appsigner.resources'
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

VERBOSE_OPTION_HELP: str = 'Include this option to instruct command to echo the underlying CLI output'


def setUpLogging():
    """
    """
    traversable: Traversable = files(RESOURCES_PACKAGE_NAME) / JSON_LOGGING_CONFIG_FILENAME

    loggingConfigFilename: str = str(traversable)

    with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False


@group
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--python-version',    '-p', required=True,  help='Identify the python version')
@option('--identity',          '-i', required=False, help='Code signing identity')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
@pass_context
def py2appSign(ctx, python_version: str, application_name: str, projects_base: str = '', project_directory: str = '', identity: str = '', verbose: bool = False):
    """
    Specify a python version that the py2app application is using.
    \b

    Specify the application name created by py2app
    \b

    The environment variable for projects base is 'PROJECTS_BASE'.  This is a fully qualified
    directory name.
    \b

    The environment variable for project directory is 'PROJECT'.  This is just the
    simple project directory name.

    identity -- For code signing, a digital identity must be stored in a keychain that is on the calling user's keychain search list.
    if not specified then the value must be set in the 'IDENTITY' environment variable
    \b
    """
    setUpLogging()

    environment: Environment     = Environment(pythonVersion=python_version,
                                               applicationName=application_name,
                                               projectsBase=projects_base,
                                               projectDirectory=project_directory,
                                               identity=identity,
                                               verbose=verbose)

    ctx.obj = environment


@py2appSign.command()
@pass_obj
def zipSign(environment: Environment):

    zipsign: ZipSign = ZipSign(environment=environment)
    zipsign.execute()


@py2appSign.command()
@option('--fix-lib', '-f', required=False, is_flag=True, help='Fix broken library ')
@pass_obj
def appSign(environment: Environment, fix_lib: bool = False):
    # noinspection SpellCheckingInspection
    """
    fix-lib gets the following dynamic library from Homebrew;  And copies it into the
    Python virtual environment;  Works only on Apple Silicon OS X
    and with Homebrew installed

    See: https://stackoverflow.com/questions/62095338/py2app-fails-macos-signing-on-liblzma-5-dylib

    On Intel OS X

    /usr/local/Cellar/xz/5.2.5/lib/liblzma.5.dylib

    Apple Silicon

    /opt/homebrew/opt/xz/lib/liblzma.5.dylib
    """
    applicationSign: ApplicationSign = ApplicationSign(environment=environment, fixLib=fix_lib)
    applicationSign.execute()


@command
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
def appNotarize(application_name: str, projects_base: str = '', project_directory: str = '', verbose: bool = False):
    """
    Specify the application name created by py2app
    \b

    The environment variable for projects base is 'PROJECTS_BASE'.  This is a fully qualified
    directory name.
    \b

    The environment variable for project directory is 'PROJECT'.  This is just the
    simple project directory name.

    Assumes the developer stored application specific ID with the name 'APP_PASSWORD'

    """
    environment: BasicEnvironment = BasicEnvironment(applicationName=application_name, projectsBase=projects_base, projectDirectory=project_directory, verbose=verbose)

    applicationNotarize: ApplicationNotarize = ApplicationNotarize(environment=environment)
    applicationNotarize.execute()


@command
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
def appStaple(application_name: str, projects_base: str = '', project_directory: str = '', verbose: bool = False):

    environment: Environment     = Environment(pythonVersion='',                    # Not Needed
                                               applicationName=application_name,
                                               projectsBase=projects_base,
                                               projectDirectory=project_directory,
                                               identity='',                         # Not needed
                                               verbose=verbose)

    applicationStaple: ApplicationStaple = ApplicationStaple(environment=environment)
    applicationStaple.execute()


@command()
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
def appVerify(application_name: str, projects_base: str = '', project_directory: str = '', verbose: bool = False):

    environment: Environment     = Environment(pythonVersion='',                    # Not Needed
                                               applicationName=application_name,
                                               projectsBase=projects_base,
                                               projectDirectory=project_directory,
                                               identity='',                         # Not needed
                                               verbose=verbose)

    applicationVerify: ApplicationVerify = ApplicationVerify(environment=environment)
    applicationVerify.execute()


@group
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--keychain-profile', '-p', required=False, help='Keychain profile name storing Notary Tool Application Id')
@pass_context
def notaryTool(ctx, keychain_profile: str):
    """
    Use this command to request information about a specific submission or a history of all
    your submissions.

    The default keychain profile name is 'NOTARY_TOOL_APP_ID'
    """
    notaryEnvironment: NotaryEnvironment = NotaryEnvironment()
    if keychain_profile is not None:
        notaryEnvironment.keyChainProfile = keychain_profile
    ctx.obj = notaryEnvironment


@notaryTool.command()
@pass_obj
def history(notaryEnvironment: NotaryEnvironment):
    """
    """
    notary: Notary = Notary(notaryEnvironment=notaryEnvironment)
    notary.history()


@notaryTool.command()
@option('--submission-id', '-i', required=True, help='Submission ID returned from a previous invocation of `appNotarize`')
@pass_obj
def information(notaryEnvironment: NotaryEnvironment, submission_id: str):
    """
    """
    notary: Notary = Notary(notaryEnvironment=notaryEnvironment)
    notary.information(submissionId=submission_id)


if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    """
    py2appSign(['--python-version', '3.10', '-d', 'pyut', '--application-name', 'pyut', 'zipsign'])
    py2appSign(['--python-version', '3.10', '-d', 'pyut', '--application-name', 'pyut', 'appsign'])
    appNotarize(['-d', 'pyut', '--application-name', 'pyut', '--verbose'])
    appStaple(['-d', 'pyut', '--application-name', 'pyut', '--verbose'])
    notaryTool(['information', '-i', '5f57fc1e-23d3-42ab-b0ad-ec1d2635c4ad'])
    notaryTool(['--keychain-profile', 'NOTARY_TOOL_APP_ID', 'history'])
    """
    py2appSign(['--python-version', '3.11', '-d', 'pyut', '--application-name', 'pyut', '--verbose', 'appsign'])
