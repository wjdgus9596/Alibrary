from konlpy.tag import Hannanum
from konlpy import jvm
from collections import Counter
import requests
import sys, os

'''
형태소 분석기 * 한나눔 
'''
# 한나눔 함수

def main(data):

    txt_path1 = 'C:/Users/eoxhd/PycharmProjects/YoutubeAl/불용어_KOR.txt'
    txt_path2 = 'C:/Users/eoxhd/PycharmProjects/YoutubeAl/불용어_ENG.txt'

    if getattr(sys, 'frozen', False):
        txt_path1 = os.path.join(sys._MEIPASS, "불용어_KOR.txt")
        txt_path2 = os.path.join(sys._MEIPASS, "불용어_ENG.txt")

    with open(txt_path1 , 'r', encoding='UTF-8') as file:
        data_kor = file.read().split(',')
    with open(txt_path2 , 'r', encoding='UTF-8') as file:
        data_eng = file.read().split(',')
    hn = Hannanum()
    # combined_csv 불러오기
    # data tokenize
    title = []
    for i in range(len(data)):
        title.append(hn.nouns(data[i]))

    listkey = []
    keyword = []

    def keylog(data):
        for i in data:
            keyword = i
            for j in range(len(keyword)):
                if keyword[j].isalnum():
                    listkey.append(keyword[j])
        return listkey

    def frequency_sort(data):
        rt_data = []
        r = int(0.01 * (len(Counter(data))))
        y = Counter(data).most_common()
        for i in range(r):
            rt_data.append(y[i][0])
        return rt_data

    def frequency_sort2(data):
        rt_data = []
        y = Counter(data).most_common()
        for i in range(len(y)):
            rt_data.append(y[i][0])
        return rt_data

    def overlap(a,b):
        for i in a:
            if i not in b:
                b.append(i)
        return b

    def semikeyword(a,b):
        result = []
        for i in b:
            if a in i:
                for j in i:
                    result.append(j)
        return result

    listkey = keylog(title)
    listkey = frequency_sort(listkey)
    overlap(listkey,keyword)


    ####################################################
    '''
    국립국어원 API 명사 추출
    '''

    apikey2 = '7131C62E63584A814819DEC9B9245F1A'


    def midReturn(val, s, e):
        if s in val:
            val = val[val.find(s) + len(s):]
            if e in val:
                val = val[:val.find(e)]
        return val


    def midReturn_all(val, s, e):
        if s in val:
            tmp = val.split(s)
            val = []
            if e in tmp[1]:
                val.append(tmp[1][:tmp[1].find(e)])
        else:
            val = []
        return val


    def checkexists2(query):
        url = 'https://opendict.korean.go.kr/api/search?key=' + apikey2 + '&q=' + query
        response = requests.get(url)
        ans = ''

        words = midReturn_all(response.text, '<item>', '</item>')

        for w in words:
            word = midReturn(w, '<word>', '</word>')
            pos = midReturn(w, '<pos>', '</pos>')
            if pos != '명사' and word == query:
                ans = word
        if len(ans) > 0:
            return ans
        else:
            return ''

    for i in keyword:
        result = checkexists2(i)
        if result != '':
            keyword.remove(i)

    alresult = []
    for i in range(len(keyword)):
        alresult.append(keyword[i])
    c = 0

    for i in range(len(keyword)):
        a = []
        b = []
        c += 1
        d = semikeyword(keyword[i],title)
        a = frequency_sort2(d)
        a = overlap(a, b)
        b = []
        for j in range(1,len(a)) :
            if a[j] not in keyword:
                b.append(a[j])

        for k in range(0,3):
            if len(b) >= 3 :

                if c >= len(alresult):
                    alresult.append(b[k])

                else :
                    alresult.insert(c, b[k])
            c += 1
    result = []
    result = overlap(alresult, result)
    for i in result:
        if i in data_kor:
            result.remove(i)
    for i in result:
        if i in data_eng:
            result.remove(i)
    for i in result:
        if i.isnumeric() == True:
            result.remove(i)
    return result

if __name__ == '__main__':
    jvm.init_jvm()
    main()

