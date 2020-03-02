from pprint import pformat

# TODO: find a way to save the reference from the original converted dictionay/dictionary keys so the values can be
#       accessed from the old dictionary and the new DotDict object.

class DotDictionary(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return None

    def add_dict(self, key, obj):
        if not isinstance(obj, dict) or not isinstance(obj, self.__class__):
            ValueError("Not a dictionary type")
        if isinstance(obj, self.__class__):  # assumes all children of obj are also of type DotDict
            self[key] = obj
        else:
            self[key] = self.from_dict(obj, self)
        return self[key]

    def __setattr__(self, name, value):
        # print("In set attr")
        if isinstance(value, dict):
            self[name] = self.from_dict(value, self.__class__(value))
        else:
            self[name] = value
        return self[name]

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def from_dict(self, obj, depth=None):
        for k,v in obj.items():
            if isinstance(v, dict):
                new = self.__class__(v)
                if depth:
                    depth[k] = self.from_dict(v, new)
                else:
                    self[k] = self.from_dict(v, new)
            else:
                if depth:
                    depth[k] = v
                else:
                    self[k] = v
        if depth:
            return depth
        else:
            return obj

    def __str__(self):
        return pformat(self, indent=4)

testdict = {
    "val01": "0",
    "Level1": {
            "val11": "1",
            "val12": "2",
            "Level2": {
                "Level3": {
                    "val31": "5"
                },
                "val21": "3",
                "val22": "4"
            }
        }
}

if __name__ == "__main__":
    n = DotDictionary()
    n.from_dict(testdict)
    print(n)
    print(type(n))
    print(n.Level1)
    print(type(n.Level1.Level2))
    print(n.Level1.Level2.Level3)
    g = {"t": 40}
    n.Level1.g = g
    n.Level1.Level2.g = g
    print(n)
    print(type(n.Level1.g))