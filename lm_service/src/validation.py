from dataclasses import dataclass, field
from typing import Any


@dataclass
class Arg:
    """
    Class to parse a given argument
    """

    value: Any = field()
    type: str = field()
    name: str = field()
    required: bool = field(default=True)

    def is_valid(self):
        """
        Returns whether the argument is valid or not

        Returns:
            bool: True if the argument is valid, false otherwise
        """
        # If the argument is required, check that it contains a value
        if self.required and not self.value:
            return False
        # Check if the argument type matches the type of the value provided
        if type(self.value) != eval(self.type):
            return False
        return True


@dataclass
class Args:
    """
    Class used to parse multiple arguments
    """

    args: list[Arg] = field(default_factory=list)

    def get_invalid(self):
        """
        Returns the first invalid argument found (if any)

        Returns:
            Arg | None: Invalid argument
        """
        for arg in self.args:
            if not arg.is_valid():
                return arg
        return None

    def add(self, arg: Arg):
        """
        Adds an argument to be parsed

        Args:
            arg (Arg): Argument to parse
        """
        self.args.append(arg)
