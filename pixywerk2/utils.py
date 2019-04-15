import mimetypes
import os

from typing import Dict, Optional


def merge_dicts(dict_a: Dict, dict_b: Dict) -> Dict:
    """Merge two dictionaries.

    Arguments:
        dict_a (dict): The dictionary to use as the base.
        dict_b (dict): The dictionary to update the values with.

    Returns:
        dict: A new merged dictionary.

    """
    dict_z = dict_a.copy()
    dict_z.update(dict_b)
    return dict_z


def guess_mime(path: str) -> Optional[str]:
    """Guess the mime type for a given path.

    Arguments:
        root (str): the root path of the file tree
        path (str): the sub-path within the file tree

    Returns:
        str: the guessed mime-type

    """
    mtypes = mimetypes.guess_type(path)
    ftype = None
    if os.path.isdir(path):
        ftype = "directory"
    elif os.access(path, os.F_OK) and mtypes[0]:
        ftype = mtypes[0]
    else:
        ftype = "application/octet-stream"
    return ftype
