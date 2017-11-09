import sys
import time
import datetime
import vk_api


DATA = {}


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
    global DATA
    config_file = open('config.conf')
    vars_list = config_file.readlines()
    for var in vars_list:
        DATA[var.split()[0]] = is_num(var.split()[2])


def post_picture_and_move_it(post_time):
    photo_id = vk.photos.get(owner_id=DATA['owner_id'], album_id=DATA['input_album_id'], count=1)['items'][0]['id']
    vk.wall.post(owner_id=DATA['group_id'],
                 attachments='photo{}_{}'.format(DATA['owner_id'], photo_id),
                 publish_date=post_time,
                 )
    vk.photos.move(owner_id=DATA['owner_id'],
                   target_album_id=DATA['output_album_id'],
                   photo_id=photo_id,
                   )


set_vars()
vk_session = vk_auth(DATA['login'], DATA['password'])
vk = vk_session.get_api()
print('set up and ready')
timing = open(DATA['time_file']).readlines()
posting_time = []
for x in range(len(timing)):
    posting_time.append(datetime.datetime(int(timing[x].split(':')[0]),                     # Day
                                          int(timing[x].split(':')[1]),                     # Month
                                          int(timing[x].split(':')[2]),                     # Year
                                          int(timing[x].split(':')[3]),                     # Hour
                                          int(timing[x].split(':')[4].replace('\n', ''))    # Minute
                                          ))
for t in posting_time:
    try:
            post_picture_and_move_it(time.mktime(t.timetuple()))
    except Exception as ex:
        print(ex)
        continue
print('Done!')
