"""Class to hold the section header token."""

from dataclasses import dataclass

from tpc_plugin_parser.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class SectionHeader(object):
    """Dataclass to hold a section header name."""

    line_number: int
    name: str
    token_name: str = TokenName.SECTION_HEADER.value
