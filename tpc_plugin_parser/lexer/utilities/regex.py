"""List of regex the lexer uses."""

ASSIGNMENT = (
    r"^(?:[\s]*)(?P<name>[\w]+)(?:(?:[\s]*)(?P<equals>=)(?:(?:[\s]*)(?P<value>(?:(?!\s*fail\s*\().)+))?)?(?:[\s]*)$"
)
COMMENT = r"^(?:[\s]*)(?P<comment>(?:[#;]+)(?:.*))(?:[\s]*)$"
CPM_PARAMETER_VALIDATION = r"^(?:[\s]*)(?P<name>[\w\\]+)(?:(?:[\s]*,[\s]*)(?:source)(?:[\s]*)=(?:[\s]*)(?P<source>[^, ]*))(?:(?:[\s]*,[\s]*)(?:mandatory)(?:[\s]*)=(?:[\s]*)(?P<mandatory>[^,]*))?(?:(?:[\s]*,[\s]*)(?:allowcharacters)(?:[\s]*)=(?:[\s]*)(?P<allowcharacters>.*))?$"
FAIL_STATE = r"^(?:[\s]*)(?P<name>[\w]+)(?:[\s]*)=(?:[\s]*)(?:[\s]*)(?:fail)(?:[\s]*)\((?:[\s]*)(?P<message>.*)(?:[\s])?,(?:[\s]*)(?P<code>[0-9]+)\)(?:[\s]*)$"
SECTION_HEADER = r"^(?:[\s]*)\[(?P<name>[\w]+(?:[\s]+[\w]+)*)](?:[\s]*)$"
TRANSITION = r"^(?:[\s]*)(?P<current>[\w]+)(?:[\s]*,[\s]*)(?P<condition>[\w]+)(?:[\s]*,[\s]*)(?P<next>[\w]+)(?:[\s]*)$"
