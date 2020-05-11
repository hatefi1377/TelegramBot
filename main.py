import json
from urllib.request import urlopen
from urllib.parse import quote
import time
from data_base import data_base_data
import time
from flask_sslify import SSLify
from flask import Flask

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def index():
    return '<h1>Botman</h1>'



def aux_dec2utf8(resp):
    decoded = ''
    for line in resp:
        decoded += line.decode('utf-8')
    return decoded


TOKEN = '1118640921:AAEA-DoYAk5BlDmzzDNhUhdeKAknoR5l1qw'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

cmd = 'getme'

resp = urlopen(URL + cmd)
line = aux_dec2utf8(resp)
gtm = json.loads(line)

list_questions = [
    "/hatef_thought",
    "/about_you",
    "/darkhast",
    "/start"
]
i = 1
j = 1
status = True
while status:

    cmd = 'getUpdates'

    resp = urlopen(URL + cmd)
    line = aux_dec2utf8(resp)
    upds = json.loads(line)

    NoM = len(upds['result'])

    if NoM != 0 and 'text' in upds['result'][0]['message'] and 'username' in upds['result'][0]['message']['from']:


        commend = upds['result'][0]['message']['text']
        chid = str(upds['result'][0]['message']['chat']['id'])
        user_name = upds['result'][0]['message']['from']['username']


        if commend == '/start' :
            test = '''Welcome to my bot'''
            txt = quote(test.encode('utf-8'))
            cmd = 'sendMessage'
            resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))
            uid = upds['result'][0]['update_id']
            cmd = 'getUpdates'
            urlopen(URL + cmd + '?offset={}'.format(uid + 1))


        if commend in list_questions:
            if user_name in data_base_data:
                if commend == '/hatef_thought':
                    text = data_base_data[f'{user_name}']['/hatef_thought']
                    txt = quote(text.encode('utf-8'))

                    cmd = 'sendMessage'

                    resp = urlopen(URL + cmd +
                                   '?chat_id={}&text={}'.format(chid, txt))

                elif commend == '/about_you':
                    text = data_base_data[f'{user_name}']['/about_you']
                    txt = quote(text.encode('utf-8'))
                    cmd = 'sendMessage'
                    resp = urlopen(URL + cmd +
                                   '?chat_id={}&text={}'.format(chid, txt))


            elif user_name not in data_base_data and commend == '/darkhast' :
                test = '''
                اسم و فامیل شریفتون ؟
                لطفا به فرم
                name - < اسم و فامیل شریف >
                بفرستید
                '''
                txt = quote(test.encode('utf-8'))
                cmd = 'sendMessage'
                resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))
                uid = upds['result'][0]['update_id']
                cmd = 'getUpdates'
                urlopen(URL + cmd + '?offset={}'.format(uid + 1))



            else:
                test = '''
                من در مورد شما چیزی ثبت نکردم 😔
                اگه می خواید درخواست بدید که ثبت کنم از دستور
                /darkhast
                می تونید استفاده کنید
                '''
                txt = quote(test.encode('utf-8'))

                cmd = 'sendMessage'

                resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))

                uid = upds['result'][0]['update_id']
                cmd = 'getUpdates'
                urlopen(URL + cmd + '?offset={}'.format(uid + 1))

            line = aux_dec2utf8(resp)
            chck = json.loads(line)

            if chck['ok']:
                uid = upds['result'][0]['update_id']
                cmd = 'getUpdates'
                urlopen(URL + cmd + '?offset={}'.format(uid + 1))

        elif 'name -' in commend :
            with open(f'/home/hatefi/bot/darkhast/{j}.json', 'w', encoding='utf-8') as f:
                json.dump(upds, f, ensure_ascii=False, indent=4)
            j += 1

            test = 'درخواست شما با موفقیت ثبت شد'
            txt = quote(test.encode('utf-8'))

            cmd = 'sendMessage'

            resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))
            uid = upds['result'][0]['update_id']
            cmd = 'getUpdates'
            urlopen(URL + cmd + '?offset={}'.format(uid + 1))

        else:
            test = 'همچین دستوری موجود نداریم 🤨'
            txt = quote(test.encode('utf-8'))

            cmd = 'sendMessage'

            resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))

            with open(f'/home/hatefi/bot/log/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(upds, f, ensure_ascii=False, indent=4)
            i += 1
            uid = upds['result'][0]['update_id']
            cmd = 'getUpdates'
            urlopen(URL + cmd + '?offset={}'.format(uid + 1))

    elif NoM != 0 and 'username' not in upds['result'][0]['message']['from']:
        chid = str(upds['result'][0]['message']['chat']['id'])
        test = 'لطفا برای ادامه یک یوزر تلگرام برای خود بگزارید 🤨'
        txt = quote(test.encode('utf-8'))

        cmd = 'sendMessage'

        resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))

        uid = upds['result'][0]['update_id']
        cmd = 'getUpdates'
        urlopen(URL + cmd + '?offset={}'.format(uid + 1))

    elif NoM != 0 :
        test = 'همچین دستوری موجود نداریم 🤨'
        txt = quote(test.encode('utf-8'))
        chid = str(upds['result'][0]['message']['chat']['id'])
        cmd = 'sendMessage'

        resp = urlopen(URL + cmd + '?chat_id={}&text={}'.format(chid, txt))

        uid = upds['result'][0]['update_id']
        cmd = 'getUpdates'
        urlopen(URL + cmd + '?offset={}'.format(uid + 1))

    time.sleep(1)

