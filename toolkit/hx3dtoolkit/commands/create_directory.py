from hx3dtoolkit.config import config
import os

class CreateDirectoryCommand:
    def __init__(self, destination, **options):
        self.destination = destination
        self.options = options

    def execute(self):
        if not os.path.exists(self.destination):
            if config.debug_mode:
                print("[D] {} does not exist. Creating...".format(self.destination))
            os.makedirs(self.destination)
        else:
            if config.debug_mode:
                print("[D] {} already exists. Passing...".format(self.destination))
        return 0
