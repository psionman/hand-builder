# forms/frm_config.py
"""ConfigFrame for Hand builder."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from psiutils.constants import PAD
from psiutils.utilities import window_resize

from hand_builder import logger
from hand_builder.buttons import ButtonFrame, IconButton
from hand_builder.config import FIELDS, config
from hand_builder.constants import APP_TITLE
from hand_builder.text import Text

txt = Text()


class ConfigFrame:
    """
    A configuration dialog for editing application settings.
    """

    data_directory: tk.StringVar
    my_int: tk.IntVar
    my_bool: tk.BooleanVar

    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.dialog_opened = False
        self.save_button = None

        # Assign tk variables and check for changes
        config.assign_tk_variables(self, FIELDS, self._check_value_changed)

        self._show()

    def _show(self) -> None:
        """
        Initialize and display the configuration form GUI.
        """
        root = self.root
        root.geometry(config.geometry[Path(__file__).stem])
        root.transient(self.parent.root)
        root.title(f"{APP_TITLE} - {txt.CONFIG}")

        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(
            row=8, column=0, columnspan=9, sticky=tk.EW, padx=PAD, pady=PAD
        )

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

        self.root.update_idletasks()
        root.bind("<Control-x>", self._dismiss)
        root.bind("<Control-s>", self._save_config)
        root.bind("<FocusIn>", self._set_config)
        root.bind(
            "<Configure>", lambda e: window_resize(root, __file__, config)
        )

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        """
        Create and return the main frame containing form input widgets.
        """
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        row = 0
        label = ttk.Label(frame, text="label text")
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.data_directory)
        entry.grid(row=row, column=1, sticky=tk.EW)

        button = IconButton(frame, txt.OPEN, "open", self._get_data_directory)
        button.grid(row=row, column=2, padx=PAD)

        row += 1

        label = ttk.Label(frame, text="Display cards")
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        checkbox = ttk.Checkbutton(frame, variable=self.display_cards)
        checkbox.grid(row=row, column=1, sticky=tk.W, padx=PAD, pady=PAD)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        """
        Create and return the button frame for the form.
        """
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = self._frame_button(frame)
        self.save_button = frame.get_button("save")
        frame.enable(False)
        return frame

    def _frame_button(self, frame: ButtonFrame) -> list[IconButton]:
        return [
            frame.icon_button("save", self._save_config, True, tag="save"),
            frame.icon_button("exit", self._dismiss),
        ]

    def _get_data_directory(self, *args) -> None:
        directory = self._get_directory(self.data_directory.get())
        if directory:
            self.data_directory.set(directory)

    def _get_directory(self, default: str) -> str:
        """
        Prompt the user to select a new data directory and update the value.
        """
        self.dialog_opened = True
        return filedialog.askdirectory(
            initialdir=Path(default),
            parent=self.root,
        )

    def _check_value_changed(self, *args) -> bool:
        """
        Enable or disable form buttons based on changes in configuration.
        """
        enable = bool(self._config_changes())
        self.button_frame.enable(enable)

    def _save_config(self):
        changes = {
            field: f"(old value={change[0]}, new_value={change[1]})"
            for field, change in self._config_changes().items()
        }

        for field in FIELDS:
            config.update(field, getattr(self, field).get())

        logger.info("Config saved", changes=changes)
        self.save_button.disable()
        config.save()
        self._dismiss()

    def _config_changes(self) -> dict:
        stored = config.config
        return {
            field: (stored[field], getattr(self, field).get())
            for field in FIELDS
            if stored[field] != getattr(self, field).get()
        }

    def _set_config(self, *args) -> None:
        if self.dialog_opened:
            self.dialog_opened = False
            return
        for field in FIELDS:
            getattr(self, field).set(config.config[field])

    def _dismiss(self, *args) -> None:
        """
        Close the configuration window and terminate the application.
        """
        self.root.grab_release()
        self.root.destroy()
