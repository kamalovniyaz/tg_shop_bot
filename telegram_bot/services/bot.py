import asyncio
import re

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown as md
from decouple import config

from shop.models import Category, Subcategory, Product

# Объект бота
bot = Bot(token=config("TG_BOT_TOKEN"))
# Диспетчер
dp = Dispatcher()

user_data = {}


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(chat_id='@ozonmanager', user_id=user_id)

    if is_subscribed.status != 'left':
        kb = [
            [types.KeyboardButton(text="Каталог")],
            [types.KeyboardButton(text="Корзина")],
            [types.KeyboardButton(text="FAQ")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                             input_field_placeholder="Выберите действие")

        await message.answer("Добро пожаловать!", reply_markup=keyboard)
    else:
        await message.answer("Перед использованием бота подпишитесь на канал: @ozonmanager")


@dp.message(F.text.lower() == "каталог")
async def show_category(message: types.Message):
    category = Category.objects.all()
    kb = []

    for cat in category:
        kb.append([types.KeyboardButton(text=cat.name)])

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         input_field_placeholder="Выберите категорию")
    await message.answer("Выберите категорию", reply_markup=keyboard)


pattern = re.compile(r'^(Мужские|Женские) (футболки|шорты)$', re.IGNORECASE)


@dp.message(lambda message: pattern.match(message.text))
async def show_subcategory(message: types.Message):
    user_data[message.from_user.id] = {'category': message.text}

    subcategory = Subcategory.objects.filter(category__name=message.text)
    kb = []

    for sub_cat in subcategory:
        kb.append([types.KeyboardButton(text=sub_cat.name)])

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         input_field_placeholder="Выберите подкатегорию")
    await message.answer("Выберите подкатегорию", reply_markup=keyboard)


def create_product_keyboard(user_id, product_id, current_index, total_products):
    keyboard = InlineKeyboardMarkup()

    decrease_button = InlineKeyboardButton("-")

    count_button = InlineKeyboardButton(f"Количество")

    increase_button = InlineKeyboardButton("+")

    add_to_cart_button = InlineKeyboardButton("Добавить в корзину")

    next_product_button = InlineKeyboardButton("Следующий товар")

    keyboard.row(decrease_button, count_button, increase_button)
    keyboard.row(add_to_cart_button, next_product_button)

    return keyboard


@dp.message(lambda message: message.text in ["Футболки", "Шорты"])
async def show_catalog(message: types.Message):
    product = Product.objects.filter(subcategory__name=message.text,
                                     subcategory__category__name=user_data[message.from_user.id][
                                         'category']).first()
    print(product)
    message_text = md.text(
        md.text(product.name),
        md.text("Описание: ", product.description),
        md.text('Цена:', md.text(float(product.price)), " руб"),
        sep='\n'
    )
    user_id = message.from_user.id

    keyboard = create_product_keyboard(user_id=user_id, product_id=product.id, current_index=0,
                                       total_products=product.quantity)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=product.image_url,
        caption=message_text,
        reply_markup=keyboard,
    )


@dp.message(F.text.lower() == "корзина")
async def show_cart(message: types.Message):
    await message.answer("Ваша корзина")


@dp.message(F.text.lower() == "faq")
async def show_cart(message: types.Message):
    await message.answer("Ответы на частозадаваемые вопросы")


async def main():
    kb = [
        [types.KeyboardButton(text="/start")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await dp.start_polling(bot, reply_markup=keyboard)


def start_bot():
    asyncio.run(main())


if __name__ == "__main__":
    start_bot()
