from logging import Logger
from logging import getLogger

from abc import abstractmethod
from abc import ABC

from py2appsigner.Environment import Environment


class CommandBase(ABC):

    def __init__(self, environment: Environment):

        self._environment: Environment = environment

        self.logger: Logger = getLogger(__name__)

    @abstractmethod
    def execute(self):
        pass
