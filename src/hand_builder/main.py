# main.py

"""
A tkinter application for Hand builder.
"""

import sys
import tkinter as tk
from tkinter import ttk

from forms.frm_main import AppFrame
from psiutils.utilities import display_icon
from psiutils.widgets import get_styles

from hand_builder import __app_name__, __version__
from hand_builder.constants import APP_TITLE, ICON_FILE
from hand_builder.module_caller import ModuleCaller

PARSER_ARGS = (
    ("module", "Module to load"),
    ("project", "Project name"),
    ("secondary", "Secondary argument"),
)


def main() -> None:
    root = tk.Tk()
    root.title(APP_TITLE)
    display_icon(root, ICON_FILE, ignore_error=True)

    root.protocol("WM_DELETE_WINDOW", root.destroy)

    get_styles()
    style = ttk.Style()
    style.configure("orange-red-fg.TEntry", foreground="#FF4500")

    if PARSER_ARGS:
        args = ModuleCaller.create_parser(PARSER_ARGS)
        if args.module:
            try:
                ModuleCaller(root, args)
            except Exception:
                root.destroy()
        else:
            AppFrame(root)

    root.mainloop()


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(f"{__app_name__}. Version: {__version__}")
        sys.exit(0)
    main()
