# forms/frm_main.py

"""AppFrame for Hand builder."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from bridgeobjects import Hand
from clipboard import copy
from PIL import Image, ImageDraw, ImageFont, ImageTk
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

IMAGE_DIR = (
    "/home/jeff/projects/bfg/bfg_api/src/locale/en_GB/images/card_images"
)
SUIT_SYMBOLS = {
    "H": "♥",
    "D": "♦",
    "C": "♣",
    "S": "♠",
}

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT = ImageFont.truetype(FONT_PATH, 16)
CARD_IMAGE_HEIGHT = 100


class AppFrame:
    """Create AppFrame for Hand builder application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.card_selected = {}
        self.hand_frame = None

        # tk variables
        self.pbn = tk.StringVar(value="")
        self.hand_length = tk.IntVar(value=0)
        self.hand_data = tk.StringVar(value="")
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
        self.hand_frame = self._hand_frame(frame)
        self.hand_frame.grid(row=row, column=0, sticky=tk.NSEW)
        row += 1

        pbn_frame = self._pbn_frame(frame)
        pbn_frame.grid(row=row, column=0, sticky=tk.NSEW)
        row += 1

        selection_frame = self._selection_frame(frame)
        selection_frame.grid(row=row, column=0, sticky=tk.NSEW)
        row += 1

        return frame

    def _hand_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(
            master, style="green.TFrame", height=CARD_IMAGE_HEIGHT + 10
        )
        frame.grid_propagate(False)
        frame.rowconfigure(0, weight=1)
        return frame

    def _pbn_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        row = 0
        label = ttk.Label(frame, text="PBN:")
        label.grid(row=row, column=0, sticky=tk.E)

        entry = ttk.Entry(
            frame,
            width=20,
            state="readonly",
            takefocus=False,
            textvariable=self.pbn,
        )

        entry.grid(row=row, column=1, columnspan=2, sticky=tk.W)
        button = ttk.Button(
            frame, text="Copy", command=lambda: copy(self.pbn.get())
        )
        button.grid(row=row, column=3, sticky=tk.W, padx=PAD)

        row += 1
        label = ttk.Label(frame, text="Hand Length:")
        label.grid(row=row, column=0, sticky=tk.E)
        self.hand_length_entry = ttk.Entry(
            frame,
            width=10,
            state="readonly",
            takefocus=False,
            textvariable=self.hand_length,
            style="orange-red-fg.TEntry",
        )
        self.hand_length_entry.grid(row=row, column=1, sticky=tk.W)
        label = ttk.Label(frame, textvariable=self.hand_data)
        label.grid(row=row, column=2, sticky=tk.W)
        return frame

    def _selection_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        self.card_label_images = {}

        for column, rank in enumerate(RANKS):
            frame.columnconfigure(column, weight=1)
            for row, suit in enumerate(SUITS):
                frame.rowconfigure(row, weight=1)
                frame.rowconfigure(row, weight=1)
                card = f"{rank}{suit}"
                img = self._make_label_image(rank, suit)
                self.card_label_images[card] = img

                check_button = ttk.Checkbutton(
                    frame,
                    image=img,
                    variable=self.card_selected[card],
                    command=lambda rank=rank, suit=suit: self._card_checked(
                        rank, suit
                    ),
                )
                check_button.grid(row=row, column=column)
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            # frame.icon_button("build", self._process, True),
            frame.icon_button("close", self._dismiss),
        ]
        frame.enable(False)
        return frame

    def _card_checked(self, rank: str, suit: str) -> None:
        cards = self._get_checked_cards()
        self.hand_length_entry.configure(style="orange-red-fg.TEntry")
        if len(cards) == 13:
            self.hand_length_entry.configure(style="green-fg.TEntry")
        if len(cards) > 13:
            self.hand_length_entry.configure(style="red-fg.TEntry")
        self.hand_length.set(len(cards))

        self.pbn.set(self.to_pbn(cards))
        self._value_changed(cards)
        self._hand_image()

    def _get_checked_cards(self) -> list[str]:
        cards = []
        for key, value in self.card_selected.items():
            if value.get():
                cards.append(key)
        return cards

    def _print_hand(self, cards: list[str]) -> None:
        print(self.pbn.get())

    def _hand_image(self) -> None:
        self._clear_hand_frame()
        hand = Hand(self.pbn.get())
        self.hand_data.set(f"{hand.shape} {hand.hcp}")
        for column, card in enumerate(hand.cards):
            img = Image.open(Path(IMAGE_DIR, f"{card.name}.png"))
            scale = 100 / img.height
            img = img.resize(
                (int(img.width * scale), int(img.height * scale)),
                Image.LANCZOS,
            )
            width, height = img.size
            left_third = img.crop((0, 0, width // 2, height))
            img = ImageTk.PhotoImage(left_third)
            self._place_image(img, column)

    def _make_label_image(self, rank: str, suit: str) -> ImageTk.PhotoImage:
        symbol = SUIT_SYMBOLS[suit]
        colour = "red" if suit in ("H", "D") else "black"

        # measure widths so the two runs sit flush together
        dummy = Image.new("RGBA", (1, 1))
        d = ImageDraw.Draw(dummy)
        rank_w = d.textlength(rank, font=FONT)
        symbol_w = d.textlength(symbol, font=FONT)

        img = Image.new("RGBA", (int(rank_w + symbol_w) + 4, 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), rank, font=FONT, fill="black")
        draw.text((rank_w, 0), symbol, font=FONT, fill=colour)
        return ImageTk.PhotoImage(img)

    def _place_image(self, img: ImageTk.PhotoImage, column: int) -> None:
        label = ttk.Label(self.hand_frame, image=img)
        label.image = img  # Keep a reference - important!!!!
        label.grid(row=0, column=column)

    def _clear_hand_frame(self) -> None:
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

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
        # cards = self._get_checked_cards()
        # self._print_hand(cards)
        # copy(self.pbn.get())
        pass

    def _dismiss(self, *args) -> None:
        self.root.destroy()
