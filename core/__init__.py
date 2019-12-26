import pathlib


class G:
    """ global data container """


g = G()

g.ROOT_PATH = pathlib.Path('.').absolute()
