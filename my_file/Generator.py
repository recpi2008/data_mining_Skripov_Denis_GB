# a = []
# for i in range(1,11):
#     a.append(i**2)
# print(a)

# Генератор списка / list comprehension
# a = [i**2 for i in range(1,11)]
# print(a)

#Итератор
# s = [1,2,3]
# d = iter(s)
# print(next(d))
# print(next(d))
# print(next(d))
# print(next(d))

#Гениратор
# b = (i**2 for i in range(1,11))
# print(next(b))
# print(next(b))
# print(next(b))
# print(next(b))

# Функция генератор
# def gen_d():
#     for i in [1,2,3]:
#         yield i
# s = gen_d()
# print(next(s))
# print(next(s))
# print(next(s))
#
# for i in gen_d():
#     print(i)

def fact(n):
    pr = 1
    s = []
    for i in range(1,n+1):
        pr *=i
        s.append(pr)
    return s
print(fact(10))

def fact_gen(n):
    pr = 1
    for i in range(1,n+1):
        pr *=i
        yield pr
# s = fact_gen(10)
# print(next(s))
# print(next(s))
# print(next(s))
# print(next(s))

for i in fact_gen(10):
    print(i, end=" ")


