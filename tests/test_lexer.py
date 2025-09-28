"""Test the lexer."""

import pytest
from tpc_plugin_parser.lexer.lexer import Lexer
from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.lexer.tokens.comment import Comment
from tpc_plugin_parser.lexer.tokens.cpm_parameter_validation import CPMParameterValidation
from tpc_plugin_parser.lexer.tokens.fail_state import FailState
from tpc_plugin_parser.lexer.tokens.parse_error import ParseError
from tpc_plugin_parser.lexer.tokens.section_header import SectionHeader
from tpc_plugin_parser.lexer.tokens.transition import Transition
from tpc_plugin_parser.lexer.utilities.token_name import TokenName


class TestLexer(object):
    """Test the lexer."""

    @pytest.mark.parametrize(
        "line,expected_token_list",
        [
            (
                'password, source=FILE, Mandatory=![string equal -nocase "<username>" ""], allowcharacters=abc',
                [
                    (
                        TokenName.CPM_PARAMETER_VALIDATION,
                        CPMParameterValidation(
                            line_number=1,
                            name="password",
                            source="FILE",
                            mandatory='![string equal -nocase "<username>" ""]',
                            allow_characters="abc",
                            token_name=TokenName.CPM_PARAMETER_VALIDATION.value,
                        ),
                    ),
                ],
            ),
            (
                "TestVar",
                [
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=1,
                            name="TestVar",
                            equals=None,
                            assigned=None,
                        ),
                    ),
                ],
            ),
            (
                "testvar    =   ",
                [
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=1,
                            name="testvar",
                            equals="=",
                            assigned=None,
                        ),
                    ),
                ],
            ),
            (
                "test_var = 123",
                [
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=1,
                            name="test_var",
                            equals="=",
                            assigned="123",
                        ),
                    ),
                ],
            ),
            (
                "# this is a standard comment     ",
                [
                    (
                        TokenName.COMMENT,
                        Comment(
                            line_number=1,
                            content="# this is a standard comment",
                        ),
                    ),
                ],
            ),
            (
                ";this is a standard comment",
                [
                    (
                        TokenName.COMMENT,
                        Comment(
                            line_number=1,
                            content=";this is a standard comment",
                        ),
                    ),
                ],
            ),
            (
                "standard=FAIL('This is a standard fail state', 1234)",
                [
                    (
                        TokenName.FAIL_STATE,
                        FailState(
                            name="standard",
                            line_number=1,
                            message="'This is a standard fail state'",
                            code=1234,
                        ),
                    ),
                ],
            ),
            (
                "standard   =  FAIL  ('This is a standard fail state, isn't it?',     2468)",
                [
                    (
                        TokenName.FAIL_STATE,
                        FailState(
                            name="standard",
                            line_number=1,
                            message="'This is a standard fail state, isn't it?'",
                            code=2468,
                        ),
                    ),
                ],
            ),
            (
                "standard   =  FAIL  (This is a standard fail state, isn't it?,     2468)",
                [
                    (
                        TokenName.FAIL_STATE,
                        FailState(
                            name="standard",
                            line_number=1,
                            message="This is a standard fail state, isn't it?",
                            code=2468,
                        ),
                    ),
                ],
            ),
            (
                "[Some Section Header]",
                [
                    (
                        TokenName.SECTION_HEADER,
                        SectionHeader(
                            line_number=1,
                            name="Some Section Header",
                        ),
                    ),
                ],
            ),
            (
                "   [Some Section Header]    ",
                [
                    (
                        TokenName.SECTION_HEADER,
                        SectionHeader(
                            line_number=1,
                            name="Some Section Header",
                        ),
                    ),
                ],
            ),
            (
                "state1,condition,state2",
                [
                    (
                        TokenName.TRANSITION,
                        Transition(
                            line_number=1,
                            current_state="state1",
                            condition="condition",
                            next_state="state2",
                        ),
                    ),
                ],
            ),
            (
                " state_1    ,   condition2    , STATE2   ",
                [
                    (
                        TokenName.TRANSITION,
                        Transition(
                            line_number=1,
                            current_state="state_1",
                            condition="condition2",
                            next_state="STATE2",
                        ),
                    ),
                ],
            ),
            (
                "[Some Section Header]\r\rTestVar\r",
                [
                    (
                        TokenName.SECTION_HEADER,
                        SectionHeader(
                            line_number=1,
                            name="Some Section Header",
                        ),
                    ),
                    (
                        TokenName.ASSIGNMENT,
                        Assignment(
                            line_number=3,
                            name="TestVar",
                            equals=None,
                            assigned=None,
                        ),
                    ),
                ],
            ),
        ],
    )
    def test_token(self, line: str, expected_token_list) -> None:
        """
        Test to ensure that a token parses ok.

        :param line: The line to be parsed.
        :param expected_token_list: A copy of the object we expect to receive back.
        """
        lexer = Lexer(source=line)
        tokens = lexer.tokens

        # The following 2 lines have been added to ensure we receive the same tokens after process running twice.
        lexer.process()
        tokens_post_process = lexer.tokens

        assert tokens == expected_token_list
        assert tokens_post_process == tokens

    @pytest.mark.parametrize(
        "line,expected_tokens",
        [
            (
                "This line will not match.",
                [
                    ParseError(
                        line_number=1,
                        content="This line will not match.",
                    )
                ],
            ),
        ],
    )
    def test_unmatched_lines(self, line: str, expected_tokens: list[ParseError]) -> None:
        """
        Test to ensure that the lexer returns a ParseError token.

        :param line: The line to be parsed.
        :param expected_tokens: Parse error tokens.
        """
        lex: Lexer = Lexer(source=line)
        lex.process()
        found_tokens = lex.tokens
        assert len(found_tokens) == len(expected_tokens)
        assert found_tokens[0][1].content == expected_tokens[0].content
        assert found_tokens[0][1].line_number == expected_tokens[0].line_number
