import random


def _get_random_fact():
    with open('data/facts.txt', 'r', encoding='utf8') as file:
        data = file.readlines()
        print(data)
    return random.choice(data)


def send_fact(event, vk, keyboard):
    fact = _get_random_fact()
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=f"Случайный факт про котов: {fact}",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard.get_keyboard())
