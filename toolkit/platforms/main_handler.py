from .handler import Handler
from commands import *

class MainHandler(Handler):
    def __init__(self, command, args):
        super().__init__(command, args)

    ########

    def clean(self):
        Command("rm -rf _build*", stderr=True).execute()
