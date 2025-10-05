"""Class to hold the fail state token."""

from dataclasses import dataclass

from tpc_plugin_parser.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class FailState(object):
    """Dataclass to hold a fail state."""

    line_number: int
    name: str
    message: str
    code: int
    token_name: str = TokenName.FAIL_STATE.value

    @property
    def name_normalised(self) -> str:
        """
        Normalised version of the name.

        Returns:
            str: Normalised name.
        """
        return self.name.lower()
