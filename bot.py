import logging, asyncio, os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from api import parse_vacancies, save_data_to_db

API_TOKEN = os.getenv('API_TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)

# Определение состояний для finite state machine (FSM)
class Form(StatesGroup):
    salary = State()
    schedule = State()
    experience = State()
    text_to_find = State()

# Хендлер для команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.salary)
    await message.answer("Это бот для парсинга данных. Введите желаемую зарплату")

# Хендлер для ввода желаемой зарплаты
@router.message(Form.salary)
async def process_salary(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(Form.schedule)
    await message.answer('''
Укажите желаемый рабочий график:
<code>full</code> - полная занятость
<code>part</code> - частичная занятость
<code>project</code> - проектная работа
<code>volunteer</code> - волонтерство
<code>probation</code> - стажировка
''', parse_mode='html')

# Хендлер для ввода рабочего графика
@router.message(Form.schedule)
async def process_schedule(message: Message, state: FSMContext):
    await state.update_data(schedule=message.text)
    await state.set_state(Form.experience)
    await message.answer('''
Укажите желаемый рабочий график:
<code>noExperience</code> - Нет опыта
<code>between1And3</code> - От 1 года до 3 лет
<code>between3And6</code> - От 3 до 6 лет
<code>moreThan6</code> - Более 6 лет
''', parse_mode='html')

# Хендлер для ввода опыта работы
@router.message(Form.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Form.text_to_find)
    await message.answer("Введите текст, который должен присутстовать в вакансии")

# Хендлер для ввода искомого текста
@router.message(Form.text_to_find)
async def process_text_to_find(message: Message, state: FSMContext):
    await state.update_data(text_to_find=message.text)
    data = await state.get_data()

    data = parse_vacancies(data['text_to_find'], data['salary'], data['schedule'], data['experience'])

    ans = 'Доступные вакансии:'
    await message.answer(ans)
    save_data_to_db(data)
    for vacancy in data:
        await message.answer(f'ID: {vacancy[0]}\nНазвание: {vacancy[1]}\nГрафик: {vacancy[2]}\nЗанятость: {vacancy[3]}\nГород: {vacancy[4]}\n Опыт: {vacancy[5]}\nЗарплата: {vacancy[6]}')

    await state.clear()
    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
