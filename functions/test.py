import random
import num2words
from functions import keyboards, fallback


def start(from_id, vk):
    vk.messages.send(user_id=from_id,
                     message="Добро пожаловать в тест про котов!\nТест начинается! "
                             'Вы можете прервать тест командой "Выход"',
                     random_id=random.randint(0, 2 ** 64))


def ask(ids_data, from_id, vk, question):
    vk.messages.send(user_id=from_id,
                     message=question,
                     random_id=random.randint(0, 2 ** 64),
                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
    ids_data[from_id]['test_question'] += 1


def check(ids_data, from_id, message_text, vk, correct_answer, result_on_correct, result_on_wrong):
    try:
        if correct_answer in message_text or num2words.num2words(int(correct_answer), lang='ru') in message_text:
            vk.messages.send(user_id=from_id,
                             message=result_on_correct,
                             random_id=random.randint(0, 2 ** 64))
            ids_data[from_id]['score'] += 1
        else:
            vk.messages.send(user_id=from_id,
                             message=result_on_wrong,
                             random_id=random.randint(0, 2 ** 64))
    except Exception:
        vk.messages.send(user_id=from_id,
                         message=result_on_wrong,
                         random_id=random.randint(0, 2 ** 64))


def end(ids_data, from_id, vk):
    ids_data[from_id]['test_active'] = False
    ids_data[from_id]['test_question'] = 0
    vk.messages.send(user_id=from_id,
                     message=f"Тест закончен!\n"
                             f"Вы набрали {ids_data[from_id]['score']} баллов из 9!",
                     random_id=random.randint(0, 2 ** 64),
                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
    if ids_data[from_id]['score'] > 4:
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


def check_fallback(message_text, ids_data, from_id, vk):
    if "выход" in message_text:
        fallback.fallback(ids_data, from_id, vk, ("test_active",))
        ids_data[from_id]["score"] = 0
        ids_data[from_id]["test_question"] = 0
        return None
    return True


def run_test(message_data, vk, ids_data):
    message_text = message_data[0]
    from_id = message_data[1]
    if check_fallback(message_text, ids_data, from_id, vk) is None:
        return None
    test_question = ids_data[from_id]['test_question']

    if test_question == 0:
        start(from_id, vk)
        ask(ids_data, from_id, vk, "Сколько у котов лап?")

    elif test_question == 1:
        check(ids_data, from_id, message_text, vk, '4', 'Верно!', 'Неверно! У котов 4 лапы!')
        ask(ids_data, from_id, vk, "Следующий вопрос: каково минимальное количество часов сна у котов в сутки?")

    elif test_question == 2:
        check(ids_data, from_id, message_text, vk, '12', 'Верно! Коты спят от 12 до 16 часов в день!',
              'Неверно! Коты спят от 12 до 16 часов в день!')
        ask(ids_data, from_id, vk, "Следующий вопрос: сколько существует пород кошек?")

    elif test_question == 3:
        check(ids_data, from_id, message_text, vk, '300', 'Верно! Существует около 300 пород кошек!',
              'Неверно! Существует около 300 пород кошек!')
        ask(ids_data, from_id, vk, "Следующий вопрос: как называется наука, изучающая кошек?")

    elif test_question == 4:
        check(ids_data, from_id, message_text, vk, 'фелинология', 'Верно!',
              'Неверно! Наука, изучающая кошек называется фелинология!')
        ask(ids_data, from_id, vk, "Следующий вопрос: разновидностью какой дикой кошки является пантера?")

    elif test_question == 5:
        check(ids_data, from_id, message_text, vk, 'леопарда', 'Верно!',
              'Неверно! Пантера является разновидностью леопарда!')
        ask(ids_data, from_id, vk, "Следующий вопрос: какую дикую кошку использовали в качестве помощника на охоте?")
    elif test_question == 6:
        check(ids_data, from_id, message_text, vk, 'гепарда', 'Верно!',
              'Неверно! В качестве помощника на охоте использовали гепарда!')
        ask(ids_data, from_id, vk, "Следующий вопрос: какой вкус кошка различает лучше всего?")

    elif test_question == 7:
        check(ids_data, from_id, message_text, vk, 'горький', 'Верно!',
              'Неверно! Кошка лучше всего различает горький вкус!')
        ask(ids_data, from_id, vk, "Бывают ли у кошек молочные зубы?")

    elif test_question == 8:
        check(ids_data, from_id, message_text, vk, 'да', 'Верно!',
              'Неверно! У кошек есть молочные зубы!')
        ask(ids_data, from_id, vk, "Последний вопрос: Как понять что кошка рада Вас видеть?")

    elif test_question == 9:
        check(ids_data, from_id, message_text, vk, 'вверх', 'Верно!',
              'Неверно! Когда кошка рада вас видеть, её хвост поднимается вверх!')
        end(ids_data, from_id, vk)
