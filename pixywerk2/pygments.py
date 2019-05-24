"""Map Pygments into the Template API for inclusion in outputs."""
from typing import Optional

import pygments
import pygments.formatters
import pygments.lexers
import pygments.util
import pygments.styles



def pygments_markup_contents_html(input_text: str, file_type: str, style: Optional[str]=None) -> str:
    """Format input string with Pygments and return HTML."""

    if style is None:
        style = 'default'
    style = pygments.styles.get_style_by_name(style)
    formatter = pygments.formatters.get_formatter_by_name('html', style=style)
    try:
        lexer = pygments.lexers.get_lexer_for_filename(file_type)
    except pygments.util.ClassNotFound:
        try:
            lexer = pygments.lexers.get_lexer_by_name(file_type)
        except pygments.util.ClassNotFound:
            lexer = pygments.lexers.get_lexer_by_mimetype(file_type)

    return pygments.highlight(input_text, lexer, formatter)

def pygments_get_css(style: Optional[str]=None) -> str:
    """Return the CSS styles associated with a particular style definition."""

    if style is None:
        style = 'default'
    style = pygments.styles.get_style_by_name(style)
    formatter = pygments.formatters.get_formatter_by_name('html', style=style)
    return formatter.get_style_defs()
