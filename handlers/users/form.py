from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from dbsrc import TableUser
from utils.db_api.dbutils import add_user_to_db
from dbsrc import DataAccessLayer
from data.config import conn_string
from loader import dp
from states.form import Form

dal = DataAccessLayer(conn_string)
session = dal.get_session()


@dp.message_handler(Command("form"))
async def enter_form(message: types.Message):
    msg = """
    Заполните анкету 
    """
    await message.answer(msg)
    await message.answer("Введите имя\n")
    await Form.Q1.set()


@dp.message_handler(state = Form.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1 = answer)
    await message.answer("Введите email \n")
    await Form.next()


@dp.message_handler(state = Form.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer2 = answer)
    await message.answer("Введите ключевые слова для поиска вакансий \n")
    await Form.next()


@dp.message_handler(state = Form.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = message.text

    rec = TableUser(
        user_id = message.from_user,
        user_name = answer1,
        user_email = answer2,
        user_keywords = answer3
    )

    add_user_to_db(rec, session)

    await message.answer("Отлично! Регистрация прошла успешно! ")
    await message.answer(f"Имя - {answer1}")
    await message.answer(f"Email - {answer2}")
    await message.answer(f"Ключевые слова - {answer3}")

    await state.reset_state()
