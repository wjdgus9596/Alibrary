import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def main():

    window = tk.Tk()
    window.title("키워드 수정")
    window.geometry("600x600")
    window.resizable(True,True)

    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side="right", fill="y")
    checklist = tk.Text(window, width=60, bg='skyblue')
    checklist.pack()
    frame1 = tk.Frame(window)
    frame1.pack()
    global point
    global df


    def save():
        root = tk.Tk()
        root.withdraw()
        global point
        global df
        savepoint = filedialog.askdirectory(parent=root, initialdir="/", title='파일위치를 선택해주세요')
        point = savepoint + '/keyword.txt'
        with open(point,'r',encoding='UTF-8') as file :
            df = file.readlines()
        global ck_var
        global ck_btn
        ck_var = [None] * len(df)
        ck_btn = [None] * len(df)
        ck_var = edit(df, ck_var, ck_btn)


    def edit(a,b,c):

        for i in range(len(a)):
            b[i] = tk.IntVar()
            c[i] = tk.Checkbutton(checklist, text=a[i], variable=b[i])
            checklist.window_create("end", window=c[i])
            checklist.insert("end", "\n")
        return b



    def saving(a, b, c):
        chklist = []
        for i in range(len(b)):
            if b[i].get() == 1:
                chklist.append(c[i])

        with open(a , 'w', encoding='UTF-8') as file:
            for word in chklist:
                file.write(word)
        msgbox = messagebox.showinfo("완료","저장이 완료되었습니다.")

    def edit_exit():
        msgbox = messagebox.askquestion('확인', 'edit를 종료하시겠습니까?')
        if msgbox == 'yes':
            window.quit()



    checklist.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=checklist.yview)
    checklist.configure(state="disabled")
    btn1 = tk.Button(frame1, text='불러오기', command=lambda: save(), width=20, height=3)
    btn2 = tk.Button(frame1, text='저장', command = lambda: saving(point,ck_var,df), width=20, height=3)
    btn3 = tk.Button(frame1, text='종료', command = lambda : edit_exit(), width=20, height=3)
    btn1.pack()
    btn2.pack()
    btn3.pack()

    window.mainloop()

if __name__ == '__main__':
    main()





