from aiogram import types, Dispatcher
from keyboards import kb_client
from create_bot import bot


async def echo_send(message: types.Message):
    await bot.send_message(message.from_user.id, 'Бот для сброса пароля\n'
                                                 'для начала наберите команду "сброс"',
                           reply_markup=kb_client)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
