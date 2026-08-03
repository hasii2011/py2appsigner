
from pathlib import Path

from py2appsigner.environment.DiskImageEnvironment import DiskImageEnvironment

class BaseDiskImage:
    def __init__(self, environment: DiskImageEnvironment):

        self._environment: DiskImageEnvironment  = environment

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
