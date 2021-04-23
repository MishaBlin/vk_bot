import random
import traceback

import vk_api

from main import auth_handler


# getting random picture function
def _get_random_atch():
    try:
        login, password = '89129858385', 'MihailkaOther2'
        vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)

        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError:
            traceback.print_exc()
            return

        tools = vk_api.VkTools(vk_session)
        wall = tools.get_all('wall.get', 100, {'owner_id': -203940448})
        post = random.choice(wall['items'])
        while 'attachments' not in post and 'photo' not in post['attachments'][-1]:
            post = random.choice(wall['items'])

        return post['attachments'][-1]['photo']
    except Exception:
        traceback.print_exc()


# sending random picture
def send_photo(from_id, vk, keyboard):
    photo = _get_random_atch()
    vk.messages.send(user_id=from_id,
                     message=f"Случайная картинка: ",
                     attachment=f'photo{photo["owner_id"]}_{photo["id"]}',
                     random_id=random.randint(0, 2 ** 64), keyboard=keyboard.get_keyboard())
