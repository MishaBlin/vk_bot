import random
import time
from functions import keyboards


def run_test(message_data, vk, ids_data):
    message_text = message_data[0]
    from_id = message_data[1]
    if ids_data[from_id]['test_question'] == 0:
        vk.messages.send(user_id=from_id,
                         message="Добро пожаловать в тест про котов!\nТест начинается!",
                         random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=from_id,
                         message="Первый вопрос: сколько у котов лап?",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        ids_data[from_id]['test_question'] += 1
    elif ids_data[from_id]['test_question'] == 1:
        time.sleep(1)
        if "4" in message_text or 'четыре' in message_text:
            vk.messages.send(user_id=from_id,
                             message="Верно!",
                             random_id=random.randint(0, 2 ** 64))
            ids_data[from_id]['score'] += 1
        else:
            vk.messages.send(user_id=from_id,
                             message="Неверно! У котов 4 лапы!",
                             random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=from_id,
                         message="Следующий вопрос: каково минимальное количество часов сна у котов в сутки?",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        ids_data[from_id]['test_question'] += 1
    elif ids_data[from_id]['test_question'] == 2:
        time.sleep(1)
        if "12" in message_text or 'двенадцать' in message_text:
            vk.messages.send(user_id=from_id,
                             message="Верно! Коты спят от 12 до 16 часов в день!",
                             random_id=random.randint(0, 2 ** 64))
            ids_data[from_id]['score'] += 1
        else:
            vk.messages.send(user_id=from_id,
                             message="Неверно! Коты спят от 12 до 16 часов в день!",
                             random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=from_id,
                         message="Последний вопрос: сколько существует пород кошек?",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        ids_data[from_id]['test_question'] += 1

    elif ids_data[from_id]['test_question'] == 3:
        time.sleep(1)
        if "300" in message_text or 'триста' in message_text:
            vk.messages.send(user_id=from_id,
                             message="Верно! Существует около 300 пород кошек!",
                             random_id=random.randint(0, 2 ** 64))
            ids_data[from_id]['score'] += 1
        else:
            vk.messages.send(user_id=from_id,
                             message="Неверно! Существует около 300 пород кошек!",
                             random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        ids_data[from_id]['test_active'] = False
        ids_data[from_id]['test_question'] = 0
        vk.messages.send(user_id=from_id,
                         message=f"Тест закончен!\n"
                                 f"Вы набрали {ids_data[from_id]['score']} баллов из 3!",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        if ids_data[from_id]['score'] == 3:
            time.sleep(1)
            user = vk.users.get(user_id=from_id, fields='sex')[0]
            if 'sex' in user:
                if user['sex'] == 2:
                    vk.messages.send(user_id=from_id,
                                     message=f"Вы молодец!",
                                     random_id=random.randint(0, 2 ** 64))
                elif user['sex'] == 1:
                    vk.messages.send(user_id=from_id,
                                     message=f"Вы умница!",
                                     random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=from_id,
                                 message=f"Вы молодец!",
                                 random_id=random.randint(0, 2 ** 64))
        ids_data[from_id]['score'] = 0
