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

RANKS = "AKQJT98765432"
SUITS = "SHDC"


class AppFrame:
    """Create AppFrame for Hand builder application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.card_selected = {}
        self.pbn = ""

        # tk variables
        for rank in RANKS:
            for suit in SUITS:
                self.card_selected[f"{rank}{suit}"] = tk.BooleanVar(
                    value=False
                )

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
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        row = 0
        hand_frame = self._hand_frame(frame)
        hand_frame.grid(row=row, column=0, sticky=tk.NSEW)
        row += 1

        selection_frame = self._selection_frame(frame)
        selection_frame.grid(row=row, column=0, sticky=tk.NSEW)
        row += 1

        return frame

    def _hand_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master, style="red.TFrame")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return frame

    def _selection_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        for column, rank in enumerate(RANKS):
            frame.columnconfigure(column, weight=1)
            for row, suit in enumerate(SUITS):
                frame.rowconfigure(row, weight=1)
                check_button = ttk.Checkbutton(
                    frame,
                    text=f"{rank}{suit}",
                    variable=self.card_selected[f"{rank}{suit}"],
                    command=lambda rank=rank, suit=suit: self._card_checked(
                        rank, suit
                    ),
                )
                check_button.grid(row=row, column=column)
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button("build", self._process, True),
            frame.icon_button("close", self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _card_checked(self, rank: str, suit: str) -> None:
        cards = []
        for key, value in self.card_selected.items():
            if value.get():
                cards.append(key)
        self._value_changed(cards)
        self._print_hand(cards)

    def _print_hand(self, cards: list[str]) -> None:
        self.pbn = self.to_pbn(cards)
        print(self.pbn)

    def to_pbn(self, cards: list[str]) -> str:
        by_suit = {suit: [] for suit in SUITS}
        for card in cards:
            rank, suit = card[0], card[1]
            by_suit[suit].append(rank)

        suits = []
        for suit in SUITS:
            ranks = sorted(by_suit[suit], key=RANKS.index)
            suits.append("".join(ranks))
        return ".".join(suits)

    def _value_changed(self, cards) -> bool:
        """
        Determine whether any configuration value has changed.
        """
        enable = len(cards) > 0
        self.button_frame.enable(enable)

    def _process(self, *args) -> None:
        pass

    def _dismiss(self, *args) -> None:
        self.root.destroy()
