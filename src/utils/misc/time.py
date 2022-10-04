import datetime


def seconds_to_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)

    return datetime.time(h, m, s)