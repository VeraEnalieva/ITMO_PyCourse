# coding: utf-8

import random


class GameExeptions(object):

    def existance_choise(self):
        print ('Эта клетка уже была взорвана. Выберите другую клетку.')

    def out_of_range(self):
        print ('Клетки с таким названием не существует.')

    def existance_ship(self):   # На случай, если дойдёт до двух игроков
        print('В Вашем арсенале уже нет такого корабля.  Выберите пожалуйста другой корабль.')


# Базовый класс для корабля
class Ship(object):

    def __init__(self, count, type):
        self.count = count      # количество кораблей
        self.type = type        # палубность


    def draw_ship(self):
        for i in range(self.count):
            print ('='*self.type, ' ')


#
# # Создаём корабли
ship_type_4 = Ship(1, 4)
ship_type_3 = Ship(2, 3)
ship_type_2 = Ship(3, 2)
ship_type_1 = Ship(4, 1)

# Рисуем новые корабли
ship_type_4.draw_ship()
ship_type_3.draw_ship()
ship_type_2.draw_ship()
ship_type_1.draw_ship()



# # Создаём ячейки
row = [i for i in range(10)]
vertik = list("ABCDEFGHIJ")
cell_new = [str(v)+str(i) for i in row for v in vertik]
print(cell_new)

# Возможные значения для ячеек
cell_value_symbol = ['O', '=', '*', '+']

# Базовый класс для поля
class Cell(object):

    def __init__(self, cell_name, cell_value):
        self.cell_name = cell_name
        self.cell_value = cell_value


    def draw_cell(self, dict_name, cell_name):
        if cell_name in dict_name:
            print (cell_value_symbol[2])


    def draw_smart_Cell(self):                       # Рисуем умное поле, из словаря.
        pass


    def draw_Cell(self):                                  # Просто рисуем начальное поле. Видимо только один раз, а может и вообще не понадобится....
        #print ('    ', [a for a in range(1,11)])
        print ('    A   B   C   D   E   F   G   H   I   J')
        n = 0
        for i in range(10):
            print (n, ' ', 'O   '*10)
            n+=1
        print ('\nВыберите клетку для удара: ')


cell = Cell('A2','+')
cell.draw_cell(cell_new,'A2')
# Пока только одно поле и один пользователь. Потом можно сделать двух, как в классическом бое
class GamerName(object):
    pass

class UserMenu(object):

    def get_start(self):
        print ('\nХотите разбить флот-неведимку адмирала Тельняшкина?\n')
        print ('''Немножно подскажу. В его арсенале всего лишь 10 кораблей:\n
        Четырёхпалубных   1 шт
        Трёхпалубных      2 шт
        Двухпалубных      3 шт
        Однопалубных      4 шт
        ''')


#UserMenu.get_start()
#Cell.draw_Cell()

