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


def main():
    longpoll = VkBotLongPoll(vk_session, "203940448")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            prints(event)
            vk = vk_session.get_api()
            user = vk.users.get(user_id=event.obj.message['from_id'])[0]
            print(f'user: {user}')

            message_text = event.obj.message['text']

            try:
                if message_text.lower() == 'help':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="""
                                             Доступные команды:
                                             'Картинка' — получить случайную картинку кота,
                                             'Факт' — получить случайный факт о котах,
                                             """,
                                     random_id=random.randint(0, 2 ** 64))

                elif message_text.lower() == 'картинка':
                    photo = get_random_atch()
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Случайная картинка: ",
                                     attachment=f'photo{photo["owner_id"]}_{photo["id"]}',
                                     random_id=random.randint(0, 2 ** 64))

                elif message_text.lower() == 'факт':
                    fact = get_random_fact()
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Случайный факт про котов: {fact}",
                                     random_id=random.randint(0, 2 ** 64))

                elif message_text.lower() == 'тест':
                    pass

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
