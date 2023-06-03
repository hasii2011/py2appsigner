
from dataclasses import dataclass


@dataclass
class NotaryEnvironment:

    keyChainProfile: str  = ''
    verbose:         bool = False
