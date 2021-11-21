from tkinter import *
import sqlite3
import tkinter.messagebox
import random

root = Tk()
root.title('Query positive number')
root.minsize(400,200)

num = StringVar()
num.set('')
ret_positive = Label(root, textvariable = num).place(x = 100, y = 110)

def random_distribution(amount,num, border):
    list1 = []
    for i in range(0,num-1):
        a = random.randint(-border,amount)
        list1.append(a)
    list1.sort()
    list1.append(amount)

    list2 = []
    for i in range(len(list1)):
        if i == 0:
            b = list1[i]
        else:
            b = list1[i] - list1[i-1]
        list2.append(b)
    return list2

def algorithm(test_results, rand_num, border):
    aggregator = 0
    total_num = len(test_results)
    dist_results = [0]*total_num
    for i in range(total_num):
        p_i = test_results[i]
        rand_list=random_distribution(p_i, rand_num, border)
        rand_p_list = random.sample(range(0, total_num), rand_num)
        for j in range(len(rand_p_list)):
            dist_results[rand_p_list[j]] += rand_list[j]
    aggregator = sum(dist_results)
    return aggregator


def query(root, label):
    number = label.get()
    people_num = int(number)
    positive_num = int(people_num * 0.1)
    rand_num = 5
    border = 10
    test_results = [0] * people_num
    positive_list = random.sample(range(0, people_num), positive_num)
    for i in range(positive_num):
        test_results[positive_list[i]] = 1
    ret = algorithm(test_results, rand_num, border)
    num.set(ret)

def exit_program():
    quit()

def main():

#input：组别 positive
#output：group有几个positive
    input_name = Label(root, text = 'Please enter the total number of residents :').place(x = 30, y = 30)
    label = StringVar()
    entry = Entry(root,bg='#ffffff',width=15,textvariable=label).place(x=30,y=50,anchor='nw')
    query_button = Button(root,bg='white',text='Query',width=8,height=1,
                           command=lambda :query(root, label)).place(x=30,y=75,anchor='nw')
    #exit_button = Button(root,bg='white',text='Exit',width=8,height=1, command=lambda :exit_program()).place(x=380,y=75,anchor='nw')
    ret_positive = Label(root, text = 'Positive：').place(x = 30, y = 110)

    root.mainloop()

main()
