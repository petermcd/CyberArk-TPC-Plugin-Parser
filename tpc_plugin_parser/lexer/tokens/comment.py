"""Class to hold the comment token."""

from dataclasses import dataclass

from tpc_plugin_parser.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class Comment(object):
    """Dataclass to hold a comment."""

    line_number: int
    content: str
    token_name: str = TokenName.COMMENT.value
