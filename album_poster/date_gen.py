import datetime


class Generator:
    def __init__(self, path, days_count):
        post_time = open(path).readlines()
        output_file = open('datetime.conf','w')
        out = []
        date = datetime.datetime.today()
        for x in range(days_count):
            for string in post_time:
                time = datetime.time(int(string.split(':')[0]),
                                     int(string.split(':')[1])
                                     )
                out.append(datetime.datetime.combine(date, time)
                                            .strftime("%Y:%m:%d:%H:%M")+'\n')
            date += datetime.timedelta(days=1)

        output_file.writelines(out)
        print('Done!')


if __name__ == '__main__':
    Generator('time.conf', 10)
