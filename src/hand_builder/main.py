# main.py

"""
A tkinter application for Hand builder.
"""

import argparse
import sys
import tkinter as tk
from tkinter import ttk

from forms.frm_main import AppFrame
from psiutils.utilities import display_icon
from psiutils.widgets import get_styles

from hand_builder import __app_name__, __version__
from hand_builder.constants import APP_TITLE, ICON_FILE
from hand_builder.module_caller import ModuleCaller


def main() -> None:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument(
        "module", nargs="?", default=None, help="Module to load"
    )
    parser.add_argument(
        "primary", nargs="?", default=None, help="Primary argument"
    )
    parser.add_argument(
        "secondary", nargs="?", default=None, help="Secondary argument"
    )
    args = parser.parse_args()

    root = tk.Tk()
    root.title(APP_TITLE)
    display_icon(root, ICON_FILE, ignore_error=True)

    root.protocol("WM_DELETE_WINDOW", root.destroy)

    get_styles()
    style = ttk.Style()
    style.configure("orange-red-fg.TEntry", foreground="#FF4500")

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
