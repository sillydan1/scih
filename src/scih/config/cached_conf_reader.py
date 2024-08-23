"""Cached configuration file reader module."""

"""
 scih - Simple CI webhooks integration extension
   Copyright (C) 2024 Asger Gitz-Johansen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import re

from loguru import logger

from scih.config.sci_pipeline import SciPipeline


class CachedConfReader:
    """A wrapper around a config file that will Lazily load the config file."""

    def __init__(self, filepath: str) -> None:
        """Construct a new CachedConfReader.

        Args:
            filepath: Filepath to the configuration file.

        """
        self._pattern = re.compile(r'"[^"]*"|\S+')
        self._config: dict[str, str] | None = None
        self._filepath: str = filepath
        self._last_time_changed: float = 0

    @property
    def config(self) -> dict[str, str]:
        """Lazy loaded, and automatically up-to-date config property."""
        if self._config is None:
            self._config = self._read_config_file()
            self._last_time_changed = self._get_mtime()
        mtime = self._get_mtime()
        if self._last_time_changed < mtime:
            logger.opt(colors=True).info("config file on disk is newer - reloading")
            self._config = self._read_config_file()
        self._last_time_changed = mtime
        return self._config

    def _get_mtime(self) -> float:
        """Get the last time the config file was modified."""
        return os.path.getmtime(self._filepath)

    def _read_config_file(self) -> dict[str, str]:
        """Read the sci configuration file and provide a trigger-name to trigger-file mapping."""
        logger.opt(colors=True).info("loading configuration file")
        result: dict[str, str] = {}
        with open(self._filepath, "r") as f:
            lines = f.readlines()
        for line in lines:
            pipeline = SciPipeline.from_strings(self._pattern.findall(line.strip()))
            if pipeline is not None:
                logger.opt(colors=True).info(
                    f"loaded pipeline <light-blue>{pipeline.name}</light-blue> [<yellow>{pipeline.trigger}</yellow>]"
                )
                result[pipeline.trigger] = f"/tmp/sci/{pipeline.trigger}"
            else:
                logger.error("could not parse pipeline")
        return result
