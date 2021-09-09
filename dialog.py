import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import Tokenizer
import crawler_final
import Algorithm
import Crawler_link
import os
import subprocess
import pandas as pd


window = tk.Tk()
window.title("데이터 생성")
window.geometry("400x500")

frame1 = tk.Frame(window)
frame1.pack()

dir_path = []
savepoint = ''
db = pd.read_csv("C:/Users/eoxhd/PycharmProjects/YoutubeAl/bigdata_set.csv")
def chrome():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(parent=root,initialdir="/",title='크롬폴더를 선택해주세요')+"/Application"
    textarea.insert(tk.INSERT, dir_path + '\n')
    cmd2 = 'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeTEMP"'
    os.chdir(dir_path)
    subprocess.Popen(cmd2)

    return dir_path

def crawl():
    global data
    data = crawler_final.main(point)
    data1 = data['시청기록']
    data2 = data['검색기록']
    data.to_csv(savepoint + '통합.csv')
    viewkey = Tokenizer.main(data1)
    searchkey = Tokenizer.main(data2)
    semikey = viewkey + searchkey
    global key
    key = []
    for i in semikey:
        if i not in key:
            key.append(i)
    with open(savepoint + 'keyword.txt', 'w', encoding='UTF-8') as file:
        for word in key:
            file.write(word + '\n')

def driver():
    global point
    root = tk.Tk()
    root.withdraw()
    point = filedialog.askdirectory(parent=root, initialdir="/", title='크롬드라이버의 위치를 선택해주세요')
    textarea.insert(tk.INSERT, point + '\n')
    return point

def save():
    root = tk.Tk()
    root.withdraw()
    global savepoint
    savepoint = filedialog.askdirectory(parent=root, initialdir="/",title='저장위치를 선택해주세요')
    savepoint = savepoint + '/'
    textarea.insert(tk.INSERT, savepoint + '\n')
    return savepoint

def pro_exit():
    msgbox = tk.messagebox.askquestion('확인', '프로그램을 종료하시겠습니까?')
    if msgbox == 'yes' :
        window.quit()

def algorithm():
    csv = pd.read_csv(savepoint + '통합.csv')
    csv = pd.DataFrame(csv)
    with open(savepoint + 'keyword.txt', 'r', encoding='UTF-8') as file:
        key1 = file.readlines()
    keyword = []
    for i in key1:
        keyword.append(i[:-1])
    result = Algorithm.main(data, keyword)
    keyword = pd.DataFrame({'키워드': keyword})
    finalresult = Crawler_link.main(result,point)
    finaldata = pd.concat([csv, keyword, finalresult], axis=1)
    finaldata.to_csv(savepoint + '최종.csv')
    return finaldata


tk.Button(frame1, text="저장할위치", command=lambda : save(), width=20, height=3).grid(row=0, column=0)
tk.Button(frame1, text="크롬드라이버위치", command=lambda : driver(), width=20, height=3).grid(row=1, column=0)
tk.Button(frame1, text="크롬켠후 로그인", command=lambda : chrome(), width=20, height=3).grid(row=2, column=0)
tk.Button(frame1, text="크롤링", command=lambda : crawl(), width=20, height=3).grid(row=3, column=0)
tk.Button(frame1, text="알고리즘검색", command=lambda : algorithm(), width=20, height=3).grid(row=4, column=0)
tk.Button(frame1, text="종료", command=lambda : pro_exit(), width=20, height=3).grid(row=5, column=0)


textarea = tk.Text(window)
textarea.pack()

window.mainloop()


