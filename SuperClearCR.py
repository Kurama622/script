#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
##########################################################################
# File Name: SuperClearCR.py
# Author: stubborn vegeta
# Created Time: 2019年11月21日 星期四 22时41分09秒
##########################################################################
import pyperclip
import time,os,re
import signal
import warnings,random
import requests
from hashlib import md5
from urllib.parse import quote, urlencode, urlparse
from random import randrange

def JudgeChar(cliplist):
    N = cliplist.__len__()
    for charIndex in range(N):
        if cliplist[charIndex] == '-' and cliplist[charIndex+1] == '\n':
            cliplist[charIndex+1]= ''
            cliplist[charIndex]= ''
        elif cliplist[charIndex] == '\n':
            cliplist[charIndex]= ' '
    return cliplist

class InputTimeoutError(Exception):
    pass

def interrupted(signum, frame):
    raise InputTimeoutError

def Quit():
    signal.signal(signal.SIGALRM, interrupted)
    signal.alarm(1)
    try:
        char = input()
    except InputTimeoutError:
        char = ''
    return char

class Tse:
    def __init__(self):
        self.author = 'Ulion.Tse'

    @classmethod
    def timeStat(self, func):
        def wrapper(*args, **kwargs):
            import time
            t1 = time.time()
            r = func(*args, **kwargs)
            t2 = time.time()
            # print('UseTimeSeconds(fn: {}): {}'.format(func.__name__, round((t2 - t1), 2)))
            return r
        return wrapper

    def get_headers(self, host_url, if_use_api=False, if_use_referer=True):
        url_path = urlparse(host_url).path
        host_headers = {
            'Referer' if if_use_referer else 'Host': host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36"
        }
        api_headers = {
            'Origin': host_url.split(url_path)[0] if url_path else host_url,
            'Referer': host_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36"
        }
        return host_headers if not if_use_api else api_headers

    def check_language(self, from_language, to_language, language_map, output_zh=None, output_auto='auto'):
        from_language = output_auto if from_language in ('auto', 'auto-detect') else from_language
        from_language = output_zh if output_zh and from_language in ('zh','zh-CN','zh-CHS','zh-Hans') else from_language
        to_language = output_zh if output_zh and to_language in ('zh','zh-CN','zh-CHS','zh-Hans') else to_language
        
        if from_language != output_auto and from_language not in language_map:
            raise KeyError('Unsupported from_language[{}] in {}.'.format(from_language,list(language_map.keys())))
        elif to_language not in language_map:
            raise KeyError('Unsupported to_language[{}] in {}.'.format(to_language,list(language_map.keys())))
        elif from_language != output_auto and to_language not in language_map[from_language]:
            print('language_map:', language_map)
            raise Exception('Unsupported translation: from [{0}] to [{1}]!'.format(from_language,to_language))
        return from_language,to_language

