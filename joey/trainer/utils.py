def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]

def fill_type_map(BaseClass, folder_path=None):
    res = {}
    # TODO: Lookup to folder in the config
    for clazz in all_subclasses(BaseClass):
        if not clazz.type_name is None:
            res[clazz.type_name] = clazz
    return res
