"""Test the parser."""

import pytest
from tpc_plugin_parser.parser import Parser


class TestParser(object):
    """Test the lexer."""

    @pytest.mark.parametrize(
        "process_file,prompts_file",
        [
            (
                "tests/data/process.ini",
                "tests/data/prompts.ini",
            ),
        ],
    )
    def test_parser(self, process_file: str, prompts_file: str) -> None:
        """
        Test to ensure that a token parses ok.

        :param process_file: Path to the process file.
        :param prompts_file: Path to the prompts file.
        """
        with open(process_file, "r") as process_file:
            process_content = process_file.read()

        with open(prompts_file, "r") as prompts_file:
            prompts_content = prompts_file.read()

        parser = Parser(process_file=process_content, prompts_file=prompts_content)

        assert len(parser.process_file) == 6
        assert len(parser.process_file["default"]) == 6
        assert len(parser.process_file["states"]) == 8
        assert len(parser.process_file["transitions"]) == 7
        assert len(parser.process_file["CPM Parameters Validation"]) == 5
        assert len(parser.process_file["parameters"]) == 5
        assert len(parser.process_file["Debug Information"]) == 7

        assert len(parser.prompts_file) == 2
        assert len(parser.prompts_file["default"]) == 6
        assert len(parser.prompts_file["conditions"]) == 8
