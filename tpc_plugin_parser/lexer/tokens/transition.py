"""Class to hold the state transition token."""

from dataclasses import dataclass

from tpc_plugin_parser.lexer.utilities.token_name import TokenName


@dataclass(frozen=True)
class Transition(object):
    """Dataclass to hold state transitions."""

    line_number: int
    current_state: str
    condition: str
    next_state: str
    token_name: str = TokenName.TRANSITION.value
