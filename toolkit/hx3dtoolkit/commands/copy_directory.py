from distutils.dir_util import copy_tree
from hx3dtoolkit.config import config

class CopyDirectoryCommand:
    def __init__(self, source, destination, **options):
        self.source = source
        self.destination = destination
        self.options = options

    def execute(self):
        try:
            if config.debug_mode:
                print('[D] Copying `{}` to `{}`'.format(self.source, self.destination))
            copy_tree(self.source, self.destination, update=1)
            return 0
        except OSError as e:
            print('[D] Directory not copied. Error: {}'.format(e))
            return 1
