# main.py

"""
A tkinter application for Hand builder.
"""

import argparse
import os
import sys
import tkinter as tk
from tkinter import ttk

import clipboard
from dotenv import load_dotenv
from forms.frm_main import AppFrame
from psiutils.utilities import display_icon
from psiutils.widgets import get_styles

from hand_builder import __app_name__, __version__, logger
from hand_builder.constants import APP_TITLE, ICON_FILE
from hand_builder.module_caller import ModuleCaller

load_dotenv()
uv_python = os.getenv("UV_PYTHON")
if not uv_python:
    print(
        "Have you run export UV_PYTHON=/usr/bin/python3? - copied to clipboard"
    )
    clipboard.copy("export UV_PYTHON=/usr/bin/python3")


def main() -> None:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument(
        "module", nargs="?", default=None, help="Module to load"
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
            dlg = ModuleCaller(root, args.module)
            if dlg.invalid:
                logger.error("Invalid module", module=args.module)
                AppFrame(root)
        except Exception as e:
            logger.error(f"Failed to load module '{args.module}'", error=e)
            AppFrame(root)
    else:
        AppFrame(root)

    root.mainloop()


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(f"{__app_name__}. Version: {__version__}")
        sys.exit(0)
    main()
