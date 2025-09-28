"""Class to hold the assignment token."""

from dataclasses import dataclass

from tpc_plugin_parser.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class Assignment(object):
    """Dataclass to hold variable assignment details."""

    line_number: int
    name: str
    equals: str | None = None
    assigned: str | None = None
    token_name: str = TokenName.ASSIGNMENT.value
