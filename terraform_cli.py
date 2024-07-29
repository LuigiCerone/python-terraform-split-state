import subprocess
from typing import Optional, List, Union

from model import StateFileType


def list_terraform_state(cwd: Optional[str] = None, filter_state: Optional[str] = None) -> str:
    """
    Lists the resources in the Terraform state file.

    Args:
        cwd (Optional[str]): The working directory to run the Terraform command in. Defaults to None.
        filter_state (Optional[str]): Optional resource filter to apply when listing state. Defaults to None.

    Returns:
        str: Output of the 'terraform state list' command.
    """
    if filter_state:
        command = f"terraform state list | grep {filter_state}"
        return run_cli_command(command, cwd=cwd, text=True, shell=True)
    else:
        command = ["terraform", "state", "list"]
        return run_cli_command(command, cwd=cwd, text=True, shell=False)


def download_terraform_state(cwd: Optional[str] = None, download_dir_destination: str = "",
                             state_file_type: StateFileType = StateFileType.SOURCE):
    """
    Downloads the current Terraform state and saves it to a specified file.

    Args:
        cwd (Optional[str]): The working directory to run the Terraform command in. Defaults to None.
        download_dir_destination (str): The directory path to save the downloaded state file.
        state_file_type (StateFileType): The type of state file to save (source or destination). Defaults to StateFileType.SOURCE.

    Returns:
        None
    """
    command = ["terraform", "state", "pull"]
    command_output = run_cli_command(command, cwd=cwd)

    with open(f'{download_dir_destination}{state_file_type.value}', 'wb') as file:
        file.write(command_output)


def move_resource(resource_to_move_name: str, download_dir_destination: str = "") -> str:
    """
    Moves a resource in the Terraform state from one state file to another.

    Args:
        resource_to_move_name (str): The name of the resource to move.
        download_dir_destination (str): The directory path where the state files are located. Defaults to an empty string.

    Returns:
        str: Output of the 'terraform state mv' command.
    """
    command = ["terraform", "state", "mv", f"-state={download_dir_destination}{StateFileType.SOURCE.value}",
               f"-state-out={download_dir_destination}{StateFileType.DESTINATION.value}",
               resource_to_move_name, resource_to_move_name]
    return run_cli_command(command)


def upload_terraform_state(cwd: Optional[str] = None, download_dir_destination: str = "",
                           state_file_type: StateFileType = StateFileType.SOURCE) -> str:
    """
    Uploads a specified Terraform state file.

    Args:
        cwd (Optional[str]): The working directory to run the command in. Defaults to None.
        download_dir_destination (str): The directory path where the state file is located.
        state_file_type (StateFileType): The type of state file to upload (source or destination). Defaults to StateFileType.SOURCE.

    Returns:
        str: Output of the 'terraform state push' command.
    """
    command = ["terraform", "state", "push", f"{download_dir_destination}{state_file_type.value}"]
    return run_cli_command(command, cwd=cwd)


def init_state(cwd: Optional[str] = None) -> str:
    """
    Initializes the Terraform configuration by running 'terraform init'.

    Args:
        cwd (Optional[str]): The working directory to run the command in. Defaults to None.

    Returns:
        str: Output of the 'terraform init' command.
    """
    command = ["terraform", "init"]
    return run_cli_command(command, cwd=cwd)


def run_cli_command(command: Union[List[str], str], cwd: Optional[str] = None, text: bool = False,
                    shell: bool = False) -> Union[str, bytes]:
    """
    Runs a command line command and returns the output.

    Args:
        command (Union[List[str], str]): The command to run. Can be a list of command arguments or a single command string.
        cwd (Optional[str]): The working directory to run the command in. Defaults to None.
        text (bool): If True, returns the output as a string. If False, returns the output as bytes. Defaults to False.
        shell (bool): If True, the command will be executed through the shell. Defaults to False.

    Returns:
        Union[str, bytes]: Output of the command, as a string if `text` is True, otherwise as bytes.

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status.
    """
    try:
        return subprocess.check_output(command, cwd=cwd, text=text, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        print(f"Error output: {e.output}")
        raise
