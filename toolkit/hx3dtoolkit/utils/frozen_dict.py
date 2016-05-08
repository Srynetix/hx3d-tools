class FrozenDict:
    def __init__(self, base_dict, freeze_children=False):
        self.base_dict = base_dict or {}
        if freeze_children:
            self._freeze(self.base_dict)

    def __getattr__(self, attr):
        if hasattr(self.base_dict, attr):
            return getattr(self.base_dict, attr)
        elif attr in self.base_dict:
            return self.base_dict[attr]
        else:
            return None

    def __setitem__(self, key, item):
        self.base_dict.__setitem__(key, item)

    def _freeze(self, _dict):
        for k, v in _dict.items():
            if isinstance(v, dict):
                _dict[k] = FrozenDict(v)
                self._freeze(v)

    @classmethod
    def fromJSON(cls, json_content, freeze_children=False):
        import json
        return cls(json.loads(json_content), freeze_children)
