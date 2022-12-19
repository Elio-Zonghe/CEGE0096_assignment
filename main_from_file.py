# -*- coding: utf-8 -*-
from class_collection import Csv
from class_collection import MBR
from class_collection import PiP

# input points and polygon from files
point = Csv('input.csv')
point_lst = point.read()
polygon = Csv('polygon.csv')
polygon_lst = polygon.read()

# MBR
mbr = MBR(polygon_lst)
mbr.get_polygon()
mbr.show()

# PiP
pip = PiP(polygon_lst, point_lst)
pip.rca()
pip.show()

# Exporting CSV files
pip.output()

