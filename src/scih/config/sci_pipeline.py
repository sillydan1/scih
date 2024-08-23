from typing import NamedTuple

from loguru import logger


class SciPipeline(NamedTuple):
    name: str
    url: str
    trigger: str
    script: str

    @staticmethod
    def from_strings(input: list[str]) -> "SciPipeline | None":
        if len(input) != 4:
            logger.opt(colors=True).error(f'input <yellow>{input}</yellow> was not 4 strings')
            return None
        return SciPipeline(name=input[0], url=input[1], trigger=input[2], script=input[3])
