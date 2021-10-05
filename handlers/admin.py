from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from connection.connection import connect_to_ad, user_search_ad, reset_pass


class FSMAdmin(StatesGroup):
    admin_user = State()
    admin_passwd = State()
    user = State()


# @dp.message_handler(commands='сброс', state=None)
async def cm_reset(message: types.Message):
    await FSMAdmin.admin_user.set()
    await message.reply('Введите логин админа')


# @dp.message_handler(state=FSMAdmin.admin_user)
async def admin_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_user'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введи пароль админа')


# @dp.message_handler(state=FSMAdmin.admin_passwd)
async def admin_passwd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_passwd'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи логин юзера для сброса пароля')


# @dp.message_handler(state=FSMAdmin.user)
async def user_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = message.text
        await message.reply('Все данные приняты')
        conn = connect_to_ad(data['admin_user'], data['admin_passwd'])
        if conn is None or not conn.bind():
            await message.answer('Нет соединения с сервером AD')
            await state.finish()
        else:
            await message.answer('Соединение с сервером установлено')
            user = user_search_ad(data['user'], conn)
            if not user:
                await message.answer('Нет такого юзера')
                await state.finish()
            else:
                await message.answer(f'Пользователь найден\n{user}')
                if reset_pass(user, conn):
                    await state.finish()
                    await message.answer('Пароль сброшен')
                else:
                    await state.finish()
                    await message.answer('Что-то пошло не так')


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_reset, commands=['сброс'], state=None)
    dp.register_message_handler(admin_login, state=FSMAdmin.admin_user)
    dp.register_message_handler(admin_passwd, state=FSMAdmin.admin_passwd)
    dp.register_message_handler(user_search, state=FSMAdmin.user)
