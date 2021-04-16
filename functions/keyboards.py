from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def _answer_options_for_test(opt1, opt2, opt3, opt4):
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button(opt1, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(opt2, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(opt3, color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(opt4, color=VkKeyboardColor.SECONDARY)
    return keyboard


def new_keyboard(event, ids_data):
    test_question = ids_data[event.obj.message['from_id']]["test_question"]
    test_active = ids_data[event.obj.message['from_id']]["test_active"]
    if test_active:
        if test_question == 0:
            keyboard = _answer_options_for_test('4 лапы', '5 лап', '12 лап', '8 лап')
        elif test_question == 1:
            keyboard = _answer_options_for_test('2 часа', '8 часов', '24 часа', '12 часов')
        elif test_question == 2:
            keyboard = _answer_options_for_test('500 пород', '300 пород', '1000 пород', '700 пород')
    else:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Картинка", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button("Факт", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Тест", color=VkKeyboardColor.PRIMARY)

    return keyboard