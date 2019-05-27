"""Define a Jinja2 processor which embeds the (presumably HTML) input stream into a Page Template
   as defined in the ctx metadata (the ``content`` variable is assigned to the input stream and
   the target template is rendered)."""

import os

from typing import Iterable, Optional, Dict, cast

from jinja2 import Environment, FileSystemLoader

from .processors import Processor


class Jinja2PageEmbed(Processor):
    """Embed input stream as ``content`` variable in page template defined in context key ``template``."""

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

    def process(self, input_file: Iterable, ctx: Optional[Dict] = None) -> Iterable:
        """Return an iterable object of the post-processed file.

        Arguments:
            input_file (iterable): An input stream
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            iterable: The post-processed output stream
        """
        ctx = cast(Dict, ctx)
        template_env = Environment(loader=FileSystemLoader(ctx["templates"]), extensions=['jinja2.ext.do'])
        template_env.globals.update(ctx["globals"])
        template_env.filters.update(ctx["filters"])
        tmpl = template_env.get_template(ctx["template"])
        content = "".join([x for x in input_file])
        return tmpl.render(content=content, metadata=ctx)

    def extension(self, oldname: str, ctx: Optional[Dict] = None) -> str:
        """Return the mimetype of the post-processed file.

        Arguments:
            oldname (str): the input filename
            ctx (dict, optional): A context object generated from the processor configuration

        Returns:
            str: the new extension of the file after processing

        """
        return "html"


processor = Jinja2PageEmbed
