"""Lexer module for reading and processing configuration files."""

import re

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.tokens.comment import Comment
from tpc_plugin_parser.lexer.tokens.cpm_parameter_validation import (
    CPMParameterValidation,
)
from tpc_plugin_parser.lexer.tokens.fail_state import FailState
from tpc_plugin_parser.lexer.tokens.parse_error import ParseError
from tpc_plugin_parser.lexer.tokens.section_header import SectionHeader
from tpc_plugin_parser.lexer.tokens.transition import Transition
from tpc_plugin_parser.lexer.utilities.regex import (
    ASSIGNMENT,
    COMMENT,
    CPM_PARAMETER_VALIDATION,
    FAIL_STATE,
    SECTION_HEADER,
    TRANSITION,
)
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_parser.lexer.utilities.types import ALL_TOKEN_TYPES, TokenSpecs


class Lexer(object):
    """Object to handle processing the ini files."""

    __slots__ = (
        "_tokens",
        "_source",
        "_token_specs",
    )

    def __init__(self, source: str) -> None:
        """Standard init for the Lexer object."""

        self._tokens: list[
            tuple[
                TokenName,
                ALL_TOKEN_TYPES,
            ]
        ] = []
        self._source: str = source
        self._token_specs: list[TokenSpecs] = [
            {
                "pattern": re.compile(ASSIGNMENT, re.IGNORECASE),
                "token_name": TokenName.ASSIGNMENT,
                "processor_method": "_process_assignment",
            },
            {
                "pattern": re.compile(COMMENT, re.IGNORECASE),
                "token_name": TokenName.COMMENT,
                "processor_method": "_process_comment",
            },
            {
                "pattern": re.compile(CPM_PARAMETER_VALIDATION, re.IGNORECASE),
                "token_name": TokenName.CPM_PARAMETER_VALIDATION,
                "processor_method": "_process_cpm_parameter_validation",
            },
            {
                "pattern": re.compile(FAIL_STATE, re.IGNORECASE),
                "token_name": TokenName.FAIL_STATE,
                "processor_method": "_process_fail_state",
            },
            {
                "pattern": re.compile(SECTION_HEADER, re.IGNORECASE),
                "token_name": TokenName.SECTION_HEADER,
                "processor_method": "_process_section_header",
            },
            {
                "pattern": re.compile(TRANSITION, re.IGNORECASE),
                "token_name": TokenName.TRANSITION,
                "processor_method": "_process_transitions",
            },
        ]

    def process(self) -> None:
        """
        Process the content of the file line by line.
        """

        if self._tokens:
            # Returning as we have parsed the data already.
            return

        for line_number, line in enumerate(self._source.splitlines(), start=1):
            for token_spec in self._token_specs:
                if match := token_spec["pattern"].match(line):
                    getattr(self, token_spec["processor_method"])(match=match, line_number=line_number)
                    break
            else:
                if line.strip():
                    self._process_parse_error(line=line, line_number=line_number)

    def _process_assignment(self, match: re.Match, line_number: int) -> None:
        """
        Process a variable assignment line

        :param match: Regex match of the assignment.
        """
        name: str = str(match.group("name")).strip()
        equals = str(match.group("equals")).strip() if match.groupdict().get("equals", None) else None
        assigned_stripped = str(match.group("value")).strip() if match.groupdict().get("value", None) else None
        assigned = assigned_stripped or None
        self._tokens.append(
            (
                TokenName.ASSIGNMENT,
                Assignment(
                    name=name,
                    equals=equals,
                    assigned=assigned,
                    line_number=line_number,
                ),
            )
        )

    def _process_comment(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided comment.

        :param match: Regex match of the comment.
        """
        self._tokens.append(
            (
                TokenName.COMMENT,
                Comment(
                    content=str(match.group("comment")).strip(),
                    line_number=line_number,
                ),
            )
        )

    def _process_cpm_parameter_validation(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided parameter validation.

        :param match: Regex match of the parameter validation.
        """
        allow_characters: str | None = None
        if match.group("allowcharacters"):
            allow_characters = str(match.group("allowcharacters")).strip()

        self._tokens.append(
            (
                TokenName.CPM_PARAMETER_VALIDATION,
                CPMParameterValidation(
                    name=str(match.group("name")),
                    source=str(match.group("source")),
                    mandatory=str(match.group("mandatory")),
                    allow_characters=allow_characters,
                    line_number=line_number,
                ),
            )
        )

    def _process_fail_state(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided fail state .

        :param match: Regex match of the fail state.
        """
        self._tokens.append(
            (
                TokenName.FAIL_STATE,
                FailState(
                    name=str(match.group("name")).strip(),
                    message=str(match.group("message")).strip(),
                    code=int(match.group("code")),
                    line_number=line_number,
                ),
            )
        )

    def _process_parse_error(self, line: str, line_number: int) -> None:
        """
        Process a line that has a parse error.

        :param line: The line that has the parse error.
        :param line_number: The line number of the line that has the parse error.
        """
        self._tokens.append(
            (
                TokenName.PARSE_ERROR,
                ParseError(
                    content=line.strip(),
                    line_number=line_number,
                ),
            )
        )

    def _process_section_header(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided section header.

        :param match: Regex match of the section header.
        """
        self._tokens.append(
            (
                TokenName.SECTION_HEADER,
                SectionHeader(
                    name=str(match.group("name").strip()),
                    line_number=line_number,
                ),
            )
        )

    def _process_transitions(self, match: re.Match, line_number: int) -> None:
        """
        Process the provided transitions.

        :param match: Regex match of the transitions.
        """
        self._tokens.append(
            (
                TokenName.TRANSITION,
                Transition(
                    current_state=str(match.group("current")).strip(),
                    condition=str(match.group("condition")).strip(),
                    next_state=str(match.group("next")).strip(),
                    line_number=line_number,
                ),
            )
        )

    @property
    def tokens(
        self,
    ) -> list[
        tuple[
            TokenName,
            ALL_TOKEN_TYPES,
        ]
    ]:
        """A list of tokens found by the lexer."""
        if not self._tokens:
            self.process()
        return self._tokens
