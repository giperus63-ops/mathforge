_REGISTRY = {}

def register(name):
    def deco(fn):
        _REGISTRY[name] = fn
        return fn
    return deco

def get(name):
    return _REGISTRY[name]

def names():
    return sorted(_REGISTRY.keys())