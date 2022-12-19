from plotter import Plotter


# ******File Description******
# This file organises the custom classes and functions used in main_from_file and main_from_user
# For readability purposes
# ****************************


class Geometry:
    def __init__(self, id_):
        self.__id = id_

    def get_id(self):
        return self.__id


class Point(Geometry):
    def __init__(self, id_, x, y, kind=None, count=0):
        super().__init__(id_)
        self.x = x
        self.y = y
        self.kind = kind
        self.count = count

    def set_kind(self, kind):
        self.kind = kind

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_kind(self):
        return self.kind

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count


class Line(Geometry):
    def __init__(self, name, point_1, point_2):
        super().__init__(name)
        self.__point_1 = point_1
        self.__point_2 = point_2


class Polygon(Geometry):
    def __init__(self, name, points):
        super().__init__(name)
        self.__points = points

    def get_points(self):
        return self.__points

    def lines(self):
        res = []
        points = self.get_points()
        point_a = points[0]
        for point_b in points[1:]:
            res.append(Line(point_a.get_name() + '-' + point_b.get_name(), point_a, point_b))
            point_a = point_b
            res.append(Line(point_a.get_name() + '-' + points[0].get_name(), point_a, points[0]))
        return res


class Csv:
    def __init__(self, path):  # pass the file path as an argument to the main function
        self.path = path

    def read(self):
        with open(self.path, 'r') as f:
            point_lst = []
            for points in f.readlines()[1:]:
                ID, X, Y = points.split(',')
                X, Y = float(X), float(Y)
                point = Point(ID, X, Y)
                point_lst.append(point)
            # print(point_lst)
        return point_lst

    def output(self, output):
        with open(output, 'w') as f:
            f.write('ID' + ',' + 'Category\n')
            for point in self.path:
                f.write(f'{point.get_id()},{point.get_kind()}\n')


def is_odd(num):
    if (num % 2) == 0:
        res = True
    else:
        res = False
    return res


class MBR(Point):
    def __init__(self, polygon_lst):
        self.polygon_lst = polygon_lst

    def get_polygon(self):
        ppx, ppy = [], []
        for pp in self.polygon_lst:  # pp_x,pp_y stand for the x and y value of a point coordinate from the polygon_csv list respectively
            pp_x = pp.get_x()
            pp_y = pp.get_y()
            ppx.append(pp_x)  # ppx,ppy are the list of the x and y value of points from polygon
            ppy.append(pp_y)
        ppx_min, ppx_max, ppy_min, ppy_max = min(ppx), max(ppx), min(ppy), max(ppy)
        endpoint1 = Point('endpoint1', ppx_min, ppy_min)
        endpoint2 = Point('endpoint2', ppx_min, ppy_max)
        endpoint3 = Point('endpoint3', ppx_max, ppy_max)
        endpoint4 = Point('endpoint4', ppx_max, ppy_min)
        mbr_lst = [endpoint1, endpoint2, endpoint3, endpoint4]
        return mbr_lst

    def show(self):
        mbr = MBR(self.polygon_lst)
        mbr_lst = mbr.get_polygon()

        print('*********************From MBR*************************')
        print(f'The bottom left point is: {(mbr_lst[0].get_x(), mbr_lst[0].get_y())}')
        print(f'The upper left point is: {(mbr_lst[1].get_x(), mbr_lst[1].get_y())}')
        print(f'The upper right point is: {(mbr_lst[2].get_x(), mbr_lst[2].get_y())}')
        print(f'The bottom right point is: {(mbr_lst[3].get_x(), mbr_lst[3].get_y())}')
        print('******************************************************')

    def add_mbr(self):
        plt = Plotter()
        ppx, ppy, px, py = [], [], [], []
        mbr = MBR(self.polygon_lst)
        mbr_plst = mbr.get_polygon()
        for p in mbr_plst:
            px.append(p.get_x())
            py.append(p.get_y())
        for pp in self.polygon_lst:
            ppx.append(pp.get_x())
            ppy.append(pp.get_y())
        plt.add_mbr(px, py)
        plt.add_polygon(ppx, ppy)


