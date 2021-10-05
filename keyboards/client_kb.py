from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove


b1 = KeyboardButton('/start')
b2 = KeyboardButton('/help')
b3 = KeyboardButton('/сброс')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).insert(b2).add(b3)
