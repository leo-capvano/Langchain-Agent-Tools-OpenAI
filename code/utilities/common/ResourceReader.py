import os

from definitions import PROJECT_ROOT_PATH


def read_resource(resource_file_name: str) -> str:
    with open(os.path.join(PROJECT_ROOT_PATH, "res", resource_file_name), "r") as res:
        return res.read()
