
from dataclasses import dataclass
from pathlib import Path

from py2appsigner.environment.ExternalEnvironment import ExternalEnvironment


@dataclass
class DiskImageEnvironment(ExternalEnvironment):

    applicationName:  str = ''
    distDirectory:    Path = Path()
    verbose:          bool = False

    def __init__(self,
                 applicationName:  str,
                 distDirectory:    Path,
                 projectsBase:     str  = '',
                 projectDirectory: str  = '',
                 identity:         str  = '',
                 verbose:          bool = False
                 ):
        """
        Arguments for the command line always override the environment variables

        Args:
            applicationName:
            projectsBase:     Base directory for python projects.
            projectDirectory: The project directory name

        """
        super().__init__(projectsBase=projectsBase, projectDirectory=projectDirectory, identity=identity)

        self.applicationName = applicationName
        self.distDirectory   = distDirectory
        self.verbose         = verbose

    def __str__(self) -> str:

        return (
            f'{super().__str__()}'
        )

    def __repr__(self) -> str:
        return self.__str__()
