"""Convert an MD stream into an HTML stream"""

import io
import os

from typing import Iterable, Optional, Dict

import markdown

from .processors import Processor


class MarkdownProcessor(Processor):
    """Convert an MD stream into an HTML stream"""

    def filename(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the filename of the post-processed file.

        Arguments:
            oldname (str): the previous name for the file.
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new name for the file

        """
        return os.path.splitext(oldname)[0] + ".html"

    def mime_type(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new mimetype of the file after processing

        """
        return "text/html"

    def extension(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new extension of the file after processing

        """
        return "html"

    def process(self, input_file: Iterable, ctx: Optional[Dict] = None) -> Iterable:
        """Return an iterable object of the post-processed file.

        Arguments:
            input_file (iterable): An input stream
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            iterable: The post-processed output stream
        """
        md = u"".join([x for x in input_file])
        return io.StringIO(markdown.markdown(md, extensions=["extra", "admonition", "wikilinks"]))


processor = MarkdownProcessor  # pylint: disable=invalid-name
