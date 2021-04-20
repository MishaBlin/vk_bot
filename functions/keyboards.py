from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def _answer_options_for_test(opt1, opt2, opt3, opt4):
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button(opt1, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(opt2, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(opt3, color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(opt4, color=VkKeyboardColor.SECONDARY)
    return keyboard


def new_keyboard(from_id, ids_data):
    test_question = ids_data[from_id]["test_question"]
    test_active = ids_data[from_id]["test_active"]
    reminder_manage = ids_data[from_id]["reminder_manage"]
    keyboard = VkKeyboard(one_time=False)
    if test_active:
        if test_question == 0:
            keyboard = _answer_options_for_test('4 лапы', '5 лап', '12 лап', '8 лап')
        elif test_question == 1:
            keyboard = _answer_options_for_test('2 часа', '8 часов', '24 часа', '12 часов')
        elif test_question == 2:
            keyboard = _answer_options_for_test('500 пород', '300 пород', '1000 пород', '700 пород')

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
