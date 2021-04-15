import time

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def prints(event):
    print(event.obj.message)
    print(event)
    print('New message:')
    print('From id:', event.obj.message['from_id'])
    print('Text:', event.obj.message['text'])


def run_test(event, vk):
    global test_question, score, test_active
    message_text = event.obj.message['text'].lower()
    if test_question == 0:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message="Добро пожаловать в тест про котов!\nТест начинается!",
                         random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message="Первый вопрос: сколько у котов лап?",
                         random_id=random.randint(0, 2 ** 64))
        test_question += 1
    elif test_question == 1:
        time.sleep(1)
        if "4" in message_text or 'четыре' in message_text:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Верно!",
                             random_id=random.randint(0, 2 ** 64))
            score += 1
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Неверно! У котов 4 лапы!",
                             random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message="Следующий вопрос: каково минимальное количество часов сна у котов в сутки?",
                         random_id=random.randint(0, 2 ** 64))
        test_question += 1
    elif test_question == 2:
        time.sleep(1)
        if "12" in message_text or 'двенадцать' in message_text:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Верно! Коты спят от 12 до 16 часов в день!",
                             random_id=random.randint(0, 2 ** 64))
            score += 1
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Неверно! Коты спят от 12 до 16 часов в день!",
                             random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message="Последний вопрос: сколько существует пород кошек?",
                         random_id=random.randint(0, 2 ** 64))
        test_question += 1

    elif test_question == 3:
        time.sleep(1)
        if "300" in message_text or 'триста' in message_text:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Верно! Существует около 300 пород кошек!",
                             random_id=random.randint(0, 2 ** 64))
            score += 1
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Неверно! Существует около 300 пород кошек!",
                             random_id=random.randint(0, 2 ** 64))
        time.sleep(1)
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message=f"Тест закончен! Вы набрали {score} баллов из 3!",
                         random_id=random.randint(0, 2 ** 64))
        if score == 3:
            time.sleep(1)
            user = vk.users.get(user_id=event.obj.message['from_id'], fields='sex')[0]
            print(user)
            if 'sex' in user:
                if user['sex'] == 2:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Вы молодец!",
                                     random_id=random.randint(0, 2 ** 64))
                elif user['sex'] == 1:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Вы умница!",
                                     random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вы молодец!",
                                 random_id=random.randint(0, 2 ** 64))
        score = 0
        test_question = 0
        test_active = False


def get_random_fact():
    with open('facts.txt', 'r', encoding='utf8') as file:
        data = file.readlines()
        print(data)
    return random.choice(data)


def get_random_atch():
    login, password = '89129858385', 'MihailkaOther2'
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)

    try:
        vk_session.auth(token_only=True, )
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    wall = tools.get_all('wall.get', 100, {'owner_id': -203940448})
    return random.choice(wall['items'])['attachments'][-1]['photo']


TOKEN = "c93668582bede75b8ae9c46c6083476ebfe645d602d77df334e7f3e02cfc463f5f7f75b1a93a5cb39b1f7"
vk_session = vk_api.VkApi(token=TOKEN, auth_handler=auth_handler)
test_question = 0
score = 0
test_active = False


def main():
    global test_active
    longpoll = VkBotLongPoll(vk_session, "203940448")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if test_active:
                run_test(event, vk)
            else:
                prints(event)
                user = vk.users.get(user_id=event.obj.message['from_id'])[0]
                print(f'user: {user}')

                try:
                    message_text = event.obj.message['text'].lower()
                    if 'help' in message_text:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="""
                                                 Доступные команды:
                                                 'Картинка' — получить случайную картинку кота,
                                                 'Факт' — получить случайный факт о котах,
                                                 'Тест' — пройти тест про котов.
                                                 """,
                                         random_id=random.randint(0, 2 ** 64))

                    elif 'картинка' in message_text:
                        photo = get_random_atch()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Случайная картинка: ",
                                         attachment=f'photo{photo["owner_id"]}_{photo["id"]}',
                                         random_id=random.randint(0, 2 ** 64))

                    elif 'факт' in message_text:
                        fact = get_random_fact()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Случайный факт про котов: {fact}",
                                         random_id=random.randint(0, 2 ** 64))

                    elif 'тест' in message_text:
                        test_active = True
                        run_test(event, vk)

                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='''Извините, я Вас не понимаю.
                                                 Чтобы посмотреть список команд введите "help"''',
                                         random_id=random.randint(0, 2 ** 64))
                except Exception as e:
                    print(e)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='''Возникла ошибка на стороне сервера.
                                                Чтобы посмотреть список команд введите "help"''',
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
