
import os
import time

from toutiaoweb import toutiao_web




if __name__ == '__main__':
    try:
        download = toutiao_web()

        download.run('12345')

    except Exception as e:
        print('except :{0}'.format(e))

