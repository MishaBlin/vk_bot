import random
from functions import keyboards


def fallback(ids_data, from_id, vk, drop_items):
    for item in drop_items:
        ids_data[from_id][item] = False
    vk.messages.send(user_id=from_id,
                     message="Операция прервана",
                     random_id=random.randint(0, 2 ** 64),
                     keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())

