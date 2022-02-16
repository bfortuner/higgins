import json
import os
from pathlib import Path

from . import COMPLETION_CACHE_FILE


class JSONCache:
    def __init__(self, cache_path: str):
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        self.cache_path = cache_path
        self._cache = self._init_cache(cache_path)

    def _init_cache(self, cache_path):
        cache = {}
        if os.path.exists(cache_path):
            cache = json.load(open(cache_path))
        return cache

    def get(self, key):
        if key in self._cache:
            return self._cache[key]
        return None

    def add(self, key, value):
        self._cache[key] = value
        self.save()

    def save(self):
        json.dump(self._cache, open(self.cache_path, "w"))

    def __contains__(self, key):
        return key in self._cache

    def __getitem__(self, key):
        return self._cache[key]


def get_default_cache():
    return JSONCache(COMPLETION_CACHE_FILE)
