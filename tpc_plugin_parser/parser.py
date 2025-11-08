"""Parser module for reading and processing TPC files."""

from tpc_plugin_parser.lexer.lexer import Lexer
from tpc_plugin_parser.lexer.tokens.section_header import SectionHeader
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_parser.lexer.utilities.types import ALL_TOKEN_TYPES


class Parser(object):
    """Object to handle parsing ini files."""

    __slots__ = ("_file",)

    def __init__(self, file_contents: str) -> None:
        """
        Initializes the Parser with the given file contents.

        :param file_contents (str): Content of the file to be parsed.
        """

        process_lexer = Lexer(source=file_contents)
        self._prepare_process(lexed_process=process_lexer)

    def _prepare_process(self, lexed_process: Lexer) -> None:
        """
        Prepare the process file from the lexed result.

        :param lexed_process: Result of lexing the process file.
        """
        self._file = self._process_lex(lexed_file=lexed_process)

    @staticmethod
    def _process_lex(lexed_file: Lexer) -> dict[str, list[ALL_TOKEN_TYPES]]:
        """
        Process a lex and return the results.

        :param lexed_file: Result of lexing a file.

        :return: Result of processing the lexed file.
        """
        current_section_name: str = "default"
        section_entries: list[ALL_TOKEN_TYPES,] = []
        sorted_lex = {}
        for lexed_line in lexed_file.tokens:
            if lexed_line[0] == TokenName.SECTION_HEADER:
                sorted_lex[current_section_name] = section_entries
                if isinstance(lexed_line[1], SectionHeader):
                    current_section_name = lexed_line[1].name
                else:
                    # This should never be reached, this is here to satisfy typing.
                    current_section_name = "UNKNOWN"
                section_entries = []
                continue
            section_entries.append(lexed_line[1])
        sorted_lex[current_section_name] = section_entries
        return sorted_lex

    @property
    def parsed_file(self) -> dict[str, list[ALL_TOKEN_TYPES]]:
        """
        Returns the parsed file.

        :return: List of tokens from the file.
        """
        return self._file