class Google(Tse):
    def __init__(self):
        super().__init__()
        self.host_url = None
        self.cn_host_url = 'https://translate.google.cn'
        self.en_host_url = 'https://translate.google.com'
        self.host_headers = None
        self.language_map = None
        self.api_url = None
        self.query_count = 0
        self.output_zh = 'zh-CN'
 
    # def rshift(self,val, n):
    #     """python port for '>>>'(right shift with padding)
    #     """
    #     return (val % 0x100000000) >> n
    
    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            # d = google.rshift(self,a, d) if '+' == b[c + 1] else a << d
            d = (a % 0x100000000) >> d if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d
            c += 3
        return a
    
    def acquire(self, text, tkk):
        # tkk = google.get_tkk(self)
        b = tkk if tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0
        
        # assume e means char code array
        e = []
        g = 0
        size = len(text)
        for i, char in enumerate(text):
            l = ord(char)
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                        ord(text[g + 1]) & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + ord(text[g]) & 1023
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                        e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  # pragma: nocover
            a = (a & 2147483647) + 2147483648
        a %= 1000000  # int(1E6)
        return '{}.{}'.format(a, a ^ b)

    def get_language_map(self,host_html):
        lang_list_str = re.findall("source_code_name:\[(.*?)\],", host_html)[0]
        lang_list_str = ('['+ lang_list_str + ']').replace('code','"code"').replace('name','"name"')
        lang_list = [x['code'] for x in eval(lang_list_str) if x['code'] != 'auto']
        return {}.fromkeys(lang_list,lang_list)

    @Tse.timeStat
    def google_api(self, query_text, from_language='auto', to_language='zh', **kwargs):
        '''
        https://translate.google.com, https://translate.google.cn.
        :param query_text: string, must.
        :param from_language: string, default 'auto'.
        :param to_language: string, default 'zh'.
        :param **kwargs:
                :param if_use_cn_host: boolean, default True.
                :param is_detail_result: boolean, default False.
                :param proxies: dict, default None.
                :param sleep_seconds: float, default 0.05.
        :return: string or list
        '''
        self.host_url = self.cn_host_url if kwargs.get('if_use_cn_host', True) else self.en_host_url
        self.host_headers = self.get_headers(self.cn_host_url, if_use_api=False)
        is_detail_result = kwargs.get('is_detail_result', False)
        proxies = kwargs.get('proxies', None)
        sleep_seconds = kwargs.get('sleep', 0.05)
    
        with requests.Session() as ss:
            host_html = ss.get(self.host_url, headers=self.host_headers, proxies=proxies).text
            self.language_map = self.get_language_map(host_html)
            from_language,to_language = self.check_language(from_language,to_language,self.language_map,output_zh=self.output_zh)
            
            tkk = re.findall("tkk:'(.*?)'", host_html)[0]
            tk = self.acquire(query_text, tkk)
            self.api_url = (self.host_url + '/translate_a/single?client={0}&sl={1}&tl={2}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md'
                            + '&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk='
                            + str(tk) + '&q=' + quote(query_text)).format('webapp', from_language,to_language)  # [t,webapp]

            r = ss.get(self.api_url, headers=self.host_headers, proxies=proxies)
            r.raise_for_status()
            data = r.json()
        time.sleep(sleep_seconds)
        self.query_count += 1
        return data if is_detail_result else ''.join([item[0] for item in data[0] if isinstance(item[0],str)])

