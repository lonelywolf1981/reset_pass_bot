from aiogram.dispatcher.filters import Text
# from ldap3 import Server, Connection, SUBTREE, ALL
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp


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
    # async with state.proxy() as data:

    await state.finish()


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

    # AD_SERVER = 'kmf.local'
    # AD_SEARCH_TREE = 'dc=kmf,dc=local'
    # USER_DN = ''

    # await message.reply(data['admin_user'])
    #
    # user = 'kmf\\' + str(data['admin_user'])
    # pwd = str(data['admin_passwd'])
    # await message.answer(user, pwd)
    # server = Server(AD_SERVER, get_info=ALL, use_ssl=True)
    # conn = Connection(server, user=user, password=pwd, auto_bind=True)
    # if not conn.bind():
    #     await message.answer('Нет связи с сервером!')
    #     await state.finish()
    # else:
    #     SEARCHFILTER = '(&(|(sAMAccountname=' + data['user'] + '))(objectClass=person))'
    #     await conn.search(search_base=AD_SEARCH_TREE, search_filter=SEARCHFILTER, search_scope=SUBTREE,
    #                       attributes=['cn', 'givenName'], paged_size=5)
    #     for entry in conn.response:
    #         if entry.get("dn") and entry.get("attributes"):
    #             if entry.get("attributes").get("cn"):
    #                 USER_DN = entry.get("dn")
    #
    #     await message.answer(f'Юзер найден\n{USER_DN}')
    #     if conn.extend.microsoft.modify_password(USER_DN, '123qweASD'):
    #         await message.answer('Пароль заменен на стандартный')
    #     else:
    #         await message.answer('Что-то пошло не так?!')
