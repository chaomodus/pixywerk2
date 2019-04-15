import abc

from typing import Iterable, Optional, Dict


class ProcessorException(Exception):  # pragma: no cover
    """A base exception class to be used by processor objects."""


class Processor(abc.ABC):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        """Initialize the class."""

    @abc.abstractmethod
    def filename(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the filename of the post-processed file.

        Arguments:
            oldname (str): the previous name for the file.
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new name for the file

        """

    @abc.abstractmethod
    def mime_type(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new mimetype of the file after processing

        """

    @abc.abstractmethod
    def extension(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new extension of the file after processing

        """

    @abc.abstractmethod
    def process(self, input_file: Iterable, ctx: Optional[Dict] = None) -> Iterable:
        """Return an iterable object of the post-processed file.

        Arguments:
            input_file (iterable): An input stream
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            iterable: The post-processed output stream
        """
