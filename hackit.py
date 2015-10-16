__author__ = 'yaorenjie'

import requests
import re

if __name__ == '__main__':
    resp = requests.get('http://pu.guitarworld.com.cn/q1850/')
    r = re.findall('<title>(.*)</title>', resp.content)
    title = r[0].split('-')[0].strip()
    for index, (song_id, page_id) in enumerate(re.findall('/userspace/uploadfiles/qupupic/(\d+)/thumbnail/(\d+).gif', resp.content)):
        print song_id, page_id
        url = 'http://pu.guitarworld.com.cn/userspace/uploadfiles/qupupic/%s/%s.gif' % (song_id, page_id)
        ret = requests.get(url)
        file_name = title + '_' + str(index + 1) + '.gif'
        f = file('/Users/yaorenjie/Downloads/' + file_name, 'aw')
        f.write(ret.content)
        f.close()
