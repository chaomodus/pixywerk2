import datetime
import glob
import itertools
import os
import pytz
from typing import Callable, Dict, List, Iterable, Union, cast

from .metadata import MetaTree
from .processchain import ProcessorChains


def file_list(root: str, listcache: Dict) -> Callable:
    def get_file_list(path_glob: str, *, sort_order: str = "ctime", reverse: bool = False, limit: int = 0) -> Iterable:
        stattable = cast(List, [])
        if path_glob in listcache:
            stattable = listcache[path_glob]
        else:
            for fil in glob.glob(os.path.join(root, path_glob)):
                if os.path.isdir(fil):
                    continue
                if fil.endswith(".meta") or fil.endswith("~"):
                    continue
                st = os.stat(fil)
                stattable.append(
                    {
                        "file_path": os.path.relpath(fil, root),
                        "file_name": os.path.split(fil)[-1],
                        "mtime": st.st_mtime,
                        "ctime": st.st_ctime,
                        "size": st.st_size,
                        "ext": os.path.splitext(fil)[1],
                    }
                )
            listcache[path_glob] = stattable
        ret = sorted(stattable, key=lambda x: x[sort_order], reverse=reverse)
        if limit > 0:
            return itertools.islice(ret, limit)
        return ret

    return get_file_list


def file_name(root: str, metatree: MetaTree, processor_chains: ProcessorChains, namecache: Dict) -> Callable:
    def get_file_name(file_name: str) -> Dict:
        if file_name in namecache:
            return namecache[file_name]
        metadata = metatree.get_metadata(file_name)
        chain = processor_chains.get_chain_for_filename(os.path.join(root, file_name), ctx=metadata)
        namecache[file_name] = chain.output_filename
        return namecache[file_name]

    return get_file_name

def file_raw(root: str, contcache: Dict) -> Callable:
    def get_raw(file_name: str) -> str:
        if file_name in contcache:
            return contcache[file_name]
        with open(os.path.join(root, file_name), 'r', encoding="utf-8") as f:
            return f.read()

    return get_raw

def file_content(root: str, metatree: MetaTree, processor_chains: ProcessorChains, contcache: Dict) -> Callable:
    def get_file_content(file_name: str) -> Iterable:
        if file_name in contcache:
            return contcache[file_name]
        metadata = metatree.get_metadata(file_name)
        chain = processor_chains.get_chain_for_filename(os.path.join(root, file_name), ctx=metadata)
        contcache[file_name] = chain.output
        return unicode(chain.output)

    return get_file_content


def file_metadata(metatree: MetaTree) -> Callable:
    def get_file_metadata(file_name: str) -> Dict:
        return metatree.get_metadata(file_name)

    return get_file_metadata


def time_iso8601(timezone: str) -> Callable:
    tz = pytz.timezone(timezone)

    def get_time_iso8601(time_t: Union[int, float]) -> str:
        return datetime.datetime.fromtimestamp(time_t, tz).isoformat("T")

    return get_time_iso8601
