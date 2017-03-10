# coding: utf-8

print ('''Привет :-) ,
Эта программа определяет является ли введённый текст полиндромом''')
def polindrom(x):
    revrs = x[::-1]
    if revrs == x:
        print ('Это полиндром')
    else:
        print ('Это не полиндром')

polindrom(str(input('Наберите текст: \n')))


