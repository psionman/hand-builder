# forms/frm_xxx.py

"""xxxFrame for Hand builder."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from psiutils.buttons import ButtonFrame
from psiutils.constants import PAD
from psiutils.utilities import window_resize

from hand_builder.config import config
from hand_builder.constants import APP_TITLE, DEFAULT_GEOMETRY
from hand_builder.text import Text

txt = Text()

FRAME_TITLE = f"{APP_TITLE} - <title>"


class xxxFrame:
    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)

        # tk variables

        self.show()

    def show(self) -> None:
        root = self.root
        try:
            root.geometry(config.geometry[Path(__file__).stem])
        except KeyError:
            root.geometry(DEFAULT_GEOMETRY)
        root.title(FRAME_TITLE)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        row = 0
        main_frame = self._main_frame(root)
        main_frame.grid(row=row, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        row += 1
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(
            row=row, column=0, columnspan=9, sticky=tk.EW, padx=PAD, pady=PAD
        )

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(column=0, sticky=tk.SE)

        self.root.update_idletasks()
        root.bind("<Control-x>", self._dismiss)
        root.bind(
            "<Configure>", lambda e: window_resize(root, __file__, config)
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button("build", self._process, True),
            frame.icon_button("exit", self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _process(self, *args) -> None:
        pass

    def _dismiss(self, *args) -> None:
        self.root.destroy()
