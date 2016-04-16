from dependencies.colorama import Fore, Style

def color_print(txt, color=Fore.GREEN, style=Style.BRIGHT):
    print("{}{}{}{}".format(style, color, txt, Style.RESET_ALL))
