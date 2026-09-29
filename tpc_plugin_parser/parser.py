"""Parser module for reading and processing TPC files."""

from tpc_plugin_parser.lexer.lexer import Lexer
from tpc_plugin_parser.lexer.tokens.section_header import SectionHeader
from tpc_plugin_parser.lexer.utilities.token_name import TokenName
from tpc_plugin_parser.lexer.utilities.types import ALL_TOKEN_TYPES


class Parser:
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
        current: list[ALL_TOKEN_TYPES] = []
        sorted_lex: dict[str, list[ALL_TOKEN_TYPES]] = {"default": current}
        for token_name, token in lexed_file.tokens:
            if token_name == TokenName.SECTION_HEADER and isinstance(token, SectionHeader):
                current = sorted_lex.setdefault(token.name, [])
                continue
            current.append(token)
        return sorted_lex

    @property
    def parsed_file(self) -> dict[str, list[ALL_TOKEN_TYPES]]:
        """
        Returns the parsed file.

        :return: List of tokens from the file.
        """
        return self._file
