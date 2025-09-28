"""Enum to hold the allowed token names."""

from enum import Enum


class TokenName(Enum):
    """CLass to hold the token name."""

    ASSIGNMENT = "Assignment"
    COMMENT = "Comment"
    FAIL_STATE = "Fail State"
    CPM_PARAMETER_VALIDATION = "CPM Parameter Validation"
    PARSE_ERROR = "Parse Error"
    SECTION_HEADER = "Section Header"
    TRANSITION = "Transition"
