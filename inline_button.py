from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def inlinemarkups(text: list, callback: list, align: list = None) -> InlineKeyboardMarkup:
    keybd = InlineKeyboardMarkup()
    if not align:
        for button in range(len(text)):
            keybd.add(
                InlineKeyboardButton(
                    text=text[button],
                    callback_data=callback[button]
                )
            )
    else:
        for row in align:
            rows = []
            for _ in range(row):
                try:
                    rows.append(InlineKeyboardButton(text=text.pop(0),
                                                     callback_data=callback.pop(0)))
                except:
                    print("Wrong align!")
            keybd.row(*rows)
    return keybd


def commmarkups(buts: list, align: list = None) -> ReplyKeyboardMarkup:
    keybd = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    if not align:
        for text in buts:
            keybd.add(KeyboardButton(str(text)))
    else:
        for rows in align:
            row = []
            for text in range(rows):
                row.append(KeyboardButton(str(buts.pop(0))))
            keybd.add(*row)
    return keybd


SOLVE = {
    "ru": "Решить Судоку",
    "en": "Solve Sudoku"
}
INFO = {
    "ru": "ℹ️Как использовать",
    "en": "ℹ️How to use"
}
LANGUAGE = {
    "ru": "🇷🇺 Сменить язык",
    "en": "🇬🇧 Set language"
}


def menu(lang):
    return commmarkups(
        buts=[SOLVE[lang],
              INFO[lang], LANGUAGE[lang]],
        align=[1, 2]
    )
