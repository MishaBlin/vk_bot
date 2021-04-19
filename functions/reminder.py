import datetime
import random
import traceback

from functions import keyboards
from apscheduler.schedulers.background import BackgroundScheduler


def get_times(message_text, ids_data, from_id):
    times = message_text.strip(' ./?,!@#$%^&*()_-').split(', ')
    another_times = message_text.split(',')
    if len(times) == ids_data[from_id]['amount_of_feeds'] and (len(x) == 5 for x in times):
        return times
    elif len(another_times) == ids_data[from_id]['amount_of_feeds'] and (len(x) == 5 for x in another_times):
        return another_times
    else:
        return None


def remind(from_id, ids_data, vk):
    vk.messages.send(user_id=from_id,
                     message="Напоминание!\nВремя покормить кота!",
                     random_id=random.randint(0, 2 ** 64),
                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
    print(f"sent to {from_id} at {datetime.datetime.now()}")


def create_reminder(from_id, message_text, ids_data, vk):
    if ids_data[from_id]['creation']:
        try:
            if ids_data[from_id]['getting_times']:
                times = get_times(message_text, ids_data, from_id)
                if times:
                    scheduler = BackgroundScheduler()
                    for item in times:
                        scheduler.add_job(func=remind, trigger="cron", day_of_week='mon-sun', hour=item[:2],
                                          minute=item[3:],
                                          args=(from_id, ids_data, vk))
                        ids_data[from_id]['reminders'].append((item[:2], item[3:]))
                    scheduler.start()
                    vk.messages.send(user_id=from_id,
                                     message="Напоминание успешно создано!",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
                    ids_data[from_id]['creation'] = False
                    ids_data[from_id]['getting_times'] = False
                else:
                    vk.messages.send(user_id=from_id,
                                     message='Пожалуйста, введите корректное значение для каждого кормления в формате '
                                             '"hh-mm" через запятую.',
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

            else:
                if 0 < int(message_text) <= 9:
                    ids_data[from_id]['amount_of_feeds'] = int(message_text)
                    ids_data[from_id]['getting_times'] = True
                    vk.messages.send(user_id=from_id,
                                     message='Введите время для каждого кормления в формате "hh-mm" через запятую.',
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
                else:
                    vk.messages.send(user_id=from_id,
                                     message="Пожалуйста, введите корректное значение (Рекомендуется вводить "
                                             "значение от 1 до 9).",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

        except Exception:
            traceback.print_exc()
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


def get_reminders(ids_data, from_id):
    data = ids_data[from_id]['reminders']
    if data:
        line = 'Ваши напоминания:\n'
        for item in enumerate(data):
            line += f"{item[0] + 1}. Кормление кота в {item[1][0]}:{item[1][1]}\n"
        return line
    return "У Вас нет напоминаний."


def deleting_reminders(ids_data, from_id, message_text, vk):
    try:
        if ids_data[from_id]['deleting_reminders']:
            clear_line = ''
            for symbol in message_text:
                if symbol != ' ':
                    clear_line += symbol
            to_delete_list = clear_line.split(',')
            helper = 1
            for item in to_delete_list:
                del ids_data[from_id]['reminders'][int(item) - helper]
                helper += 1
            vk.messages.send(user_id=from_id,
                             message="Выбранныйе напоминания успешно удалены!",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
            ids_data[from_id]['deleting_reminders'] = False

        else:
            vk.messages.send(user_id=from_id,
                             message="Пожалуйста, через запятую введите номера напоминаний, которые вы хотите удалить.",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
            ids_data[from_id]['deleting_reminders'] = True
    except Exception:
        traceback.print_exc()
        vk.messages.send(user_id=from_id,
                         message="Пожалуйста, введите корректное значение: "
                                 "номера напоминаний через запятую, которые вы хотите удалить.",
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())


def manage(message_data, ids_data, vk):
    message_text = message_data[0]
    from_id = message_data[1]

    if ids_data[from_id]['first_reminder_run']:
        vk.messages.send(user_id=from_id,
                         message="Добро пожаловать в центр напоминаний!\n"
                                 "Напоминания помогут вам не забывать вовремя кормить кота!\n\n"
                                 "Список команд центра напоминаний:\n"
                                 '1. "Создать" — создать новое напоминание,\n'
                                 '2. "Удалить" — удаление имеющихся напоминаний,\n'
                                 '3. "Мои напоминания" — просмотр списка имеющихся напоминаний,\n'
                                 '4. "Выход" — выйти из Центра напоминий.',
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        ids_data[from_id]['first_reminder_run'] = False
    else:
        if ids_data[from_id]['creation']:
            create_reminder(from_id, message_text, ids_data, vk)

        elif ids_data[from_id]['deleting_reminders']:
            deleting_reminders(ids_data, from_id, message_text, vk)

        elif 'создать' in message_text:
            create_reminder(from_id, message_text, ids_data, vk)
            ids_data[from_id]['creation'] = True

        elif 'мои' in message_text:
            vk.messages.send(user_id=from_id,
                             message=get_reminders(ids_data, from_id),
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

        elif 'удал' in message_text:
            vk.messages.send(user_id=from_id,
                             message=get_reminders(ids_data, from_id),
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
            if get_reminders(ids_data, from_id) != "У Вас нет напоминаний.":
                deleting_reminders(ids_data, from_id, message_text, vk)

        elif 'выход' in message_text:
            ids_data[from_id]["reminder_manage"] = False
            ids_data[from_id]['first_reminder_run'] = True
            vk.messages.send(user_id=from_id,
                             message="Вы вышли из центра напоминаний",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
