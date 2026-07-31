
from typing import List

from tqdm import tqdm

from click import secho

from os import linesep as osLineSep

MAX_HDI_UTIL_VALUE: int = 100


class HDIUtilPuppetStringOutput:
    def __init__(self):
        self._progressBar: tqdm = tqdm(total=MAX_HDI_UTIL_VALUE)
        self._progressBar.set_description('Start the disk image creation')

    def updateProgress(self, cmdOutput: str):

        noLf:       str       = cmdOutput.strip(osLineSep)
        splitValue: List[str] = noLf.split(sep=':')

        if len(splitValue) < 2:
            self._progressBar.write(noLf)
        elif splitValue[0] == 'created':
            finalValue: int = MAX_HDI_UTIL_VALUE - self._progressBar.n
            if finalValue > 0:
                self._progressBar.update(finalValue)
            self._progressBar.refresh()
            self._progressBar.close()
            secho(f'Success!  DMG {cmdOutput}')

        else:
            progressValue: float = float(splitValue[1])
            if progressValue == -1.0:
                self._progressBar.update(1)     # fake it
            else:
                intProgressValue: int = int(progressValue)
                deltaValue:       int = intProgressValue - self._progressBar.n
                if deltaValue > 0:
                    self._progressBar.update(deltaValue)