# class Youdao(Tse):
    # def __init__(self):
        # super().__init__()
        # self.host_url = 'http://fanyi.youdao.com'
        # self.api_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        # self.get_sign_url = 'http://shared.ydstatic.com/fanyi/newweb/v1.0.24/scripts/newweb/fanyi.min.js'
        # self.get_sign_pattern = 'http://shared.ydstatic.com/fanyi/newweb/(.*?))/scripts/newweb/fanyi.min.js'
        # self.host_headers = self.get_headers(self.host_url, if_use_api=False)
        # self.api_headers = self.get_headers(self.host_url, if_use_api=True)
        # self.language_map = None
        # self.query_count = 0
        # self.output_zh = 'zh-CHS'
    
    # def get_language_map(self, host_html):
        # et = etree.HTML(host_html)
        # lang_list = et.xpath('//*[@id="languageSelect"]/li/@data-value')
        # lang_list = [(x.split('2')[0], [x.split('2')[1]]) for x in lang_list if '2' in x]
        # lang_map = dict(map(lambda x: x, lang_list))
        # lang_map.pop('zh-CHS')
        # lang_map.update({'zh-CHS': list(lang_map.keys())})
        # return lang_map

    # def get_sign_key(self, ss, host_html, proxies):
        # try:
            # r = ss.get(self.get_sign_url, headers=self.host_headers, proxies=proxies)
            # r.raise_for_status()
        # except:
            # self.get_sign_url = re.search(self.get_sign_pattern, host_html).group(0)
            # r = ss.get(self.get_sign_url, headers=self.host_headers, proxies=proxies)
        # sign = re.findall('n.md5\("fanyideskweb"\+e\+i\+"(.*?)"\)', r.text)
        # return sign[0] if sign and sign != [''] else 'Nw(nmmbP%A-r6U3EUn]Aj'

    # def get_form(self, query_text, from_language, to_language, sign_key):
        # ts = str(int(time.time()))
        # salt = str(ts) + str(random.randrange(0, 10))
        # sign_text = ''.join(['fanyideskweb', query_text, salt, sign_key])
        # sign = md5(sign_text.encode()).hexdigest()
        # bv = md5(self.api_headers['User-Agent'][8:].encode()).hexdigest()
        # form = {
            # 'i': str(query_text),
            # 'from': from_language,
            # 'to': to_language,
            # 'ts': ts,                   # r = "" + (new Date).getTime()
            # 'salt': salt,               # i = r + parseInt(10 * Math.random(), 10)
            # 'sign': sign,               # n.md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj"),e=text
            # 'bv': bv,                   # n.md5(navigator.appVersion)
            # 'smartresult': 'dict',
            # 'client': 'fanyideskweb',
            # 'doctype': 'json',
            # 'version': '2.1',
            # 'keyfrom': 'fanyi.web',
            # 'action': 'FY_BY_REALTlME',  # not time.["FY_BY_REALTlME","FY_BY_DEFAULT"]
            # # 'typoResult': 'false'
        # }
        # return form

    # @Tse.timeStat
    # def youdao_api(self, query_text, from_language='auto', to_language='zh', **kwargs):
        # '''
        # http://fanyi.youdao.com
        # :param query_text: string, must.
        # :param from_language: string, default 'auto'.
        # :param to_language: string, default 'zh'.
        # :param **kwargs:
                # :param nonautomatic_recognize_replaced_language: string, default 'en'.
                # :param is_detail_result: boolean, default False.
                # :param proxies: dict, default None.
                # :param sleep_seconds: float, default 0.05.
        # :return: string or dict
        # '''
        # nonautomatic_recognize_replaced_language = kwargs.get('nonautomatic_recognize_replaced_language', 'en')
        # is_detail_result = kwargs.get('is_detail_result', False)
        # proxies = kwargs.get('proxies', None)
        # sleep_seconds = kwargs.get('sleep', 0.05)

        # with requests.Session() as ss:
            # host_html = ss.get(self.host_url, headers=self.host_headers, proxies=proxies).text
            # self.language_map = self.get_language_map(host_html)
            # sign_key = self.get_sign_key(ss, host_html, proxies)
            # from_language, to_language = self.check_language(from_language, to_language, self.language_map,output_zh=self.output_zh)

            # def post_data(from_language):
                # form = self.get_form(str(query_text), from_language, to_language, sign_key)
                # r = ss.post(self.api_url, data=form, headers=self.api_headers, proxies=proxies)
                # r.raise_for_status()
                # return r.json()

            # data = post_data(from_language)
            # data = post_data(nonautomatic_recognize_replaced_language) if data.get('errorCode') == 40 else data
        # time.sleep(sleep_seconds)
        # self.query_count += 1
        # if data['errorCode'] == 40:
            # raise Exception('Unable to automatically recognize the language of `query_text`, '
                            # 'please specify parameters of `from_language` or `nonautomatic_recognize_replaced_language`.')
        # return data if is_detail_result else ''.join(item['tgt'] for item in data['translateResult'][0])

