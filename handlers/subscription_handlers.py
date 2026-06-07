"""
Обработчики сообщений VK-бота.

Файл содержит:
- обработку команд пользователя;
- управление состояниями FSM;
- взаимодействие с сервисным слоем;
- формирование ответов пользователю.
"""

from vkbottle.bot import Bot
from vkbottle.bot import Message

from config.config import TOKEN

from keyboards.main_keyboard import (
    get_main_keyboard
)

from services.subscription_service import (
    SubscriptionService
)

from storage.database import JsonDatabase
from storage.state_storage import (
    StateStorage
)

from states.subscription_states import (
    UserState
)


# Создание экземпляра бота
bot = Bot(token=TOKEN)

# Инициализация базы данных
database = JsonDatabase(
    "storage/subscriptions.json"
)

# Инициализация сервисного слоя
service = SubscriptionService(database)

# Хранилище состояний пользователей
state_storage = StateStorage()


@bot.on.message()
async def message_handler(message: Message):
    """
    Главный обработчик сообщений.

    В зависимости от состояния пользователя
    выполняет нужное действие:
    - добавление подписки;
    - удаление подписки;
    - изменение стоимости;
    - оплата подписки;
    - просмотр информации.
    """

    if not message.text:
        return

    # Приведение текста к нижнему регистру
    text = message.text.strip().lower()

    user_id = message.from_id

    # Получение текущего состояния пользователя
    state = state_storage.get_state(
        user_id
    )

    # =====================================
    # Команда запуска бота
    # =====================================

    if text in [
        "начать",
        "старт",
        "/start"
    ]:

        state_storage.clear_state(
            user_id
        )

        await message.answer(
            "Менеджер подписок запущен.",
            keyboard=get_main_keyboard()
        )

        return

    # =====================================
    # Команда помощи
    # =====================================

    if text == "помощь":

        await message.answer(
            "Доступные действия:\n\n"
            "• Добавить\n"
            "• Удалить\n"
            "• Изменить\n"
            "• Оплатить\n"
            "• Список\n"
            "• Долги\n"
            "• Расходы",
            keyboard=get_main_keyboard()
        )

        return

    # =====================================
    # Добавление подписки
    # =====================================

    if text == "добавить":

        state_storage.set_state(
            user_id,
            UserState.ADD_NAME
        )

        await message.answer(
            "Введите название подписки:"
        )

        return

    # Ожидание названия подписки
    if state == UserState.ADD_NAME:

        name = message.text.strip()

        if len(name) < 2:

            await message.answer(
                "Название слишком короткое."
            )

            return

        state_storage.temp_data[
            user_id
        ] = {
            "name": name
        }

        state_storage.set_state(
            user_id,
            UserState.ADD_PRICE
        )

        await message.answer(
            "Введите стоимость подписки:"
        )

        return

    # Ожидание стоимости подписки
    if state == UserState.ADD_PRICE:

        try:
            price = int(message.text)

        except ValueError:

            await message.answer(
                "Введите числовую стоимость."
            )

            return

        name = (
            state_storage
            .temp_data[user_id]["name"]
        )

        new_id = (
            service.create_subscription(
                name,
                price
            )
        )

        state_storage.clear_state(
            user_id
        )

        await message.answer(
            f"Подписка успешно добавлена.\n"
            f"ID: {new_id}",
            keyboard=get_main_keyboard()
        )

        return

    # =====================================
    # Удаление подписки
    # =====================================

    if text == "удалить":

        state_storage.set_state(
            user_id,
            UserState.DELETE_SELECT
        )

        await message.answer(
            "Введите ID подписки:"
        )

        return

    # Ожидание ID удаляемой подписки
    if state == UserState.DELETE_SELECT:

        try:
            subscription_id = int(
                message.text
            )

        except ValueError:

            await message.answer(
                "Введите числовой ID."
            )

            return

        result = (
            service.delete_subscription(
                subscription_id
            )
        )

        state_storage.clear_state(
            user_id
        )

        if result:

            await message.answer(
                "Подписка удалена.",
                keyboard=get_main_keyboard()
            )

        else:

            await message.answer(
                "Подписка не найдена.",
                keyboard=get_main_keyboard()
            )

        return

    # =====================================
    # Оплата подписки
    # =====================================

    if text == "оплатить":

        state_storage.set_state(
            user_id,
            UserState.PAY_SELECT
        )

        await message.answer(
            "Введите ID подписки:"
        )

        return

    # Ожидание ID оплачиваемой подписки
    if state == UserState.PAY_SELECT:

        try:
            subscription_id = int(
                message.text
            )

        except ValueError:

            await message.answer(
                "Введите числовой ID."
            )

            return

        result = (
            service.pay_subscription(
                subscription_id
            )
        )

        state_storage.clear_state(
            user_id
        )

        if result:

            await message.answer(
                "Подписка оплачена.",
                keyboard=get_main_keyboard()
            )

        else:

            await message.answer(
                "Подписка не найдена.",
                keyboard=get_main_keyboard()
            )

        return

    # =====================================
    # Изменение стоимости подписки
    # =====================================

    if text == "изменить":

        state_storage.set_state(
            user_id,
            UserState.UPDATE_SELECT
        )

        await message.answer(
            "Введите ID подписки:"
        )

        return

    # Ожидание ID подписки
    if state == UserState.UPDATE_SELECT:

        try:
            subscription_id = int(
                message.text
            )

        except ValueError:

            await message.answer(
                "Введите числовой ID."
            )

            return

        subscription = (
            service.get_subscription_by_id(
                subscription_id
            )
        )

        if subscription is None:

            state_storage.clear_state(
                user_id
            )

            await message.answer(
                "Подписка не найдена.",
                keyboard=get_main_keyboard()
            )

            return

        state_storage.temp_data[
            user_id
        ] = {
            "subscription_id":
                subscription_id
        }

        state_storage.set_state(
            user_id,
            UserState.UPDATE_PRICE
        )

        await message.answer(
            "Введите новую стоимость:"
        )

        return

    # Ожидание новой стоимости
    if state == UserState.UPDATE_PRICE:

        try:
            new_price = int(
                message.text
            )

        except ValueError:

            await message.answer(
                "Введите числовое значение."
            )

            return

        subscription_id = (
            state_storage
            .temp_data[user_id]
            ["subscription_id"]
        )

        result = (
            service.update_price(
                subscription_id,
                new_price
            )
        )

        state_storage.clear_state(
            user_id
        )

        if result:

            await message.answer(
                "Стоимость изменена.",
                keyboard=get_main_keyboard()
            )

        else:

            await message.answer(
                "Ошибка изменения.",
                keyboard=get_main_keyboard()
            )

        return

    # =====================================
    # Вывод списка подписок
    # =====================================

    if text == "список":

        subscriptions = (
            service.get_all_subscriptions()
        )

        if not subscriptions:

            await message.answer(
                "Подписок пока нет.",
                keyboard=get_main_keyboard()
            )

            return

        response = (
            "Ваши подписки:\n\n"
        )

        for sub in subscriptions:

            status = (
                "Оплачена"
                if sub["paid"]
                else "Не оплачена"
            )

            response += (
                f"ID: {sub['id']}\n"
                f"Название: {sub['name']}\n"
                f"Цена: {sub['price']} ₽\n"
                f"Статус: {status}\n\n"
            )

        await message.answer(
            response,
            keyboard=get_main_keyboard()
        )

        return

    # =====================================
    # Просмотр неоплаченных подписок
    # =====================================

    if text == "долги":

        debts = (
            service.get_unpaid_subscriptions()
        )

        if not debts:

            await message.answer(
                "Все подписки оплачены.",
                keyboard=get_main_keyboard()
            )

            return

        response = (
            "Неоплаченные подписки:\n\n"
        )

        for sub in debts:

            response += (
                f"ID: {sub['id']} | "
                f"{sub['name']} | "
                f"{sub['price']} ₽\n"
            )

        await message.answer(
            response,
            keyboard=get_main_keyboard()
        )

        return

    # =====================================
    # Общие расходы
    # =====================================

    if text == "расходы":

        total = (
            service.get_total_cost()
        )

        await message.answer(
            f"Общая сумма расходов: "
            f"{total} ₽",
            keyboard=get_main_keyboard()
        )

        return

    # =====================================
    # Неизвестная команда
    # =====================================

    await message.answer(
        "Неизвестная команда.\n"
        "Нажмите «Помощь».",
        keyboard=get_main_keyboard()
    )

