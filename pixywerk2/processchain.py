"""Interface for chains of processors"""

import os
import os.path
import random

from typing import List, Iterable, Optional, Any, Dict, Type, cast

import yaml

from .processors.processors import Processor


class ProcessorChain:
    """This implements a wrapper for an arbitrary set of processors and an associated file stream."""

    def __init__(
        self,
        processors: List[Processor],
        file_name: str,
        file_data: Iterable[str],
        file_type: str,
        ctx: Optional[Dict] = None,
    ):
        """Initialize the processing stream.

        Arguments:
             processors (list): A list of processor objects.
             file_data (Iterable): An iterable from which to retrieve the input
             file_type (str): the specified file type for consumer information.

        """
        self._processors = processors
        self._file_data = file_data
        self._file_type = file_type
        self._file_name = file_name
        self._ctx: Dict = {}
        if ctx is not None:
            self._ctx = cast(Dict, ctx)

    @property
    def output(self) -> Iterable:
        """Return an iterable for the output of the process chain

        Returns:
            :obj:'iterable': the iterable

        """
        prev = self._file_data
        for processor in self._processors:
            if processor:
                prev = processor.process(prev, self._ctx)

        return prev

    @property
    def output_mime(self) -> str:
        """Return the post-processed MIME value from the processing chain

        Returns:
            str: the mime type

        """
        fname = self._file_name
        for processor in self._processors:
            fname = processor.mime_type(fname, self._ctx)
        return fname

    @property
    def output_ext(self) -> str:
        """Return the post-processed extension from the processing chain

        Returns:
            str: the extension
        """
        fname = self._file_name
        for processor in self._processors:
            fname = processor.extension(fname, self._ctx)
        return fname

    @property
    def output_filename(self) -> str:
        """Return the post-processed filename from the processing chain

        Returns:
            str: the new filename

        """
        fname = os.path.basename(self._file_name)
        for processor in self._processors:
            fname = processor.filename(fname, self._ctx)
        return fname


class ProcessorChains:
    """Load a configuration for processor chains, and provide ability to process the chains given a particular input
    file.
    """

    def __init__(self, config: Optional[str] = None):
        """Initialize, with a specified configuration file

        Arguments:
            config (str, optional): The path to a yaml formatted configuration file.

        """
        if config is None:  # pragma: no coverage
            config = os.path.join(os.path.dirname(__file__), "defaults", "chains.yaml")

        self.chainconfig = yaml.load(open(config, "r"))
        self.extensionmap: Dict[str, Any] = {}
        self.processors: Dict[str, Type[Processor]] = {}
        for ch, conf in self.chainconfig.items():
            if conf["extension"] == "default":
                self.default = ch
            else:
                if conf["extension"]:
                    for ex in conf["extension"]:
                        if ex in self.extensionmap or ex is None:
                            # log an error or except or something we'll just override for now.
                            pass
                        self.extensionmap[ex] = ch
            for pr in conf["chain"]:
                if pr in self.processors:
                    continue
                processor_module = __import__("processors", globals(), locals(), [pr], 1)
                self.processors[pr] = processor_module.__dict__[pr].processor

    def get_chain_for_filename(self, filename: str, ctx: Optional[Dict] = None) -> ProcessorChain:
        """Get the ProcessorChain, as configured for a given file by extension.

        Arguments:
            filename (str): The name of the file to get a chain for.

        Returns:
            ProcessorChain: the constructed processor chain.
        """
        r = filename.rsplit(".", 1)
        ftype = "default"
        if r:
            ftype = r[-1]
        if ctx and "pragma" in ctx:
            if "no-proc" in ctx["pragma"]:
                ftype = "default"

        if ctx and "type" in ctx:
            ftype = ctx["type"]
        return self.get_chain_for_file(open(filename, "r"), ftype, filename, ctx)

    def get_chain_for_file(
        self, file_obj: Iterable, file_ext: str, file_name: Optional[str] = None, ctx: Optional[Dict] = None
    ) -> ProcessorChain:
        """Get the ProcessorChain for a given iterable object based on the specified file type

        Arguments:
            file_obj (:obj:`iterable`): The input file stream
            file_ext (str): The type (extension) of the input stream

        Returns:
            ProcessorChain: the constructed processor chain.

        """
        if file_ext not in self.extensionmap or not self.extensionmap[file_ext]:
            if file_ext in self.chainconfig:
                file_type = file_ext
            else:
                file_type = "default"
        else:
            file_type = self.extensionmap[file_ext]

        if not (bool(file_name)):
            file_name = hex(random.randint(0, 65536))

        return ProcessorChain(
            [self.processors[x]() for x in self.chainconfig[file_type]["chain"]],
            cast(str, file_name),
            file_obj,
            file_type,
            ctx,
        )
