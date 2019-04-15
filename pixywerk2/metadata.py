"""Constructs a tree-like object containing the metadata for a given path, and caches said metadata."""

import logging
import mimetypes
import os
import uuid

from typing import Dict, Optional, Union, List, Tuple, Any, cast

import jstyleson

from .utils import guess_mime

# setup mimetypes with some extra ones
mimetypes.init()
mimetypes.add_type("text/html", "thtml")
mimetypes.add_type("text/html", "cont")

logger = logging.getLogger(__name__)


class MetaCacheMiss(Exception):
    """Raised on cache miss."""


class MetaCache:
    """This class provides an in-memory cache for metadata tree."""

    def __init__(self, max_age: float = 200.0):
        """Initialize the cache.

        Arguments:
            max_age (int): the number of seconds to age-out cache items

        """
        self._max_age = max_age
        self._cache: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str, new_time_stamp: float) -> Any:
        """Get an item from the cache.

        Arguments:
            key (str): the cache key to retieve
            new_time_stamp (int): The time to use to compare the stored time with

        Returns:
            :obj:misc: The previously stored value.

        Raises:
            MetaCacheMiss: on missing key, or on aged out

        """
        if key not in self._cache:
            raise MetaCacheMiss("no item for key {}".format(key))

        if self._cache[key][0] + self._max_age <= new_time_stamp:
            return self._cache[key][1]

        raise MetaCacheMiss("cache expired for key {}".format(key))

    def put(self, key: str, value: Union[Dict, List, int, str, object], time_stamp: float) -> None:
        """Put an item into the cache.

        Arguments:
            key (str): the key to store the cache item under
            value (:obj:misc): the value to store
            time_stamp (float): the time stamp to store the item under

        """
        self._cache[key] = (time_stamp, value)


class MetaTree:
    """This provides an interface to loading and caching tree metadata for a given directory tree."""

    def __init__(self, root: str, default_metadata: Optional[Dict] = None):
        """Initialize the metadata tree object.

        Arguments:
            root (str): The path to the root of the file tree to operate on.
            default_metadata (dict, optional): The default metadata to apply to the tree

        """
        self._cache = MetaCache()
        if default_metadata is None:
            default_metadata = {}
        self._default_metadata = default_metadata
        if root[-1] != "/":
            root += "/"
        self._root = root

    def get_metadata(self, rel_path: str) -> Dict:
        """Retrieve the metadata for a given path

        The general procedure is to iterate the tree, at each level
m        load .meta (JSON formatted dictionary) for that level, and
        then finally load the path.meta, and merge these dictionaries
        in descendant order.

        Arguments:
            rel_path (str): The path to retrieve the metadata for (relative to root)

        Returns:
            dict: A dictionary of metadata for that path tree.

        """
        metablob = dict(self._default_metadata)
        # iterate path components from root to target path
        comps = [self._root] + rel_path.split("/")
        fullpath = ""
        for pth in comps:
            fullpath = os.path.join(fullpath, pth)
            st = os.stat(fullpath)

            cachekey = fullpath + ".meta"
            meta = cast(Dict, {})
            try:
                st_meta = os.stat(cachekey)
                meta = self._cache.get(cachekey, st_meta.st_mtime)
            except FileNotFoundError:
                st_meta = None  # type: ignore
            except MetaCacheMiss:
                meta = {}

            if not meta and st_meta:
                meta = jstyleson.load(open(cachekey, "r"))
                self._cache.put(cachekey, meta, st_meta.st_mtime)

            metablob.update(meta)

        # return final dict
        metablob["dir"], metablob["file_name"] = os.path.split(rel_path)
        metablob["file_path"] = rel_path
        metablob["uuid"] = uuid.uuid3(
            uuid.NAMESPACE_OID, metablob["uuid-oid-root"] + os.path.join(self._root, rel_path)
        )
        metablob["os-path"], _ = os.path.split(fullpath)
        metablob["guessed-type"] = guess_mime(os.path.join(self._root, rel_path))
        if "mime-type" not in metablob:
            metablob["mime-type"] = metablob["guessed-type"]
        metablob["stat"] = {}
        for stk in ("st_mtime", "st_ctime", "st_atime", "st_mode", "st_size", "st_ino"):
            metablob["stat"][stk.replace("st_", "")] = getattr(st, stk)

        return metablob
