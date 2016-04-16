class FrozenDict:

    def __init__(self, base_dict):
        self.base_dict = base_dict

    def __getattr__(self, attr):
        if attr in self.base_dict:
            return self.base_dict[attr]
        else:
            raise AttributeError("No {} in {}".format(attr, type(self)))
