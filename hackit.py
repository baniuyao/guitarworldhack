__author__ = 'yaorenjie'

import requests
import re
import sys
import os

PATH='/Users/yaorenjie/kuaipan/family/guitarworld/'

if __name__ == '__main__':
    n = sys.argv[1]
    resp = requests.get('http://pu.guitarworld.com.cn/q%s/' % n)
    r = re.findall('<title>(.*)</title>', resp.content)
    title = r[0].split('-')[0].strip().replace('/', '_')
    os.mkdir(PATH + title)
    for index, (song_id, page_id) in enumerate(re.findall('/userspace/uploadfiles/qupupic/(\d+)/thumbnail/(\d+).gif', resp.content)):
        print song_id, page_id, title
        url = 'http://pu.guitarworld.com.cn/userspace/uploadfiles/qupupic/%s/%s.gif' % (song_id, page_id)
        ret = requests.get(url)
        file_name = title + '_' + str(index + 1) + '.gif'
        f = file(PATH + title + '/' + file_name, 'aw')
        f.write(ret.content)
        f.close()
