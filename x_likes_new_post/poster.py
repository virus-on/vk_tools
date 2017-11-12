import sys
import time
import vk_api
from random import shuffle


DATA = {}
MESSAGES = []


def vk_auth(login, password):
    vk_obj = vk_api.VkApi(login, password)
    try:
        vk_obj.auth()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        sys.exit()
    return vk_obj


def is_num(s):
    if s.isnumeric():
        return int(s)
    else:
        return s


def set_vars():
    global DATA, MESSAGES
    config_file = open('configuration.conf')
    message_file = open('messages.txt')
    vars_list = config_file.readlines()
    for var in vars_list:
        DATA[var.split()[0]] = is_num(var.split()[2])
    MESSAGES = message_file.readlines()


def get_likes_count():
    return vk.wall.get(count=2, owner_id=DATA['GROUP_ID'])['items'][1]['likes']['count']


def post_picture_and_move_it():
    shuffle(MESSAGES)
    if DATA['POST_COUNT'] == 0:
        MESSAGES[-1] = DATA['LAST_MESSAGE']
    photo_id = vk.photos.get(owner_id=DATA['OWNER_ID'], album_id=DATA['INPUT_ALBUM_ID'], count=1)['items'][0]['id']
    vk.wall.post(owner_id=DATA['GROUP_ID'],
                 attachments='photo{}_{}'.format(DATA['OWNER_ID'], photo_id),
                 message=MESSAGES[-1])
    vk.photos.move(owner_id=DATA['OWNER_ID'],
                   target_album_id=DATA['OUTPUT_ALBUM_ID'],
                   photo_id=photo_id)


set_vars()
vk_session = vk_auth(DATA['LOGIN'], DATA['PASSWORD'])
vk = vk_session.get_api()

print('set up and ready')
post_picture_and_move_it()
DATA['POST_COUNT'] -= 1
print('Posted, ' + str(DATA['POST_COUNT']) + ' to go!')

while DATA['POST_COUNT'] > 0:
    try:
        print(str(get_likes_count()) + " of " + str(DATA['LIKES_COUNT']))
        if get_likes_count() > DATA['LIKES_COUNT']:
            DATA['POST_COUNT'] -= 1
            post_picture_and_move_it()
            print('Posted, ' + str(DATA['POST_COUNT']) + ' to go!')
    except Exception as ex:
        print(ex)
        continue
    time.sleep(30)

print('Done!')
