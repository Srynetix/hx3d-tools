class FrozenDict:
    def __init__(self, base_dict, freeze_children=False):
        self.base_dict = base_dict
        if freeze_children:
            self._freeze(self.base_dict)

    def __getattr__(self, attr):
        if hasattr(self.base_dict, attr):
            return getattr(self.base_dict, attr)
        elif attr in self.base_dict:
            return self.base_dict[attr]
        else:
            return None

    def _freeze(self, _dict):
        for k, v in _dict.items():
            if isinstance(v, dict):
                _dict[k] = FrozenDict(v)
                self._freeze(v)
