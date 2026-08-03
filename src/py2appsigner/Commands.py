
import logging
import logging.config

from json import loads as jsonLoads

from importlib.resources import files
from importlib.resources.abc import Traversable

from pathlib import Path

from os import linesep as osLineSep

from click import group
from click import secho
from click import clear
from click import option
from click import command
from click import pass_obj
from click import pass_context
from click import version_option

from py2appsigner import __version__ as version

from py2appsigner.ApplicationNotarize import ApplicationNotarize
from py2appsigner.ApplicationSign import ApplicationSign
from py2appsigner.ApplicationStaple import ApplicationStaple
from py2appsigner.ApplicationVerify import ApplicationVerify

from py2appsigner.Notary import Notary

from py2appsigner.diskimage.DiskImageSign import DiskImageSign
from py2appsigner.diskimage.DiskImageCreate import DiskImageCreate
from py2appsigner.diskimage.DiskImageStaple import DiskImageStaple
from py2appsigner.diskimage.DiskImageVerify import DiskImageVerify
from py2appsigner.diskimage.DiskImageNotarize import DiskImageNotarize

from py2appsigner.environment.Environment import Environment
from py2appsigner.environment.BasicEnvironment import BasicEnvironment
from py2appsigner.environment.NotaryEnvironment import NotaryEnvironment
from py2appsigner.environment.DiskImageEnvironment import DiskImageEnvironment

from py2appsigner.ZipSign import ZipSign


RESOURCES_PACKAGE_NAME:       str = 'py2appsigner.resources'
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

VERBOSE_OPTION_HELP: str = 'Include this option to instruct the command to echo the underlying CLI output'

def setUpLogging():
    """
    """
    traversable: Traversable = files(RESOURCES_PACKAGE_NAME) / JSON_LOGGING_CONFIG_FILENAME

    loggingConfigContent:    str  = traversable.read_text(encoding='utf-8')
    configurationDictionary: dict = jsonLoads(loggingConfigContent)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False

@group(name='py2AppSign')
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--python-version',    '-p', required=True,  help='Identify the python version')
@option('--identity',          '-i', required=False, help='Code signing identity')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
@pass_context
def py2AppSign(ctx, python_version: str, application_name: str, projects_base: str = '', project_directory: str = '', identity: str = '', verbose: bool = False):
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


@py2AppSign.command(name='zipSign')
@option('--delete-part-files', '-d', required=False, is_flag=True, help='Remove opaque .part files')
@pass_obj
def zipSign(environment: Environment, delete_part_files: bool = False):
    """
    Signs the internal python zipfile;  May optionally remove some bad files in test/zipimport_data
    """
    zipsign: ZipSign = ZipSign(environment=environment, deletePartFiles=delete_part_files)
    zipsign.execute()


@py2AppSign.command(name='appSign')
@option('--fix-lib',      '-l', required=False, is_flag=True, help='Fix broken library')
@option('--fix-sym-link', '-s', required=False, is_flag=True, help='Fix invalid symbolic link')
@pass_obj
def appSign(environment: Environment, fix_lib: bool = False, fix_sym_link: bool = False):
    """
    fix-lib gets the following dynamic library from Homebrew;  And copies it into the
    application;  Works only on Apple Silicon OS X
    and with Homebrew installed

    See: https://stackoverflow.com/questions/62095338/py2app-fails-macos-signing-on-liblzma-5-dylib

    On Intel OS X

    /usr/local/Cellar/xz/5.2.5/lib/liblzma.5.dylib

    Apple Silicon

    /opt/homebrew/opt/xz/lib/liblzma.5.dylib

    --fix-sym-link removes the following symbolic link from the application binary before signing

     <application>.app/Contents/Resources/lib/python<python version>/site.pyo

     Leaving this file in place with a signed and notarized application causes it to
     fail the appVerify phase and renders the binary unusable

    """
    applicationSign: ApplicationSign = ApplicationSign(environment=environment, fixLib=fix_lib, fixSymLink=fix_sym_link)
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

    Assumes the developer stored application specific ID in the Apple key chain
     with the name 'NOTARY_TOOL_APP_ID'

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

