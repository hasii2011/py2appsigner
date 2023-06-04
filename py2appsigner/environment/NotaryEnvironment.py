
from dataclasses import dataclass

from py2appsigner.Common import DEFAULT_NOTARY_TOOL_KEYCHAIN_PROFILE_NAME


@dataclass
class NotaryEnvironment:

    keyChainProfile: str  = DEFAULT_NOTARY_TOOL_KEYCHAIN_PROFILE_NAME
