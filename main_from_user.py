# -*- coding: utf-8 -*-
from class_collection import Csv
from class_collection import MBR
from class_collection import PiP
from class_collection import Point


# Input points from keyboard
point_lst = []
i = 1
print("Please input the points in 'x,y' format")
print('ENTER and continue to input the next point, ending with consecutive ENTERs')

while True:
    input_tuple = tuple(input(f'The point_{i} is: ').split(','))  # pass a tuple pairs as an argument to a main function
    if input_tuple[0] == '':
        break
    else:
        ID = str(i)
        X, Y = input_tuple[0], input_tuple[1]
        X, Y = float(X), float(Y)
        point = Point(ID, X, Y)
        point_lst.append(point)
        i += 1

polygon = Csv('polygon.csv')
polygon_lst = polygon.read()

# MBR
mbr = MBR(polygon_lst)
mbr.get_polygon()

# PiP
pip = PiP(polygon_lst, point_lst)
pip.rca()


# Exporting CSV files
enq = input('Would you like to output the results as a csv? [y/n]')
if enq == 'y':
    result = Csv(point_lst)
    result.output(input("Please enter a file name as 'name.csv': "))
elif enq == 'n':
    print('Results will not be stored.')
else:
    print('Invalid input and no result file saved.')

pip.show()

