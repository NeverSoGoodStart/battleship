import copy
import argparse
import time
import sys

dire = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
dir1 = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def read_from_file(file):
    lines = open(file).readlines()
    row = [int(x) for x in lines[0].strip()]
    col = [int(x) for x in lines[1].strip()]
    ship = [int(x) for x in lines[2].strip()]
    n = len(row)
    assignment = []
    pri1 = []
    pri2 = []
    for i in range(n):
        tem = []
        for j in range(n):
            tem.append(-1)
        assignment.append(tem)
    for i in range(n):
        for j in range(n):
            tem = lines[i + 3].strip()
            if tem[j] == '.':
                assignment[i][j] = 0
            elif tem[j] == 'S':
                assignment[i][j] = 1
                if i > 0:
                    assignment[i - 1][j] = 0
                    if j > 0:
                        assignment[i - 1][j - 1] = 0
                    if j < n - 1:
                        assignment[i - 1][j + 1] = 0
                if i < n - 1:
                    assignment[i + 1][j] = 0
                    if j > 0:
                        assignment[i + 1][j - 1] = 0
                    if j < n - 1:
                        assignment[i + 1][j + 1] = 0
                if j > 0:
                    assignment[i][j - 1] = 0
                if j < n - 1:
                    assignment[i][j + 1] = 0
            elif tem[j] == 'M':
                assignment[i][j] = 2
                if i > 0:
                    pri2.append((i - 1, j))
                    if j > 0:
                        assignment[i - 1][j - 1] = 0
                    if j < n - 1:
                        assignment[i - 1][j + 1] = 0
                if i < n - 1:
                    pri2.append((i + 1, j))
                    if j > 0:
                        assignment[i + 1][j - 1] = 0
                    if j < n - 1:
                        assignment[i + 1][j + 1] = 0
                if j > 0:
                    pri2.append((i, j - 1))
                if j < n - 1:
                    pri2.append((i, j + 1))
            elif tem[j] == '<':
                assignment[i][j] = 1
                assignment[i][j + 1] = 1
                pri1.append((i, j + 1))
                if i > 0:
                    assignment[i - 1][j] = 0
                    assignment[i - 1][j + 1] = 0
                if i < n - 1:
                    assignment[i + 1][j] = 0
                    assignment[i + 1][j + 1] = 0
                if j > 0:
                    assignment[i][j - 1] = 0
                if i > 0:
                    if j > 0:
                        assignment[i - 1][j - 1] = 0
                    if j < n - 2:
                        assignment[i - 1][j + 2] = 0
                if i < n - 1:
                    if j > 0:
                        assignment[i + 1][j - 1] = 0
                    if j < n - 2:
                        assignment[i + 1][j + 2] = 0
            elif tem[j] == '>':
                assignment[i][j] = 1
                assignment[i][j - 1] = 1
                pri1.append((i, j - 1))
                if i > 0:
                    assignment[i - 1][j] = 0
                    assignment[i - 1][j - 1] = 0
                if i < n - 1:
                    assignment[i + 1][j] = 0
                    assignment[i + 1][j - 1] = 0
                if j < n - 1:
                    assignment[i][j + 1] = 0
                if i > 0:
                    if j > 1:
                        assignment[i - 1][j - 2] = 0
                    if j < n - 1:
                        assignment[i - 1][j + 1] = 0
                if i < n - 1:
                    if j > 1:
                        assignment[i + 1][j - 2] = 0
                    if j < n - 1:
                        assignment[i + 1][j + 1] = 0
            elif tem[j] == '^':
                assignment[i][j] = 1
                assignment[i + 1][j] = 1
                pri1.append((i + 1, j))
                if j > 0:
                    assignment[i][j - 1] = 0
                    assignment[i + 1][j - 1] = 0
                if j < n - 1:
                    assignment[i][j + 1] = 0
                    assignment[i + 1][j + 1] = 0
                if i > 0:
                    assignment[i - 1][j] = 0
                if i > 0:
                    if j > 1:
                        assignment[i - 1][j - 1] = 0
                    if j < n - 1:
                        assignment[i - 1][j + 1] = 0
                if i < n - 2:
                    if j > 1:
                        assignment[i + 2][j - 1] = 0
                    if j < n - 1:
                        assignment[i + 2][j + 1] = 0
            elif tem[j] == 'v':
                assignment[i][j] = 1
                assignment[i - 1][j] = 1
                pri1.append((i - 1, j))
                if j > 0:
                    assignment[i][j - 1] = 0
                    assignment[i - 1][j - 1] = 0
                if j < n - 1:
                    assignment[i][j + 1] = 0
                    assignment[i - 1][j + 1] = 0
                if i < n - 1:
                    assignment[i + 1][j] = 0
                if i > 1:
                    if j > 1:
                        assignment[i - 2][j - 1] = 0
                    if j < n - 1:
                        assignment[i - 2][j + 1] = 0
                if i < n - 1:
                    if j > 1:
                        assignment[i + 1][j - 1] = 0
                    if j < n - 1:
                        assignment[i + 1][j + 1] = 0
    org_csp = CSP(row, col, ship, assignment, pri1, pri2)
    return org_csp


