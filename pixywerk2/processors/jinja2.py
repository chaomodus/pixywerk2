"""Define a Jinja2 Processor which applies programmable templating to the input stream."""

from typing import Iterable, Optional, Dict, cast

from jinja2 import Environment, FileSystemLoader

from .passthrough import PassThrough


class Jinja2(PassThrough):
    """Pass the input stream through Jinja2 for scritable templating."""

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
        tmpl = template_env.from_string("".join([x for x in input_file]))
        return tmpl.render(metadata=ctx)


processor = Jinja2
