import os

from cli import get_path, get_string, get_selected_resources, get_confirm
from terraform_cli import list_terraform_state, download_terraform_state, move_resource, upload_terraform_state, \
    init_state
from model import StateFileType

DEFAULT_TMP_DIR: str = f'{os.getcwd()}/tmp/'


def _create_local_dir(tmp_dir_path: str = DEFAULT_TMP_DIR):
    if not os.path.exists(tmp_dir_path):
        os.makedirs(tmp_dir_path)


def main():
    source_project = get_path(msg="Enter source project path:")
    destination_project = get_path(msg="Enter destination project path:")

    print("Initializing tf states")
    init_state(source_project)
    init_state(destination_project)

    print(f'Source: {source_project} and destination: {destination_project}')

    _create_local_dir()

    download_terraform_state(cwd=source_project, download_dir_destination=DEFAULT_TMP_DIR,
                             state_file_type=StateFileType.SOURCE)

    download_terraform_state(cwd=destination_project, download_dir_destination=DEFAULT_TMP_DIR,
                             state_file_type=StateFileType.DESTINATION)

    module_filter = get_string(msg="Enter the name of the module you want to migrate (default *):")

    resources = list_terraform_state(cwd=source_project, filter_state=module_filter)
    if '\n' in resources:
        resources = resources.split('\n')

    selected_resources = get_selected_resources(resources)

    print(f'You are moving from {source_project} to {destination_project} the following resources:')
    for sel_resource in selected_resources:
        print(f"\t{sel_resource}")
    confirm = get_confirm()

    if not confirm:
        return

    # Move the resources from source to destination state files.
    for sel_resource in selected_resources:
        if not sel_resource:
            continue
        print(f"Moving: {sel_resource}")
        move_resource(sel_resource, download_dir_destination=DEFAULT_TMP_DIR)

    # Upload new state files.
    upload = get_confirm(msg="Do you want to upload the file to GCS?")
    if not upload:
        print('Exiting without upload')
        return

    upload_terraform_state(cwd=source_project, download_dir_destination=DEFAULT_TMP_DIR,
                           state_file_type=StateFileType.SOURCE)
    upload_terraform_state(cwd=destination_project, download_dir_destination=DEFAULT_TMP_DIR,
                           state_file_type=StateFileType.DESTINATION)

    print('State files updated in remote backend')


if __name__ == '__main__':
    main()
