from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from dbsrc import TableUser
from utils.db_api.dbutils import add_user_to_db, session
from loader import dp
from states.form import Form
import logging
logging.basicConfig(level="INFO")


@dp.message_handler(Command("keywords"))
async def enter_form(message: types.Message):
    msg = """
    Для того чтобы найти релевантные вакансии необходимо указать ключевые слова для поиска
    """
    await message.answer(msg)
    await message.answer("Укажите ключевые слова \n")
    await Form.Q1.set()


@dp.message_handler(state = Form.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    rec = TableUser(
        user_id = message.from_user.id,
        user_name = message.from_user.full_name,
        user_keywords = answer,
        user_email = "email"
    )


    add_user_to_db(rec)
    await message.answer("Ключевые слова успешно добавлены! ")
    await state.reset_state()



