from aiogram import types, Dispatcher
from keyboards import kb_client
from create_bot import bot


async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Бот для сброса пароля\n'
                                                     'для начала наберите команду "сброс"',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/reset_pass_bot')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
