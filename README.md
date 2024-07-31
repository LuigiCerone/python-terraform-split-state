# terraform_move_resources

There is a utility script in this repo that is useful if you need to migrate one or more resources between two Terraform
states.
The logic is quite simple, and the script has only been created to automate the repetitive and error-prone task.

You have a source project from which you want to move one or more resources to a target project. These two repos have
separate state files (in our case in a remote backend).

The high level logic is:

* Read the two projects (the path to them is asked via cli), init them and download the states locally.
* Ask the user for a module/resource pattern and apply it to the source state.
* List the results and ask the user to select which resource(s) to move (individual selection(s) or select all logic is
  available).
* Move the selected resources.
* Ask if the resulting states need to be pushed to the remote backend.

**Note**: The script only moves the configuration between the state files, not in the repository. Once the script is
complete, the user will need to move the actual text configuration between the `.tf` file inside the repos.

## Prerequisites

Tested with:

- Python: 3.11.0

## How to run

#### Setup venv

```bash
make
```

#### Run

```bash
source venv/bin/activate
python main.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
