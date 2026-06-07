from vkbottle import Keyboard
from vkbottle import Text


def get_main_keyboard():

    keyboard = Keyboard(
        one_time=False
    )

    keyboard.add(Text("Добавить"))
    keyboard.add(Text("Удалить"))
    keyboard.row()

    keyboard.add(Text("Изменить"))
    keyboard.add(Text("Оплатить"))
    keyboard.row()

    keyboard.add(Text("Список"))
    keyboard.add(Text("Долги"))
    keyboard.row()

    keyboard.add(Text("Расходы"))
    keyboard.add(Text("Помощь"))

    return keyboard.get_json()