"""Test the parser."""

import pytest
from tpc_plugin_parser.parser import Parser


class TestParser(object):
    """Test the lexer."""

    @pytest.mark.parametrize(
        "target_file",
        [
            "tests/data/process.ini",
        ],
    )
    def test_process(self, target_file: str) -> None:
        """
        Test to ensure that process file tokens parses ok.

        :param target_file: Path to the file.
        """
        with open(target_file, "r") as file_handler:
            file_content = file_handler.read()

        parser = Parser(file_contents=file_content)

        assert len(parser.parsed_file) == 6
        assert len(parser.parsed_file["default"]) == 6
        assert len(parser.parsed_file["states"]) == 8
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
        Test to ensure that prompts file tokens parses ok.

        :param target_file: Path to the file.
        """
        with open(target_file, "r") as file_handler:
            file_content = file_handler.read()

        parser = Parser(file_contents=file_content)

        assert len(parser.parsed_file) == 2
        assert len(parser.parsed_file["default"]) == 6
        assert len(parser.parsed_file["conditions"]) == 8
