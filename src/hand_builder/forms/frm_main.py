# forms/frm_main.py

"""AppFrame for Hand builder."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from psiutils.buttons import ButtonFrame
from psiutils.constants import PAD
from psiutils.utilities import window_resize

from hand_builder.config import config
from hand_builder.constants import APP_TITLE
from hand_builder.main_menu import MainMenu
from hand_builder.text import Text

txt = Text()


class AppFrame:
    """Create AppFrame for Hand builder application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # tk variables
        # self.xxx = tk.StringVar()

        # Trace
        # self.xxx.trace_add('write', self._value_changed)

        self._show()

    def _show(self):
        root = self.root
        root.geometry(config.geometry[Path(__file__).stem])
        root.title(APP_TITLE)

        main_menu = MainMenu(self)
        main_menu.create()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        self.button_frame = self._button_frame(root)
        self.button_frame.grid(
            row=8, column=0, columnspan=9, sticky=tk.EW, padx=PAD, pady=PAD
        )

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

        root.update_idletasks()
        root.bind("<Control-x>", self._dismiss)
        root.bind("<Control-o>", self._process)
        root.bind(
            "<Configure>",
            lambda e: window_resize(root, __file__, config),
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button("build", self._process, True),
            frame.icon_button("close", self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _value_changed(self) -> bool:
        """
        Determine whether any configuration value has changed.
        """
        enable = self.xxx.get() != config.xxx
        self.button_frame.enable(enable)

    def _process(self, *args) -> None:
        pass

    def _dismiss(self, *args) -> None:
        self.root.destroy()