class CSP:
    def __init__(self, row, col, ship, assignment, pri1, pri2):
        self.row = row
        self.col = col
        self.ship = ship
        self.assignment = assignment
        self.lst = []
        self.n = len(row)
        self.pri1 = pri1
        self.pri2 = pri2
        for i in range(self.n):
            for j in range(self.n):
                if assignment[i][j] == -1:
                    self.lst.append((i, j))

    def __str__(self):
        res=[]
        for i in range(self.n):
            tem=[]
            for j in range(self.n):
                tem.append('.')
            res.append(tem)
        seen = []
        for i in range(self.n):
            for j in range(self.n):
                tem_ship=[]
                if self.assignment[i][j] > 0 and (i, j) not in seen:
                    seen.append((i, j))
                    tem_ship.append((i,j))
                    if j + 1 < self.n and self.assignment[i][
                        j + 1] > 0:
                        count = 2
                        tem_j = j + 1
                        seen.append((i, j + 1))
                        tem_ship.append((i,j+1))
                        while tem_j + 1 < self.n and self.assignment[i][
                            tem_j + 1] > 0:
                            count += 1
                            tem_j += 1
                            seen.append((i, tem_j))
                            tem_ship.append((i,tem_j))
                        for ii in range(len(tem_ship)):
                            if ii==0:
                                res[tem_ship[ii][0]][tem_ship[ii][1]]='<'
                            elif ii==len(tem_ship)-1:
                                res[tem_ship[ii][0]][tem_ship[ii][1]]='>'
                            else:
                                res[tem_ship[ii][0]][tem_ship[ii][1]]='M'
                    elif i + 1 < self.n and self.assignment[i + 1][
                        j] > 0:
                        count = 2
                        tem_i = i + 1
                        seen.append((i + 1, j))
                        tem_ship.append((i+1,j))
                        while tem_i + 1 < self.n and \
                                self.assignment[tem_i + 1][j] > 0:
                            count += 1
                            tem_i += 1
                            seen.append((tem_i, j))
                            tem_ship.append((tem_i,j))
                        for ii in range(len(tem_ship)):
                            if ii==0:
                                res[tem_ship[ii][0]][tem_ship[ii][1]]='^'
                            elif ii==len(tem_ship)-1:
                                res[tem_ship[ii][0]][tem_ship[ii][1]]='v'
                            else:
                                res[tem_ship[ii][0]][tem_ship[ii][1]]='M'
                    else:
                        res[i][j]='S'
        res1=''
        for i in range(self.n):
            tem=''
            for j in range(self.n):
                tem+=res[i][j]
            res1+=tem+'\n'
        return res1

    def complete(self):
        return self.lst == []

    def backtrack(self):
        if self.complete():
            return self
        var = self.select_unassign_variable()
        for value in [1, 0]:
            new_csp = copy.deepcopy(self)
            checker = new_csp.check_valid(var, value)
            if checker:
                new_csp.assignship(var,value)
                res = new_csp.backtrack()
                if res is not None:
                    return res
        return None

    def assignship(self, var, value):
        if value == 0:
            self.assignment[var[0]][var[1]] = 0
            if var in self.lst:
                self.lst.remove(var)
        elif value == 1:
            self.assignment[var[0]][var[1]] = 1
            if var in self.lst:
                self.lst.remove(var)
            for d in dire:
                tem_x = d[1] + var[1]
                tem_y = d[0] + var[0]
                if -1 < tem_y < self.n and -1 < tem_x < self.n:
                    self.assignment[tem_y][tem_x] = 0
                    if (tem_y, tem_x) in self.lst:
                        self.lst.remove((tem_y, tem_x))

    def check_valid(self, var, value):
        checker1 = self.check_row_col(var, value)
        if not checker1:
            return False
        checker2 = self.check_ship(var, value)
        if not checker2:
            return False
        return True

    def check_row_col(self, var, value):
        tem_assign = copy.deepcopy(self.assignment)
        tem_assign[var[0]][var[1]] = value
        for i in range(self.n):
            tem_row = tem_assign[i]
            res1 = self.check_single_row(tem_row, i)
            if not res1:
                return False
        for i in range(self.n):
            tem_col = []
            for j in range(self.n):
                tem_col.append(self.assignment[j][i])
            res2 = self.check_single_col(tem_col, i)
            if not res2:
                return False
        return True

    def check_ship(self, var, value):
        if var in self.lst:
            self.lst.remove(var)
        self.assignment[var[0]][var[1]] = value
        if self.lst:
            if value == 0:
                for dir in dir1:
                    tem_y = var[0] + dir[0]
                    tem_x = var[1] + dir[1]
                    if -1 < tem_y < self.n and -1 < tem_x < self.n and \
                            self.assignment[tem_y][tem_x] == 2:
                        jug = 0
                        for d in dir1:
                            tem_y1 = tem_y + dir[0]
                            tem_x1 = tem_x + dir[1]
                            if -1 < tem_y1 < self.n and -1 < tem_x1 < self.n and \
                                    self.assignment[tem_y][tem_x] == 1:
                                jug = 1
                                break
                        if jug == 0:
                            return False
                return True
            else:
                tem0 = var[0]
                tem1 = var[1]
                count = -1
                while -1 < tem0 < self.n - 1 and self.assignment[tem0][
                    tem1] > 0:
                    count += 1
                    tem0 += 1
                    tem11 = tem1 - 1
                    tem12 = tem1 + 1
                    if -1 < tem11 < self.n and self.assignment[tem0][
                        tem11] > 0:
                        return False
                    if -1 < tem12 < self.n and self.assignment[tem0][
                        tem12] > 0:
                        return False
                tem0 = var[0]
                tem1 = var[1]
                while -1 < tem0 < self.n - 1 and self.assignment[tem0][
                    tem1] > 0:
                    count += 1
                    tem0 -= 1
                    tem11 = tem1 - 1
                    tem12 = tem1 + 1
                    if -1 < tem11 < self.n and self.assignment[tem0][
                        tem11] > 0:
                        return False
                    if -1 < tem12 < self.n and self.assignment[tem0][
                        tem12] > 0:
                        return False
                if count > 4:
                    return False
                tem0 = var[0]
                tem1 = var[1]
                count = -1
                while -1 < tem1 < self.n - 1 and self.assignment[tem0][
                    tem1] > 0:
                    count += 1
                    tem1 += 1
                    tem01 = tem0 - 1
                    tem02 = tem0 + 1
                    if -1 < tem01 < self.n and self.assignment[tem01][tem1] > 0:
                        return False
                    if -1 < tem02 < self.n and self.assignment[tem02][tem1] > 0:
                        return False
                tem0 = var[0]
                tem1 = var[1]
                while 0 < tem1 < self.n and self.assignment[tem0][
                    tem1] > 0:
                    count += 1
                    tem1 -= 1
                    tem01 = tem0 - 1
                    tem02 = tem0 + 1
                    if -1 < tem01 < self.n and self.assignment[tem01][
                        tem1] > 0:
                        return False
                    if -1 < tem02 < self.n and self.assignment[tem02][
                        tem1] > 0:
                        return False
                if count > 4:
                    return False
                return True
        if not self.lst:
            seen = []
            num_ship = [0, 0, 0, 0]
            for i in range(self.n):
                for j in range(self.n):
                    if self.assignment[i][j] > 0 and (i, j) not in seen:
                        seen.append((i, j))
                        if j + 1 < self.n and self.assignment[i][
                            j + 1] > 0:
                            count = 2
                            tem_j = j + 1
                            seen.append((i, j + 1))
                            while tem_j + 1 < self.n and self.assignment[i][
                                tem_j + 1] > 0:
                                count += 1
                                tem_j += 1
                                seen.append((i, tem_j))
                            if count > 4:
                                return False
                            num_ship[count - 1] += 1
                        elif i + 1 < self.n and self.assignment[i + 1][
                            j] > 0:
                            count = 2
                            tem_i = i + 1
                            seen.append((i + 1, j))
                            while tem_i + 1 < self.n and \
                                    self.assignment[tem_i + 1][j] > 0:
                                count += 1
                                tem_i += 1
                                seen.append((tem_i, j))
                            if count > 4:
                                return False
                            num_ship[count - 1] += 1
                        else:
                            num_ship[0] += 1
            return num_ship == self.ship

    def select_unassign_variable(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.assignment[i][j] == -1:
                    return (i,j)

    def check_single_row(self, tem_row, j):
        minus_one = 0
        one = 0
        for item in tem_row:
            if item == -1:
                minus_one += 1
            if item > 0:
                one += 1
        if one - 1 < self.row[j] < one + minus_one + 1:
            return True
        return False

    def check_single_col(self, tem_col, j):
        minus_one = 0
        one = 0
        for item in tem_col:
            if item == -1:
                minus_one += 1
            if item > 0:
                one += 1
        if one - 1 < self.col[j] < one + minus_one + 1:
            return True
        return False


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    csp = read_from_file(args.inputfile)
    final_csp = csp.backtrack()
    sys.stdout = open(args.outputfile, 'w')
    print(final_csp)
    sys.stdout = sys.__stdout__
