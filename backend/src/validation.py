import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Arg:
    """
    Parent argument dataclass
    """

    def is_valid():
        return False


@dataclass
class Param(Arg):
    """
    Class to parse a given parameter
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
class Character(Arg):
    """
    Class to parse a character for the story endpoint
    """

    name: str = field()
    role: str = field()
    traits: list[str] = field()

    def is_valid(self):
        """
        Returns whether the character is valid or not

        Returns:
            bool: True if the character is valid, false otherwise
        """
        is_traits_valid = True
        # Check that all traits are strings with content
        for trait in self.traits:
            if not trait or type(trait) != eval("str"):
                is_traits_valid = False
        # Check that all params are not empty
        if not (self.name and self.role and is_traits_valid):
            return False
        return True

    def __hash__(self):
        """
        Hashes the character information. Used for sets, dicts...
        Returns:
            int: hashed character
        """
        traits = ", ".join(trait for trait in self.traits)
        return hash(self.name + self.role + traits)


@dataclass
class Characters:
    """
    Class to parse multiple characters
    """

    value: list[dict] = field()
    characters: set[Character] = field(default_factory=set)
    name: str = "characters"

    def is_valid(self):
        """
        Returns whether all characters are valid or not

        Returns:
            bool: True if the all characters are valid, false otherwise
        """
        # Remove possible duplicated characters by creating a set
        self.set_characters()
        for character in self.characters:
            if not character.is_valid():
                return False
        return True

    def set_characters(self):
        """
        Translates from dictionary of characters to a set of characters
        """
        for character in self.value:
            name = character.get("name", "")
            role = character.get("role", "")
            traits = character.get("traits", [])
            self.characters.add(Character(name, role, set(traits)))


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
