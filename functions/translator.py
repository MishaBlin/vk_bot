import random
import traceback
from functions import fallback, keyboards

# translation dict
cat_dict = ['мяу', 'миу', 'мряу', 'мяфк', 'мрр', 'мяв']


# main translator function
def translate(ids_data, from_id, vk, message_text):
    if not ids_data[from_id]['first_run']:
        try:
            if 'выход' in message_text:
                fallback.fallback(ids_data, from_id, vk, ('translation_mode',))
                ids_data[from_id]['first_run'] = True
                return None
            line = message_text.split(' ')
            cat_line = 'Перевод на кошачий: '
            for _ in range(len(line)):
                cat_line += random.choice(cat_dict) + ' '
            vk.messages.send(user_id=from_id,
                             message=cat_line,
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
        except Exception:
            traceback.print_exc()
            vk.messages.send(user_id=from_id,
                             message="Не удалось перевести сообщение.",
                             random_id=random.randint(0, 2 ** 64),
                             keyboard=keyboards.new_keyboard(from_id, ids_data).get_keyboard())
    else:
        ids_data[from_id]['first_run'] = False