# class Youdao():
    # def __init__(self):
        # self.host = 'http://fanyi.youdao.com'
        # self.api_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule?'
        # self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko' \
                  # ') Chrome/69.0.3497.100 Safari/537.36'
        # self.cookies = {
            # 'OUTFOX_SEARCH_USER_ID': '{0}@10.168.8.{1}'.format(randrange(int(1e9),int(1e10)),randrange(1,100)),
        # }
        # self.headers = {
            # 'User-Agent': self.ua,
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Host': 'fanyi.youdao.com',
            # 'Origin': 'http://fanyi.youdao.com',
            # 'Referer': 'http://fanyi.youdao.com/?keyfrom=fanyi.logo',
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6,zh-TW;q=0.5,zh-HK;q=0.4',
            # 'Connection': 'keep-alive'
        # }

    # def get_form(self,text):
        # ts = str(int(time.time()))
        # salt = str(ts) + str(randrange(0,10))
        # sign_text = ''.join(['fanyideskweb',text,salt,'n%A-rKaT5fb[Gy?;N5@Tj']) # before 20190902: p09@Bn{h02_BIEe]$P^nG
        # sign = md5(sign_text.encode()).hexdigest()
        # bv = md5(self.headers['User-Agent'][8:].encode()).hexdigest()
        # form = {
            # 'i': str(text),
            # 'smartresult': 'dict',
            # 'client': 'fanyideskweb',
            # 'ts': ts,                     # r = "" + (new Date).getTime()
            # 'salt': salt,                 # i = r + parseInt(10 * Math.random(), 10)
            # 'sign': sign,                 # n.md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj"),e=text
            # 'bv': bv,                     # n.md5(navigator.appVersion)
            # 'doctype': 'json',
            # 'version': '2.1',
            # 'keyfrom': 'fanyi.web',
            # 'action': 'FY_BY_REALTlME', #not time.
            # #'typoResult': 'false'
        # }
        # return form

    # def youdao_api(self,text,**kwargs):
        # is_detail = kwargs.get('is_detail', False)
        # proxies = kwargs.get('proxies', None)
        # form = self.get_form(text)
        # ss = requests.Session()
        # r0 = ss.get(self.host, headers=self.headers,proxies=proxies)
        # if r0.status_code == 200 and len(r0.cookies)>0:
            # r = ss.post(self.api_url, data=form, headers=self.headers,proxies=proxies)
        # else:
            # r = ss.post(self.api_url, data=form, headers=self.headers, cookies=self.cookies,proxies=proxies)
        # if r.status_code == 200:
            # translateResult = r.json()
        # else:
            # raise Exception('NetworkRequestError: response <{}>'.format(r.status_code))
        # ss.close()

        # if translateResult['errorCode'] == 0:
            # N = len(translateResult['translateResult'][0])
            # result = ''
            # for i in range(N):
                # result = result + translateResult['translateResult'][0][i]['tgt']
            # return translateResult if is_detail else result
        # else:
            # raise YoudaoApiError(result['errorCode'])

class YoudaoApiError(Exception):
    def __init__(self,errorNum):
        Exception.__init__(self)
        self.errorMsg = {
            "10": "Sorry, individual sentences are too long for me to read!",
            "20": "Sorry, more than 20,000 words is too long. Let me catch my breath!",
            "30": "Sorry, I've racked my brain. No effective translation is possible!",
            "40": "Sorry, I'm still learning the language. Unsupported language type!",
            "50": "Sorry, please do not request service frequently!",
            "transRequestError": "Translation error, please check the network and try again!",
            "serviceError": "ServiceError!"
        }
        self.errorNum = str(errorNum)
        print('YoudaoApiError: {}\n'.format(self.errorMsg[self.errorNum]))

def writeFile(data, FileName):
    if not os.path.exists(FileName):
        with open(FileName, 'w') as f:
            pass

    with open(FileName, 'a') as f:
        f.write(data)

if __name__ == '__main__':
    clipStringPre = pyperclip.paste()          # getclip
    cliplistpre = list(clipStringPre)
    JudgeChar(cliplistpre)
    clipStringPre = ''.join(cliplistpre)
    pyperclip.copy(clipStringPre)
    start = True
    while start:
        clipString = pyperclip.paste()          # getclip
        cliplist = list(clipString)
        JudgeChar(cliplist)
        clipString = ''.join(cliplist)
        pyperclip.copy(clipString)
        if clipString == clipStringPre:
            char = Quit()
            if char == 'q':
                start = False
            else:
                time.sleep(1)
        else:
            clipStringPre = clipString
#             cliplist = list(clipString)
#             JudgeChar(cliplist)
#             newString = ''.join(cliplist)
#             pyperclip.copy(newString)
            newString = clipString
            print(newString)
            # yd = Youdao()
            # youdao_api = yd.youdao_api(newString)
            yd = Google()
            youdao_api = yd.google_api(newString)
#             clipString = pyperclip.copy(youdao_api)
            print('-'*58)
            print(youdao_api)
            print('='*58)
            data = newString + '\n' + youdao_api + '\n'
            ChineseText = youdao_api + '\n'
#             writeFile(data, PATH+'En2ZhText')
#             writeFile(ChineseText, PATH+'ChineseText')
