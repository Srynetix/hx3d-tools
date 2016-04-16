from distutils.dir_util import copy_tree
from config import config
import os
import shutil

class CopyFileCommand:
    def __init__(self, source, destination, **options):
        self.source = source
        self.destination = destination
        self.options = options

    def execute(self):
        if os.path.exists(self.destination):
            if config.debug_mode:
                print('[D] File {} already exists.'.format(self.destination))
            shutil.rmtree(self.destination, ignore_errors=True)
        try:
            if config.debug_mode:
                print('[D] Copying `{}` to `{}`'.format(self.source, self.destination))
            shutil.copy(self.source, self.destination)
        except OSError as e:
            print('[D] Error while copying `{}` to `{}`. Error: `{}`'.format(self.source, self.destination, e))
