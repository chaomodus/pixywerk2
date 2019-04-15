"""Passthrough progcessor which takes input and returns it."""

import os

from .processors import Processor
from ..utils import guess_mime
from typing import Iterable, Optional, Dict, cast


class PassThrough(Processor):
    """A simple passthrough processor that takes input and sends it to output."""

    def filename(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the filename of the post-processed file.

        Arguments:
            oldname (str): the previous name for the file.
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new name for the file

        """
        return oldname

    def mime_type(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new mimetype of the file after processing

        """
        result = cast(str, guess_mime(oldname))
        if result == "directory":
            result = "DIR"
        return result

    def process(self, input_file: Iterable, ctx: Optional[Dict] = None) -> Iterable:
        """Return an iterable object of the post-processed file.

        Arguments:
            input_file (iterable): An input stream
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            iterable: The post-processed output stream
        """
        return input_file

    def extension(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new extension of the file after processing

        """
        return os.path.splitext(oldname)[-1]


processor = PassThrough