class PiP(MBR):

    def __init__(self, polygon_lst, point_lst):
        self.point_lst = point_lst
        self.polygon_lst = polygon_lst

    def rca(self):
        mbr = MBR(self.polygon_lst)
        mbr_plst = mbr.get_polygon()

        for p in self.point_lst:  # Find 'kind' = 'outside' based on MBR
            if p.get_x() > mbr_plst[2].get_x() or p.get_x() < mbr_plst[0].get_x() or p.get_y() > mbr_plst[1].get_y() or p.get_y() < mbr_plst[0].get_y():
                p.set_kind('outside')

        for p in self.point_lst:  # Determine the intersection of each input point with a polygon edge
            if p.get_kind() is None:  # Exclude points that have already been identified with 'kind'
                pre = self.polygon_lst[0]  # cur stands for current and pre stands for the previous point from polygon_lst
                for cur in self.polygon_lst[1:]:

                    if cur.get_y() >= pre.get_y():  # Set the higher end of each edge to B and the lower end to A
                        A = pre
                        B = cur
                    else:
                        A = cur
                        B = pre

                    if A.get_y() <= p.get_y() <= B.get_y():
                        AB = [B.get_x() - A.get_x(), (B.get_y() - A.get_y())]
                        AP = [p.get_x() - A.get_x(), (p.get_y() - A.get_y())]
                        res1 = AB[0] * AP[1] - AB[1] * AP[0]  # Calculate the vector product(res1) of vectors AB and AP

                        # Determine the position of the point P and edge AB according to  the res1 (reference: https://blog.csdn.net/qq_27606639/article/details/80911006)
                        if res1 == 0:  # P is co-linear with the segment AB
                            if min(A.get_x(), B.get_x()) <= p.get_x() <= max(A.get_x(), B.get_x()):
                                p.set_kind('boundary')
                        elif res1 > 0:  # P is to the left of segment AB
                            p.set_count(p.get_count() + 1)
                        elif res1 < 0:  # P is to the right of segment AB
                            p.set_count(p.get_count())

                    pre = cur

        for p in self.point_lst:
            if p.get_kind() is None:
                if p.get_count() == 0:
                    p.set_kind('outside')

        # Special cases
        for p in self.point_lst:
            if p.get_kind() is None:
                i = -2
                while i < len(self.polygon_lst) - 2:
                    if p.get_y() == self.polygon_lst[i].get_y() and p.get_x() < self.polygon_lst[i].get_x():  # Find the point i from vertices of the polygon whose y-value is equal to that of the P and to the right of P
                        C = self.polygon_lst[i - 1]
                        D = self.polygon_lst[i + 1]

                        res2 = (C.get_y() - p.get_y()) * (
                                D.get_y() - p.get_y())  # Determine the position of points C & D in front of and behind point i in relation to ray P

                        if res2 < 0:  # C, D on either side of the ray P
                            p.set_count(p.get_count() - 1)
                        elif res2 > 0:  # C, D on the same side of the ray P
                            p.set_count(p.get_count())
                        elif res2 == 0:  # C, D and P are on the common line

                            E = self.polygon_lst[i + 2]
                            res3 = (C.get_y() - p.get_y()) * (
                                    E.get_y() - p.get_y())  # Determine the position of ray P in relation to C adn E (the second point after i) by res3

                            if res3 > 0:  # C, E on either side of the ray P
                                p.set_count(p.get_count())
                            elif res3 < 0:  # C, E on the same side of the ray P
                                p.set_count(p.get_count() - 1)
                            else:  # C, E and P are on the common line again
                                p.set_count(p.get_count())
                    i += 1

        for p in self.point_lst:
            if p.get_kind() is None:
                if is_odd(int(p.get_count())):
                    p.set_kind('outside')
                else:
                    p.set_kind('inside')

    def show(self):
        plt = Plotter()
        mbr = MBR(self.polygon_lst)
        mbr_plst = mbr.get_polygon()

        for p in self.point_lst:
            plt.add_point(p.get_x(), p.get_y(), p.get_kind())

        for p in self.point_lst:
            if not (p.get_x() > mbr_plst[2].get_x() or p.get_x() < mbr_plst[0].get_x() or p.get_y() > mbr_plst[1].get_y() or p.get_y() < mbr_plst[0].get_y()):
                if p.get_kind() != 'boundary':
                    plt.add_ray([p.get_x(), (mbr_plst[2].get_x() + 0.75)], [p.get_y(), p.get_y()], p.get_kind())

        ppx, ppy = [], []
        for pp in self.polygon_lst:
            ppx.append(pp.get_x())
            ppy.append(pp.get_y())

        plt.add_polygon(ppx, ppy)
        plt.show()

    def output(self,new_name= ''):
        result = Csv(self.point_lst)
        result.output('output.csv')

