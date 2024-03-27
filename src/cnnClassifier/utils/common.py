"""
Common utility functions
"""
import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads yaml file and returns the configuration

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: configuration parsed from yaml file
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        return ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    """
    Create list of directories

    Args:
        path_to_directories (list): list of path of directories
        verbose (bool, optional): turn logging on or off. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save json data

    Args:
        path (str): path to save json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path_to_json: Path) -> ConfigBox:
    """
    Load json files data

    Args:
        path_to_json (str): path like input

    Returns:
        ConfigBox: content parsed from json file
    """
    with open(path_to_json) as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path_to_json}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save binary file

    Args:
        data (Any): data to be saved as binary
        path (str): path to save binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load binary data

    Args:
        path (str): path to binary file

    Returns:
        Any: data collected from binary file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get size in kB

    Args:
        path (str): path to the file

    Returns:
        str: size in kB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} kB"

def decode_image(img_string, file_name):
    img_data = base64.b64decode(img_string)
    with open(file_name, 'wb') as f:
        f.write(img_data)
        f.close()

def encode_image_into_base64(cropped_image_path):
    with open(cropped_image_path, "rb") as f:
        return base64.b64encode(f.read())