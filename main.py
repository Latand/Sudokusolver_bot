import asyncio
import logging
import config
import aiogram
from inline_button import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from languages import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from messages import texts as imported_text
from states import ALL_STATES as STATE
from solver import solve_puzzle

WEBHOOK_PATH = f'/{config.TOKEN}'
WEBHOOK_URL = f"https://{config.WEBHOOK_HOST}{WEBHOOK_PATH}/"

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = config.PORT

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, loop=loop, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def starting(message: types.Message):
    chat_id = message.chat.id

    lang = get_language(chat_id)
    await bot.send_message(chat_id,
                           imported_text[lang]["start"],
                           reply_markup=inlinemarkups(
                               text=["English", "Русский"],
                               callback=["language en start", "language ru start"]
                           ))


@dp.callback_query_handler(func=lambda call: "language" in call.data)
async def change_language(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    except aiogram.utils.exceptions.MessageNotModified:
        pass
    language = call.data.split()[1]
    set_language(chat_id, language)

    await bot.send_message(chat_id, imported_text[language]["changed"],
                           reply_markup=menu(language))


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    text = imported_text[lang]["explain"]
    await bot.send_message(chat_id, text)

# DESCRIBE BOT ---------------------------------------------------------------------------------------------


@dp.message_handler(commands=["set_language"])
async def lang_choose(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)

    try:
        await bot.send_message(chat_id,
                               imported_text[lang]["start"],
                               reply_markup=inlinemarkups(
                                   text=["English", "Русский"],
                                   callback=["language en", "language ru"]
                               ))
    except aiogram.utils.exceptions.CantParseEntities as err:
        print(f"Error. {err.__class__.__name__}: {err}")


@dp.message_handler(func=lambda m: m.text in SOLVE.values())
async def solve_(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, imported_text[lang]["enter"])
    await dp.current_state().set_state(STATE.SOLVE)
    #
@dp.message_handler(func=lambda m: m.text in INFO.values())
async def solve_(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, imported_text[lang]["explain"])


@dp.message_handler(state=STATE.SOLVE)
async def solve_(message: types.Message):
    chat_id = message.chat.id
    lang = get_language(chat_id)

    solved = solve_puzzle(message.text)
    if isinstance(solved, str):
        await bot.send_message(chat_id, imported_text[lang]["wrong"].format(solved))
    else:
        await bot.send_photo(chat_id, photo=solved)
    await dp.current_state().reset_state()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def unknown(message: types.Message):

    chat_id = message.chat.id
    lang = get_language(chat_id)
    await bot.send_message(chat_id, "OOPS")


async def throttling_message(user):
    try:
        await dp.throttle(str(user), rate=1)
    except Throttled:
        await bot.send_message(user, "Too fast. Try again in 1 sec")
        return True


async def on_startup(dp):
    return print(await bot.set_webhook(url=WEBHOOK_URL))


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path="",
                  skip_updates=False, host=WEBAPP_HOST, port=WEBAPP_PORT, on_startup=on_startup)
