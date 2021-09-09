import itertools
import random
import pandas as pd
import sys, os
# data = pd.read_csv("C:/Users/eoxhd/Desktop/통합.csv")
# with open("C:/Users/eoxhd/Desktop/keyword.txt", 'r', encoding='UTF-8') as file:
#     key = file.readlines()
# key1 = []
# for i in key:
#     key1.append(i[:-1])
# key = key1
def main(data,key):
    path = "C:/Users/eoxhd/PycharmProjects/YoutubeAl/bigdata_set.csv"
    if getattr(sys, 'frozen', False):
        path = os.path.join(sys._MEIPASS, "bigdata_set.csv")

    df = pd.read_csv(path)
    def overlap(a):
        new_list = []
        for i in a:
            if i not in new_list:
                new_list.append(i)
        return new_list

    viewlog = overlap(data['시청기록'])
    keylog = key
    seedsubscribe = overlap(data['업데이트영상'])
    subscribelog = []
    for i in range(len(seedsubscribe)):
        if seedsubscribe[i] not in viewlog:
            subscribelog.append(seedsubscribe[i])
    count = 16
    seedview = []

    def filtering(a,b):
        for i in a:
            filter = b.append(df[df['영상제목'].str.contains(i)])
        return b

    def transform(a):
        for i in range(len(a)):
            a[i] = a[i].values.tolist()
        return a


    filtering(keylog, seedview)
    transform(seedview)
    seedview = list(itertools.chain(*seedview))
    seedview2 = overlap(seedview)
    seedview3 = []
    for i in range(len(seedview2)):
        if seedview2[i] not in viewlog:
            seedview3.append(seedview2[i])
    seed = []
    for i in range(len(seedview3)):
        seed.append(seedview[i][1])
    seed = random.sample(seed,count) + random.sample(subscribelog,4)
    random.shuffle(seed)

    return seed

if __name__ == '__main__':
    main()