@command(name='py2AppSigner')
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
def py2AppSigner():
    clear()
    secho('Example Commands:')
    secho('     py2appSign -p 3.11 -d umldiagrammer -a UmlDiagrammer  --verbose zipsign')
    secho('     py2appSign -p 3.11 -d umldiagrammer -a UmlDiagrammer  --verbose appsign')
    secho('')
    secho('     appNotarize -d umldiagrammer -a UmlDiagrammer --verbose')
    secho('     appStaple   -d umldiagrammer -a UmlDiagrammer --verbose')
    secho('     appVerify   -d umldiagrammer -a UmlDiagrammer')
    secho('')
    secho('     notaryTool history')
    secho('     notaryTool -p NOTARY_TOOL_APP_ID history')
    secho('     notaryTool information -i <submission id>')
    secho('     notaryTool -p NOTARY_TOOL_APP_ID information -i <submission id>')
    secho('')
    secho('     dmgTool -a UmlDiagrammer -d dist createDmg')
    secho('     dmgTool -a UmlDiagrammer -d dist signDmg')
    secho('     dmgNotarize -d umldiagrammer -a UmlDiagrammer --verbose')


@group(name='dmgTool')
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name', '-a', 'applicationName', required=True, type=str,  help='The application name that py2app built')
@option('--dist-directory',   '-d', 'distDirectory',   required=True, type=Path, help='Path to dist directory')
@option('--verbose',           '-v', required=False,   is_flag=True,             help='Prepare to be overwhelmed')
@pass_context
def dmgTool(ctx, applicationName: str, distDirectory: Path, verbose: bool):
    """
    This subcommand createDmg, creates a .dmg file.  The above assumes that the macOS app exists in the dist directory.
    The verbose option is extremely verbose.  The *dist* option can be a fully qualified directory.  If it is not,
    this command assumes it is in ${PROJECTS_BASE}/${PROJECT}.

    The subcommand signDmg, signs the .dmg file created by the `createDmg` subcommand.

    """
    if verbose:
        secho(f'Application Name: `{applicationName}`{osLineSep}distDirectory: `{str(distDirectory)}`')
    setUpLogging()

    environment: DiskImageEnvironment = DiskImageEnvironment(applicationName=applicationName, distDirectory=distDirectory, verbose=verbose)
    ctx.obj = environment


@dmgTool.command(name='createDmg')
@pass_obj
def createDmg(environment: DiskImageEnvironment):

    if environment.verbose:
        secho(f'{environment=}')

    diskImageCreate: DiskImageCreate = DiskImageCreate(environment=environment)
    diskImageCreate.createDiskImage()


@dmgTool.command(name='signDmg')
@pass_obj
def signDmg(environment: DiskImageEnvironment):

    if environment.verbose:
        secho(f'Environment: {environment}')

    diskImageSign: DiskImageSign = DiskImageSign(environment=environment)
    diskImageSign.signDiskImage()

@command
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
def dmgNotarize(application_name: str, projects_base: str = '', project_directory: str = '', verbose: bool = False):
    """
    Specify the disk image name created by dmgTool ... createDmg
    \b

    The environment variable for projects base is 'PROJECTS_BASE'.  This is a fully qualified
    directory name.
    \b

    The environment variable for project directory is 'PROJECT'.  This is just the
    simple project directory name.

    Assumes the developer stored the application specific ID in the macOS keychain
    with the name 'NOTARY_TOOL_APP_ID'

    """

    environment: BasicEnvironment = BasicEnvironment(applicationName=application_name, projectsBase=projects_base, projectDirectory=project_directory, verbose=verbose)

    diskImageNotarize: DiskImageNotarize = DiskImageNotarize(environment=environment)
    diskImageNotarize.execute()


