"""List of regex the lexer uses."""

ASSIGNMENT: str = (
    r"^(?:[\s]*)(?P<name>[\w]+)(?:(?:[\s]*)(?P<equals>=)(?:(?:[\s]*)(?P<value>(?:(?!\s*fail\s*\().)+))?)?(?:[\s]*)$"
)
COMMENT: str = r"^(?:[\s]*)(?P<comment>(?:[#;]+)(?:.*))(?:[\s]*)$"
CPM_PARAMETER_VALIDATION: str = (
    r"^(?:[\s]*)(?P<name>[\w\\]+)(?:(?:[\s]*,[\s]*)(?:source)(?:[\s]*)=(?:[\s]*)"
    r"(?P<source>[^, ]*))(?:(?:[\s]*,[\s]*)(?:mandatory)(?:[\s]*)=(?:[\s]*)"
    r"(?P<mandatory>[^,]*))?(?:(?:[\s]*,[\s]*)(?:allowcharacters)(?:[\s]*)=(?:[\s]*)(?P<allowcharacters>.*))?$"
)
FAIL_STATE: str = (
    r"^(?:[\s]*)(?P<name>[\w]+)(?:[\s]*)=(?:[\s]*)(?:[\s]*)(?:fail)(?:[\s]*)\((?:[\s]*)"
    r"(?P<message>.*)(?:[\s])?,(?:[\s]*)(?P<code>[0-9]+)\)(?:[\s]*)$"
)
SECTION_HEADER: str = r"^(?:[\s]*)\[(?P<name>[\w]+(?:[\s]+[\w]+)*)](?:[\s]*)$"
TRANSITION: str = (
    r"^(?:[\s]*)(?P<current>[\w]+)(?:[\s]*,[\s]*)(?P<condition>[\w]+)(?:[\s]*,[\s]*)(?P<next>[\w]+)(?:[\s]*)$"
)
