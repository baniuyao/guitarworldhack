import requests
import base64
import re
import sys
import os

PATH = '/Users/yaorenjie/kuaipan/family/guitarworld/'


class Utils(object):
    @staticmethod
    def post_xml(url, xml_string):
        headers = {'Content-Type': 'text/xml'}
        content = requests.post(url, data=xml_string, headers=headers).content
        return re.findall('<DownloadFileResult>(.*?)</DownloadFileResult>', content)[0]

    @staticmethod
    def write_file_content(file_name, content):
        f = open(file_name, 'w')
        f.write(content)
        f.close()


class GuitarWorldHack(object):
    def __init__(self, guitar_tab_id):
        content = requests.get('http://pu.guitarworld.com.cn/q%s/' % guitar_tab_id).content
        raw_title = re.findall('<title>(.*)</title>', content)
        self._title = raw_title[0].split('-')[0].strip().replace('/', '_')
        self.song_id_page_id = re.findall('/userspace/uploadfiles/qupupic/(\d+)/thumbnail/(\d+).gif', content)

    def _create_dir(self):
        if not os.path.exists(PATH + self._title):
            os.mkdir(PATH + self._title)

    def get_gif_file(self, song_id, page_id):
        xml_content = self.gen_xml_content(song_id, page_id)
        result = Utils.post_xml('http://client.guitarworld.com.cn:8081/ClientServer.asmx',
                                xml_content)
        return base64.b64decode(result)

    def gen_xml_content(self, song_id, page_id):
        xml_content = r"""<?xml version="1.0" encoding="UTF-8"?>
            <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <DownloadFile xmlns="http://www.guitarworld.com.cn/">
                        <fileName>D:\ComsenzEXP\wwwroot\bbs\userspace\uploadfiles\qupupic\%s\%s.gif</fileName>
                        <key>5074e03c6bad5b812b54337b0841e156</key>
                    </DownloadFile>
                </s:Body>
            </s:Envelope>
            """ % (song_id, page_id)
        return xml_content

    def hack_it(self):
        self._create_dir()
        for index, (song_id, page_id) in enumerate(self.song_id_page_id):
            file_content = self.get_gif_file(song_id, page_id)
            file_name = self._title + '_' + str(index + 1) + '.gif'
            print file_name
            Utils.write_file_content(PATH + self._title + '/' + file_name, file_content)


if __name__ == '__main__':
    tab_id = sys.argv[1]
    hack = GuitarWorldHack(tab_id)
    hack.hack_it()
