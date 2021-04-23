import random

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# keyboard for test function
def _answer_options_for_test(options):
    keyboard = VkKeyboard(inline=True)
    buttons_in_line = 0
    for option in options:
        if buttons_in_line == 2 or (buttons_in_line > 0 and len(option) > 12):
            keyboard.add_line()
            buttons_in_line = 0
        keyboard.add_button(option, color=random.choice(
            [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.SECONDARY, VkKeyboardColor.NEGATIVE]))
        buttons_in_line += 1
    return keyboard


# main keyboard function
def new_keyboard(from_id, ids_data):
    test_question = ids_data[from_id]["test_question"]
    test_active = ids_data[from_id]["test_active"]
    reminder_manage = ids_data[from_id]["reminder_manage"]
    keyboard = VkKeyboard(one_time=False)
    if test_active:
        if test_question == 0:
            keyboard = _answer_options_for_test(('4 лапы', '5 лап', '12 лап', '8 лап'))
        elif test_question == 1:
            keyboard = _answer_options_for_test(('2 часа', '8 часов', '24 часа', '12 часов'))
        elif test_question == 2:
            keyboard = _answer_options_for_test(('500 пород', '300 пород', '1000 пород', '700 пород'))
        elif test_question == 3:
            keyboard = _answer_options_for_test(("Фелинология", "Кинология", "Котология", "Андриология"))
        elif test_question == 4:
            keyboard = _answer_options_for_test(("Гепарда", "Леопарда", "Тигра", "Льва"))
        elif test_question == 5:
            keyboard = _answer_options_for_test(("Гепарда", "Пантеру", "Леопарда", "Лесную кошку"))
        elif test_question == 6:
            keyboard = _answer_options_for_test(("Сладкий", "Солёный", "Кислый", "Горький "))
        elif test_question == 7:
            keyboard = _answer_options_for_test(("Да", "Нет", "Зависит от породы"))
        elif test_question == 8:
            keyboard = _answer_options_for_test(
                ("Кошка громко мяукает", "Кошка начинает шипеть", "Хвост кошки поднят вверх"))

    elif reminder_manage:
        keyboard.add_button("Создать", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("Удалить", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button("Мои напоминания", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Выход", color=VkKeyboardColor.SECONDARY)

    else:
        keyboard.add_button("Картинка", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button("Факт", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Центр напоминаний", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Тест", color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button("Переводчик", color=VkKeyboardColor.PRIMARY)

    return keyboard
