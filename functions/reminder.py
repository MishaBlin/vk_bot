import random
import schedule
from functions import keyboards

first_run = True


def remind(from_id, ids_data, vk):
    vk.messages.send(user_id=from_id,
                     message="Напоминание!\nВремя покормить кота!!",
                     random_id=random.randint(0, 2 ** 64),
                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())


def create_reminder(from_id, message_text, ids_data, vk):
    if ids_data[from_id]['creation']:
        try:
            # schedule.every(16 // int(message_text)).hours.do(remind, from_id=from_id, ids_data=ids_data, vk=vk)
            schedule.every(10).seconds.do(remind, from_id=from_id, ids_data=ids_data, vk=vk)
            if ids_data[from_id]['reminders']:
                ids_data[from_id]['reminders'] = ids_data[from_id]['reminders'].append(int(message_text))
            else:
                ids_data[from_id]['reminders'] = [int(message_text)]
            vk.messages.send(user_id=from_id,
                             message="Напоминание успешно создано!",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
            ids_data[from_id]['creation'] = False
        except ValueError:
            vk.messages.send(user_id=from_id,
                             message="Пожалуйста, введите корректное значение.",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

    else:
        vk.messages.send(user_id=from_id,
                         message="Сколько раз в день вы кормите своего кота/кошку?\n"
                                 "\n(Чтобы узнать оптимальное количество раз, посоветуйтесь с ветеринаром. "
                                 "Также, данная информация указывается на упаковке кормов). ",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())


def manage(message_data, ids_data, vk):
    message_text = message_data[0]
    from_id = message_data[1]

    if ids_data[from_id]['first_reminder_run']:
        vk.messages.send(user_id=from_id,
                         message="Добро пожаловать в центр напоминаний!\n"
                                 "Напоминания помогут вам не забывать кормить кота!\n"
                                 "\nСписок команд:\n"
                                 "'Создать'\n"
                                 "'Удалить'\n"
                                 "'Мои напоминания'\n"
                                 "'Выход'",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        ids_data[from_id]['first_reminder_run'] = False
    else:
        if ids_data[from_id]['creation']:
            create_reminder(from_id, message_text, ids_data, vk)

        elif 'создать' in message_text:
            create_reminder(from_id, message_text, ids_data, vk)
            ids_data[from_id]['creation'] = True

        elif 'выход' in message_text:
            ids_data[from_id]["reminder_manage"] = False
            ids_data[from_id]['first_reminder_run'] = True
            vk.messages.send(user_id=from_id,
                             message="Вы вышли из центра напоминаний",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