@command
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
def dmgStaple(application_name: str, projects_base: str = '', project_directory: str = '', verbose: bool = False):

    environment: BasicEnvironment = BasicEnvironment(applicationName=application_name, projectsBase=projects_base, projectDirectory=project_directory, verbose=verbose)

    diskImageStaple: DiskImageStaple = DiskImageStaple(environment=environment)
    diskImageStaple.execute()

@command()
@version_option(version=f'{version}', message='%(prog)s version %(version)s')
@option('--application-name',  '-a', required=True,  help='The application name that py2app built')
@option('--projects-base',     '-b', required=False, help='Projects base, overrides environment variable')
@option('--project-directory', '-d', required=False, help='Project directory, overrides environment variable')
@option('--verbose',           '-v', required=False, is_flag=True, help=VERBOSE_OPTION_HELP)
def dmgVerify(application_name: str, projects_base: str = '', project_directory: str = '', verbose: bool = False):

    environment: BasicEnvironment = BasicEnvironment(applicationName=application_name, projectsBase=projects_base, projectDirectory=project_directory, verbose=verbose)

    diskImageVerify: DiskImageVerify = DiskImageVerify(environment=environment)
    diskImageVerify.execute()


if __name__ == '__main__':
    # noinspection SpellCheckingInspection

    dmgTool(['--application-name', 'UmlDiagrammer', '--dist-directory', 'dist', '--verbose', 'createDmg'])

    """
    dmgTool(['--version'])
    
    dmgNotarize(['-d', 'umldiagrammer', '--application-name', 'UmlDiagrammer', '--verbose'])
    dmgNotarize(['-d', 'umldiagrammer', '-a', 'UmlDiagrammer', '--verbose'])
    dmgStaple(['-d', 'umldiagrammer', '-a', 'UmlDiagrammer', '--verbose'])
    dmgVerify(['-d', 'umldiagrammer', '-a', 'UmlDiagrammer', '--verbose'])
    dmgVerify(['-d', 'umldiagrammer', '-a', 'UmlDiagrammer', '--verbose'])

    dmgTool(['--application-name', 'UmlDiagrammer', '--dist-directory', 'dist', 'signDmg'])

    dmgTool(
        [
            '--application-name', 'UmlDiagrammer',
            '--dist-directory', 'dist',
            'createDmg',
        ]
    )
    
    py2appSign(['--python-version', '3.10', '-d', 'pyut', '--application-name', 'pyut', 'zipsign'])
    py2appSign(['--python-version', '3.10', '-d', 'pyut', '--application-name', 'pyut', 'appsign'])
    py2appSign(['-v', '-p', '3.12', '-d', 'pyut', '-a', 'Pyut', 'zipsign'])
    py2appSign(['-p', '3.11', '-d', 'pyut', '-a', 'pyut', '--verbose', 'appsign', '--fix-sym-link'])

    appNotarize(['-d', 'pyut', '--application-name', 'pyut', '--verbose'])
    appStaple(['-d', 'pyut', '--application-name', 'pyut', '--verbose'])
    notaryTool(['information', '-i', '5f57fc1e-23d3-42ab-b0ad-ec1d2635c4ad'])
    notaryTool(['--keychain-profile', 'NOTARY_TOOL_APP_ID', 'history'])
    appVerify(['-a', 'Pyut', '-d', 'pyut', '--verbose'])
    appNotarize(['-d', 'renderrob', '-a', 'renderrob', '--verbose'])

    # py2appSign(['-v', '-p', '3.13', '-d', 'umldiagrammer', '-a', 'umldiagrammer', 'zipsign', '--delete-part-files'])
    # py2appSign(['-p', '3.13', '-a', 'umldiagrammer', '-d', 'umldiagrammer', 'zipsign', '--help'])
"""
