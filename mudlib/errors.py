"""
Exception classes

Snakepit mud driver and mudlib - Copyright by Irmen de Jong (irmen@razorvine.net)
"""


class SecurityViolation(Exception):
    """Some security constraint was violated"""
    pass


class ParseError(Exception):
    """Problem with parsing the user input. Should be shown to the user as a nice error message."""
    pass


class ActionRefused(Exception):
    """The action that was tried was refused by the situation or target object"""
    pass