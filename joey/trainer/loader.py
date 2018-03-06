import cPickle as pickle


def store_model(model, fp):
    pickle.dump(model, fp,  protocol=2)


def load_model(fp):
    return pickle.load(fp)
