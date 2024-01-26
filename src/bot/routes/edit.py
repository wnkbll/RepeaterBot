from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from loguru import logger

from src.bot.callbacks import ChatsCallback
from src.bot.keyboards import ChatsKeyboard
from src.bot.filters import WhiteListFilter
from src.utils import Config, JsonReader, TimeValidator
from src.lang import STRINGS

lang = "ru"

config_path = "data/config.json"
data_path = "data/data.json"

router = Router()
router.message.filter(WhiteListFilter())


class EditState(StatesGroup):
    waiting_post = State()
    waiting_chat = State()


def get_key(dictionary: dict, index: int) -> str:
    for i, key in enumerate(dictionary.keys()):
        if i == index:
            return key


@router.message(EditState.waiting_chat)
async def waiting_chat(message: Message, state: FSMContext):
    user_data = await state.get_data()
    chats = Config(**JsonReader.read(config_path, False)).chats
    time = TimeValidator(message.text).validate_time()

    if time is None:
        await message.answer(STRINGS[lang]["bad_time"])
        logger.warning(STRINGS["debug"]["bad_time"].format(username=message.from_user.username))
        return None

    chats[get_key(chats, user_data["index"])] = time
    config = JsonReader.read(config_path, False)
    config["chats"] = chats
    JsonReader.write(config, config_path, False)

    await state.clear()


@router.callback_query(ChatsCallback.filter(F.action == "edit"))
async def edit_chat_callback(query: CallbackQuery, callback_data: ChatsCallback, state: FSMContext):
    await query.message.answer("Send new time.")
    await state.update_data(index=callback_data.index)
    await state.set_state(EditState.waiting_chat)


@router.message(Command("edit", "изменить", "редактировать"))
async def edit(message: Message, command: CommandObject):
    arguments = [
        "posts",
        "chats",
        "sleep",
        "посты",
        "чаты",
        "сон"
    ]

    if command.args not in arguments:
        await message.answer(STRINGS[lang]["unexpected_args"])
        logger.warning(STRINGS["debug"]["unexpected_args"].format(username=message.from_user.username))
        return None

    async def edit_posts():
        pass

    async def edit_chats():
        chats = Config(**JsonReader.read(config_path, False)).chats
        if len(chats) < 1:
            await message.answer(STRINGS[lang]["empty_chats"], parse_mode="Markdown")
            return None

        answer = ""
        for index, item in enumerate(chats.items()):
            answer += f"{index + 1}) {item[0]}: {item[1]}\n"

        builder = ChatsKeyboard(len(chats), "edit", chats).builder
        await message.answer(f"```\n{answer}```", parse_mode="Markdown", reply_markup=builder.as_markup())

    async def edit_sleep():
        pass

    argument = command.args

    actions = {
        "posts": edit_posts,
        "chats": edit_chats,
        "sleep": edit_sleep,
        "посты": edit_posts,
        "чаты": edit_chats,
        "сон": edit_sleep
    }

    await actions[argument]()
