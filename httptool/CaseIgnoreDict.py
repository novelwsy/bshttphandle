class CaseIgnoreDict(dict):
    def __setitem__(self, key, value):
        super(CaseIgnoreDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseIgnoreDict, self).__getitem__(key.lower())

    def update(self, other):
        if isinstance(other, dict):
            for k in other:
                self[k.lower()] = other[k]

    def has_key(self, key):
        return super(CaseIgnoreDict, self).has_key(key.lower())
