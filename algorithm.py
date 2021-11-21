
import random

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
    #print(list1)
    #print(list2)
    #print(sum(list2))
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
    #print(dist_results)
    return aggregator

people_num = 20
positive_num = 10
rand_num = 5
border = 10
test_results = [0] * people_num
positive_list = random.sample(range(0, people_num), positive_num)
for i in range(positive_num):
    test_results[positive_list[i]] = 1
ret = algorithm(test_results, rand_num, border)
print(ret)
