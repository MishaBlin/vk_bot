import traceback

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from obscene_words_filter import get_default_filter
from functions import random_picture, random_fact, test, keyboards, reminder, translator


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


TOKEN = "c93668582bede75b8ae9c46c6083476ebfe645d602d77df334e7f3e02cfc463f5f7f75b1a93a5cb39b1f7"
vk_session = vk_api.VkApi(token=TOKEN, auth_handler=auth_handler)

ids_data = {}


def main():
    profanity_filter = get_default_filter()
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, "203940448")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            from_id = event.obj.message['from_id']
            message_text = event.obj.message['text'].lower()
            user = vk.users.get(user_id=from_id)[0]
            print(f"connected to user {user['first_name']} {user['last_name']}")
            if from_id not in ids_data:
                ids_data[from_id] = {'test_active': False,
                                     "score": 0,
                                     "test_question": 0,
                                     'reminder_manage': False,
                                     'reminders': [],
                                     'first_run': True,
                                     'creation': False,
                                     'getting_times': False,
                                     'amount_of_feeds': 0,
                                     'deleting_reminders': False,
                                     'translation_mode': False,
                                     'profanity': 0}
            try:
                if profanity_filter.is_word_bad(message_text):
                    if ids_data[from_id]['profanity'] == 0:
                        vk.messages.send(user_id=from_id,
                                         message='Своими словами вы позорите честь и достоинство всех членов кошачьей '
                                                 'группы! '
                                                 'Разве не стыдно вам сквернословить в присутствии котов, '
                                                 'вы бессовестный, '
                                                 'жалкий и просто омерзительный человек. Если подобные выражения будет '
                                                 'замечено повторно, ваше сообщение будет передано в администрацию '
                                                 'сообщества '
                                                 'котов, где будет решена ваша судьба: или же вы будете прощены или же '
                                                 'проведете остаток вашей никчемной жизни в бане, не имея малейшей '
                                                 'возможности на освобождение и даже на беглый взор в сторону котов.',
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
                        ids_data[from_id]['profanity'] += 1
                    else:
                        vk.messages.send(user_id=from_id,
                                         message='Ваше сообщение передано в администрацию. Приятного дня!',
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
                        vk.messages.markAsImportantConversation(peer_id=from_id, important=1)
            except Exception:
                pass
            finally:
                if ids_data[from_id]["test_active"]:
                    test.run_test((message_text, from_id), vk, ids_data)

                elif ids_data[from_id]["reminder_manage"]:
                    reminder.manage((message_text, from_id), ids_data, vk)

                elif ids_data[from_id]['translation_mode']:
                    translator.translate(ids_data, from_id, vk, message_text)

                else:
                    try:
                        if 'help' in message_text:
                            vk.messages.send(user_id=from_id,
                                             message='Доступные команды:\n'
                                                     '"Картинка" — получить случайную картинку кота,\n'
                                                     '"Факт" — получить случайный факт о котах,\n'
                                                     '"Тест" — пройти тест про котов,'
                                                     '"Центр уведомлений" — управление уведомлениями,'
                                                     '"Переводчик" — войти в переводчик на кошачий.',
                                             random_id=random.randint(0, 2 ** 64),
                                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

                        elif 'картинка' in message_text:
                            random_picture.send_photo(from_id, vk, keyboards.new_keyboard(from_id, ids_data))

                        elif 'факт' in message_text:
                            random_fact.send_fact(from_id, vk, keyboards.new_keyboard(from_id, ids_data))

                        elif 'тест' in message_text:
                            ids_data[from_id]["test_active"] = True
                            test.run_test((message_text, from_id), vk, ids_data)

                        elif 'напомин' in message_text:
                            ids_data[from_id]["reminder_manage"] = True
                            reminder.manage((message_text, from_id), ids_data, vk)

                        elif 'перев' in message_text:
                            ids_data[from_id]['translation_mode'] = True
                            vk.messages.send(user_id=from_id,
                                             message='Добро пожаловать в переводчик на кошачий язык.\n'
                                                     'Вы можете ввести любую фразу, она будет переведена на кошачий язык.\n'
                                                     'Чтобы выйти из переводчика, введите "Выход"',
                                             random_id=random.randint(0, 2 ** 64),
                                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
                            translator.translate(ids_data, from_id, vk, message_text)

                        else:
                            vk.messages.send(user_id=from_id,
                                             message='Извините, я Вас не понимаю.\nЧтобы посмотреть список команд введите '
                                                     '"help".',
                                             random_id=random.randint(0, 2 ** 64),
                                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

                    except Exception:
                        traceback.print_exc()
                        vk.messages.send(user_id=from_id,
                                         message='Возникла ошибка на стороне сервера.\nЧтобы посмотреть список команд '
                                                 'введите "help".',
                                         random_id=random.randint(0, 2 ** 64),
                                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())


if __name__ == '__main__':
    main()
