import random


# getting random fact from file
def _get_random_fact():
    with open('data/facts.txt', 'r', encoding='utf8') as file:
        data = file.readlines()
    return random.choice(data)


# sending random fact
def send_fact(from_id, vk, keyboard):
    fact = _get_random_fact()
    vk.messages.send(user_id=from_id,
                     message=f"Случайный факт про котов: {fact}",
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard.get_keyboard())
