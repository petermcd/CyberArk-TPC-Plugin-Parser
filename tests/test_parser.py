"""Test the parser."""

import pytest

from tpc_plugin_parser.lexer.tokens.assignment import Assignment
from tpc_plugin_parser.parser import Parser


class TestParser:
    """Test the lexer."""

    @pytest.mark.parametrize(
        "target_file",
        [
            "tests/data/process.ini",
        ],
    )
    def test_process(self, target_file: str) -> None:
        """
        Test to ensure that process file tokens parses OK.

        :param target_file: Path to the file.
        """
        with open(target_file, "r") as file_handler:
            file_content = file_handler.read()

        parser = Parser(file_contents=file_content)

        assert len(parser.parsed_file) == 6
        assert len(parser.parsed_file["default"]) == 6
        assert len(parser.parsed_file["states"]) == 9
        assert len(parser.parsed_file["transitions"]) == 7
        assert len(parser.parsed_file["CPM Parameters Validation"]) == 5
        assert len(parser.parsed_file["parameters"]) == 5
        assert len(parser.parsed_file["Debug Information"]) == 7

    @pytest.mark.parametrize(
        "target_file",
        [
            "tests/data/prompts.ini",
        ],
    )
    def test_prompts(self, target_file: str) -> None:
        """
        Test to ensure that prompts file tokens parses OK.

        :param target_file: Path to the file.
        """
        with open(target_file, "r") as file_handler:
            file_content = file_handler.read()

        parser = Parser(file_contents=file_content)

        assert len(parser.parsed_file) == 2
        assert len(parser.parsed_file["default"]) == 6
        assert len(parser.parsed_file["conditions"]) == 8

    def test_duplicate_sections_are_merged(self) -> None:
        """Test that a repeated section header adds to the earlier section rather than replacing it."""
        parser = Parser(file_contents="[s]\na=1\n[t]\nb=2\n[s]\nc=3")

        assert parser.parsed_file["s"] == [
            Assignment(line_number=2, name="a", equals="=", assigned="1"),
            Assignment(line_number=6, name="c", equals="=", assigned="3"),
        ]
        assert parser.parsed_file["t"] == [
            Assignment(line_number=4, name="b", equals="=", assigned="2"),
        ]

    def test_explicit_default_section_does_not_overwrite_preamble(self) -> None:
        """Test that an explicit [default] section is merged with lines preceding the first header."""
        parser = Parser(file_contents="x=1\n[default]\ny=2")

        assert parser.parsed_file["default"] == [
            Assignment(line_number=1, name="x", equals="=", assigned="1"),
            Assignment(line_number=3, name="y", equals="=", assigned="2"),
        ]
