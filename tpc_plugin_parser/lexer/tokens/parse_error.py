"""Class to hold a parse error token."""

from dataclasses import dataclass

from tpc_plugin_parser.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class ParseError(object):
    """Dataclass to hold sparse errors."""

    line_number: int
    content: str
    token_name: str = TokenName.PARSE_ERROR.value
