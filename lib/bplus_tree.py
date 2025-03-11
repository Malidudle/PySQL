import os
import pickle

_bplus_trees = {}


class BPlusTree:
    def __init__(self, table_name):
        self.table_name = table_name
        self.index = {}
        os.makedirs("db/indexes", exist_ok=True)
        self.tree_file = f"db/indexes/{table_name}_index.db"
        if os.path.exists(self.tree_file):
            self._load_tree()

    def _load_tree(self):
        try:
            with open(self.tree_file, "rb") as f:
                self.index = pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.PickleError) as e:
            self.index = {}

    def _save_tree(self):
        with open(self.tree_file, "wb") as f:
            pickle.dump(self.index, f)

    def insert(self, key, offset):
        if isinstance(key, str) and key.isdigit():
            key = int(key)
        self.index[key] = offset
        self._save_tree()
        return True

    def search(self, key):
        if isinstance(key, str) and key.isdigit():
            key = int(key)
        return self.index.get(key)

    def range_search(self, start_key, end_key):
        if isinstance(start_key, str) and start_key.isdigit():
            start_key = int(start_key)
        if isinstance(end_key, str) and end_key.isdigit():
            end_key = int(end_key)
        result = []
        for key, offset in self.index.items():
            if start_key <= key <= end_key:
                result.append((key, offset))
        result.sort(key=lambda x: x[0])
        return result


def get_bplus_tree(table):
    if table not in _bplus_trees:
        _bplus_trees[table] = BPlusTree(table)
    return _bplus_trees[table]


def insert_into_bplus_tree(table, key, offset):
    tree = get_bplus_tree(table)
    success = tree.insert(key, offset)
    return success


def search_bplus_tree(table, key):
    tree = get_bplus_tree(table)
    offset = tree.search(key)
    return offset


def range_search_bplus_tree(table, start_key, end_key):
    tree = get_bplus_tree(table)
    results = tree.range_search(start_key, end_key)
    print(
        f"B+ Tree: Found {len(results)} records in range [{start_key}, {end_key}] in table {table}"
    )
    return results


__all__ = ["insert_into_bplus_tree", "search_bplus_tree", "range_search_bplus_tree"]
