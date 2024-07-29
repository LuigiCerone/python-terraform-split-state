import os
from typing import List, Optional

from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator


def get_path(msg: str = "Enter path:") -> str:
    """
    Prompt the user to enter a directory path.

    Args:
        msg (str): The prompt message to display to the user. Defaults to "Enter path:".

    Returns:
        str: The expanded directory path entered by the user.
    """
    input_path = inquirer.filepath(
        message=msg,
        validate=PathValidator(is_dir=True, message="Input is not a directory"),
        only_directories=True,
    ).execute()

    if input_path:
        return os.path.expanduser(input_path)


def get_string(msg: str = "Enter string:") -> str:
    """
    Prompt the user to enter a string.

    Args:
        msg (str): The prompt message to display to the user. Defaults to "Enter string:".

    Returns:
        str: The string entered by the user.
    """
    input_string = inquirer.text(
        message=msg,
        default=""
    ).execute()
    return input_string


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def get_selected_resources(resources_list: List[str]) -> Optional[List[str]]:
    """
    Prompt the user to select resources from a given list.

    Args:
        resources_list (List[str]): The list of resources to choose from.

    Returns:
        Optional[List[str]]: A list of selected resources or None if no selection is made.
    """
    choices = inquirer.select(
        message="Select resources to move from source to destination project:",
        choices=[Choice(value=resources_list, name="Select ALL"), Separator()] + resources_list,
        default=None,
        multiselect=True,
    ).execute()

    if len(choices) > 0 and isinstance(choices[0], list):
        return flatten_list(choices)
    else:
        return choices


def get_confirm(msg: str = "Confirm?") -> bool:
    """
    Prompt the user to confirm an action.

    Args:
        msg (str): The prompt message to display to the user. Defaults to "Confirm?".

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    return inquirer.confirm(message=msg, default=True).execute()
