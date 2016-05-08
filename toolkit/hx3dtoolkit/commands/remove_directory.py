from hx3dtoolkit.config import config
import shutil
import os

class RemoveDirectoryCommand:
    def __init__(self, directory, **options):
        self.directory = directory
        self.options = options

    def execute(self):
        if os.path.exists(self.directory):
            if config.debug_mode:
                print('[D] Removing `{}`'.format(self.directory))
            shutil.rmtree(self.directory, ignore_errors=True)
        else:
            if config.debug_mode:
                print('[D] Directory {} does not exist. Not removing...'.format(self.directory))
