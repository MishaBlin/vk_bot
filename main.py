import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from functions import random_picture, random_fact, test, keyboards


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


TOKEN = "c93668582bede75b8ae9c46c6083476ebfe645d602d77df334e7f3e02cfc463f5f7f75b1a93a5cb39b1f7"
vk_session = vk_api.VkApi(token=TOKEN, auth_handler=auth_handler)

ids_data = {}


def main():
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, "203940448")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['from_id'] not in ids_data:
                ids_data[event.obj.message['from_id']] = {'test_active': False, "score": 0, "test_question": 0}
            if ids_data[event.obj.message['from_id']]["test_active"]:
                test.run_test(event, vk, ids_data)
            else:
                try:
                    message_text = event.obj.message['text'].lower()
                    if 'help' in message_text:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Доступные команды:\n'Картинка' — получить случайную картинку кота,"
                                                 "\n'Факт' — получить случайный факт о котах,\n'Тест' — пройти тест "
                                                 "про котов.",
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=keyboards.new_keyboard(event, ids_data).get_keyboard())

                    elif 'картинка' in message_text:
                        random_picture.send_photo(event, vk, keyboards.new_keyboard(event, ids_data))

                    elif 'факт' in message_text:
                        random_fact.send_fact(event, vk, keyboards.new_keyboard(event, ids_data))

                    elif 'тест' in message_text:
                        ids_data[event.obj.message['from_id']]["test_active"] = True
                        test.run_test(event, vk, ids_data)

                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Извините, я Вас не понимаю.\nЧтобы посмотреть список команд введите '
                                                 '"help".',
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=keyboards.new_keyboard(event, ids_data).get_keyboard())
                except Exception as e:
                    print(e)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Возникла ошибка на стороне сервера.\nЧтобы посмотреть список команд '
                                             'введите "help".',
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=keyboards.new_keyboard(event, ids_data).get_keyboard())


if __name__ == '__main__':
    main()
