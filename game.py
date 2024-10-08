import itertools


class Game:
    def __init__(self):
        import tkinter as tk

        self.canvas = tk.Canvas(width=1920, height=1080)
        self.canvas.pack()
        self.counter = 0

        # nic-0, pesiakb-1, konb-2, strelecb-3, vezab-4, kralovnab-5, kralb-6,pesiakc-7, konc-8, strelecc-9, vezac-10, kralovnac-11, kralc-12
        self.board = [
            [[10, 0], [8, 0], [9, 0], [11, 0], [12, 0], [9, 0], [8, 0], [10, 0]],
            [[7, 0] for _ in range(8)],
            [[0, 0] for _ in range(8)],
            [[0, 0] for _ in range(8)],
            [[0, 0] for _ in range(8)],
            [[0, 0] for _ in range(8)],
            [[1, 0] for _ in range(8)],
            [[4, 0], [2, 0], [3, 0], [5, 0], [6, 0], [3, 0], [2, 0], [4, 0]],
        ]

        self.sur = [-1, -1]
        self.empasant = [-1, -1]
        self.rbl, self.rbp, self.rcl, self.rcp = 0, 0, 0, 0
        self.cur_player = 0

        self.maxdepth = 3
        self.create_board()
        self.images = self.loadimages()
        self.init_board()
        self.canvas.bind("<Button-1>", self.klik)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.canvas.mainloop()

    def create_board(self):
        farba = 1
        for y in range(8):
            farba = not farba
            for x in range(8):
                self.canvas.create_rectangle(
                    50 + x * 90,
                    50 + y * 90,
                    140 + x * 90,
                    140 + y * 90,
                    fill="#573a2e" if farba else "#fccc74",
                )
                farba = not farba
                self.canvas.update()

    def init_board(self):
        for y in range(8):
            for x in range(8):
                if self.board[y][x][0] > 0:
                    self.board[y][x][1] = self.canvas.create_image(
                        95 + 90 * x,
                        95 + 90 * y,
                        image=self.images[self.board[y][x][0] - 1],
                    )
        self.canvas.update()

    def loadimages(self):
        import tkinter as tk

        return [tk.PhotoImage(file=f"{i}.png") for i in range(1, 13)]

    def update_board(self):
        for a in range(8):
            for b in range(8):
                self.canvas.delete(self.board[a][b][1])
        self.init_board()

    def klik(self, event):
        if 0 <= (event.y - 50) // 90 <= 7 and 0 <= (event.x - 50) // 90 <= 7:
            self.sur[0] = (event.x - 50) // 90
            self.sur[1] = (event.y - 50) // 90

    def drag(self, event):
        if 0 <= (event.y - 50) // 90 <= 7 and 0 <= (event.x - 50) // 90 <= 7:
            self.canvas.coords(
                self.board[self.sur[1]][self.sur[0]][1], event.x, event.y
            )

    def release(self, event):
        if self.board[self.sur[1]][self.sur[0]][0] > 6:
            self.update_board()
            return 0
        if (
            0 <= (event.y - 50) // 90 <= 7
            and 0 <= (event.x - 50) // 90 <= 7
            and self.board[self.sur[1]][self.sur[0]][0] != 0
            and self.validator((event.y - 50) // 90, (event.x - 50) // 90)
        ):
            self.board[(event.y - 50) // 90][(event.x - 50) // 90][0] = self.board[
                self.sur[1]
            ][self.sur[0]][0]
            if (event.y - 50) // 90 != self.sur[1] or (event.x - 50) // 90 != self.sur[
                0
            ]:
                self.board[self.sur[1]][self.sur[0]][0] = 0
                self.ai_move()
        self.update_board()

    def valid(self, y, x):
        if (
            0 < self.board[self.sur[1]][self.sur[0]][0] < 7
            and 0 < self.board[y][x][0] < 7
            or self.board[self.sur[1]][self.sur[0]][0] > 6
            and self.board[y][x][0] > 6
        ):  # su rovnaka farba
            return 0

        if self.board[self.sur[1]][self.sur[0]][0] == 1:  # biely pesiak
            if self.sur[1] - y <= 0:
                return 0
            if self.sur[0] == x:
                if (
                    self.board[y][x][0] != 0
                    or self.board[max(0, self.sur[1] - 1)][self.sur[0]][0] != 0
                ):
                    return 0
                if self.sur[1] - y > 1 and self.sur[1] != 6:
                    return 0
                if self.sur[1] - y > 2:
                    return 0
                if self.sur[1] - y == 2:
                    return 1
            elif self.sur[1] - y > 1:
                return 0
            elif abs(self.sur[0] - x) > 1:
                return 0
            if self.sur[0] != x and (
                self.board[y][x][0] == 0
                and (y != self.empasant[1] and x != self.empasant[0])
            ):
                return 0
            if y == 0:
                self.board[self.sur[1]][self.sur[0]][0] = 5

        if self.board[self.sur[1]][self.sur[0]][0] == 7:  # cierny pesiak
            if y - self.sur[1] <= 0:
                return 0
            if self.sur[0] == x:
                if (
                    self.board[y][x][0] != 0
                    or self.board[min(7, self.sur[1] + 1)][self.sur[0]][0] != 0
                ):
                    return 0
                if y - self.sur[1] > 1 and self.sur[1] != 1:
                    return 0
                if y - self.sur[1] > 2:
                    return 0
                if y - self.sur[1] == 2:
                    return 1
            elif y - self.sur[1] > 1:
                return 0
            elif abs(self.sur[0] - x) > 1:
                return 0
            if self.sur[0] != x and (
                self.board[y][x][0] == 0
                and y != self.empasant[1]
                and x != self.empasant[0]
            ):
                return 0
            if y == 7:
                self.board[self.sur[1]][self.sur[0]][0] = 11

        self.empasant = [-1, -1]
        if self.board[self.sur[1]][self.sur[0]][0] in [2, 8]:  # kon
            if abs(x - self.sur[0]) != 1 or abs(y - self.sur[1]) != 2:
                if abs(x - self.sur[0]) != 2 or abs(y - self.sur[1]) != 1:
                    return 0

        if self.board[self.sur[1]][self.sur[0]][0] in [3, 9]:  # strelec
            if abs(x - self.sur[0]) != abs(y - self.sur[1]):
                return 0
            h, v = 1 if x - self.sur[0] > 0 else -1, 1 if y - self.sur[1] > 0 else -1
            for i in range(1, 10):
                if self.sur[0] + h * i == x and self.sur[1] + v * i == y:
                    break
                if self.board[self.sur[1] + v * i][self.sur[0] + h * i][0] != 0:
                    return 0

        if self.board[self.sur[1]][self.sur[0]][0] in [4, 10]:  # veza
            if x == self.sur[0] and y != self.sur[1]:
                if any(
                    self.board[i][x][0] != 0
                    for i in range(min(y, self.sur[1]) + 1, max(y, self.sur[1]))
                ):
                    return 0
            elif x != self.sur[0] and y == self.sur[1]:
                if any(
                    self.board[y][i][0] != 0
                    for i in range(min(x, self.sur[0]) + 1, max(x, self.sur[0]))
                ):
                    return 0
            else:
                return 0

        if self.board[self.sur[1]][self.sur[0]][0] in [5, 11]:  # kralovna
            if abs(x - self.sur[0]) == abs(y - self.sur[1]):  # je strelec
                h, v = (
                    1 if x - self.sur[0] > 0 else -1,
                    1 if y - self.sur[1] > 0 else -1,
                )
                for i in range(1, 10):
                    if self.sur[0] + h * i == x and self.sur[1] + v * i == y:
                        break
                    if self.board[self.sur[1] + v * i][self.sur[0] + h * i][0] != 0:
                        return 0

            elif x == self.sur[0] and y != self.sur[1]:  # je veza
                if any(
                    self.board[i][x][0] != 0
                    for i in range(min(y, self.sur[1]) + 1, max(y, self.sur[1]))
                ):
                    return 0
            elif x != self.sur[0] and y == self.sur[1]:
                if any(
                    self.board[y][i][0] != 0
                    for i in range(min(x, self.sur[0]) + 1, max(x, self.sur[0]))
                ):
                    return 0
            else:
                return 0

        if self.board[self.sur[1]][self.sur[0]][0] == 6:  # kralb
            if abs(y - self.sur[1]) > 1 or abs(x - self.sur[0]) > 1:
                if y - self.sur[1] != 0:
                    return 0
                if self.rbl == 0 and self.rbp == 0:
                    return 0
                if abs(x - self.sur[0]) != 2:
                    return 0
                if x > self.sur[0]:
                    if not self.rbp or any(
                        [self.board[7][i][0] != 0 for i in range(5, 7)]
                    ):
                        return 0
                else:
                    if not self.rbl or any(
                        [self.board[7][i][0] != 0 for i in range(1, 4)]
                    ):
                        return 0

        if self.board[self.sur[1]][self.sur[0]][0] == 12:  # kralc
            if abs(y - self.sur[1]) > 1 or abs(x - self.sur[0]) > 1:
                if y - self.sur[1] != 0:
                    return 0
                if self.rcl == 0 and self.rcp == 0:
                    return 0
                if abs(x - self.sur[0]) != 2:
                    return 0
                if x > self.sur[0]:
                    if not self.rcp or any(
                        [self.board[0][i][0] != 0 for i in range(5, 7)]
                    ):
                        return 0
                else:
                    if not self.rcl or any(
                        [self.board[0][i][0] != 0 for i in range(1, 4)]
                    ):
                        return 0

        return 1

    def validator(self, y, x):
        if (
            0 < self.board[self.sur[1]][self.sur[0]][0] < 7
            and 0 < self.board[y][x][0] < 7
            or self.board[self.sur[1]][self.sur[0]][0] > 6
            and self.board[y][x][0] > 6
        ):  # su rovnaka farba
            return 0

        if self.board[7][4][0] != 6:
            self.rbl, self.rbp = 0, 0
        if self.board[7][0][0] != 4:
            self.rbl = 0
        if self.board[7][7][0] != 4:
            self.rbp = 0
        if self.board[0][4][0] != 12:
            self.rcl, self.rcp = 0, 0
        if self.board[0][0][0] != 10:
            self.rcl = 0
        if self.board[0][7][0] != 10:
            self.rcp = 0

        if self.board[self.sur[1]][self.sur[0]][0] == 1:  # biely pesiak
            if self.sur[1] - y <= 0:
                return 0
            if self.sur[0] == x:
                if (
                    self.board[y][x][0] != 0
                    or self.board[max(0, self.sur[1] - 1)][self.sur[0]][0] != 0
                ):
                    return 0
                if self.sur[1] - y > 1 and self.sur[1] != 6:
                    return 0
                if self.sur[1] - y > 2:
                    return 0
                if self.sur[1] - y == 2:
                    self.empasant = [x, y + 1]
                    return 1
            elif self.sur[1] - y > 1:
                return 0
            elif abs(self.sur[0] - x) > 1:
                return 0
            if self.sur[0] != x and (
                self.board[y][x][0] == 0
                and (y != self.empasant[1] and x != self.empasant[0])
            ):
                return 0
            if y == self.empasant[1] and x == self.empasant[0]:
                self.board[self.empasant[1] + 1][self.empasant[0]][0] = 0
            if y == 0:
                self.board[self.sur[1]][self.sur[0]][0] = 5

        if self.board[self.sur[1]][self.sur[0]][0] == 7:  # cierny pesiak
            if y - self.sur[1] <= 0:
                return 0
            if self.sur[0] == x:
                if (
                    self.board[y][x][0] != 0
                    or self.board[min(7, self.sur[1] + 1)][self.sur[0]][0] != 0
                ):
                    return 0
                if y - self.sur[1] > 1 and self.sur[1] != 1:
                    return 0
                if y - self.sur[1] > 2:
                    return 0
                if y - self.sur[1] == 2:
                    self.empasant = [x, y - 1]
                    return 1
            elif y - self.sur[1] > 1:
                return 0
            elif abs(self.sur[0] - x) > 1:
                return 0
            if self.sur[0] != x and (
                self.board[y][x][0] == 0
                and y != self.empasant[1]
                and x != self.empasant[0]
            ):
                return 0
            if y == self.empasant[1] and x == self.empasant[0]:
                self.board[self.empasant[1] - 1][self.empasant[0]][0] = 0
            if y == 7:
                self.board[self.sur[1]][self.sur[0]][0] = 11

        self.empasant = [-1, -1]
        if self.board[self.sur[1]][self.sur[0]][0] in [2, 8]:  # kon
            if abs(x - self.sur[0]) != 1 or abs(y - self.sur[1]) != 2:
                if abs(x - self.sur[0]) != 2 or abs(y - self.sur[1]) != 1:
                    return 0

        if self.board[self.sur[1]][self.sur[0]][0] in [3, 9]:  # strelec
            if abs(x - self.sur[0]) != abs(y - self.sur[1]):
                return 0
            h, v = 1 if x - self.sur[0] > 0 else -1, 1 if y - self.sur[1] > 0 else -1
            for i in range(1, 10):
                if self.sur[0] + h * i == x and self.sur[1] + v * i == y:
                    break
                if self.board[self.sur[1] + v * i][self.sur[0] + h * i][0] != 0:
                    return 0

        if self.board[self.sur[1]][self.sur[0]][0] in [4, 10]:  # veza
            if x == self.sur[0] and y != self.sur[1]:
                if any(
                    self.board[i][x][0] != 0
                    for i in range(min(y, self.sur[1]) + 1, max(y, self.sur[1]))
                ):
                    return 0
            elif x != self.sur[0] and y == self.sur[1]:
                if any(
                    self.board[y][i][0] != 0
                    for i in range(min(x, self.sur[0]) + 1, max(x, self.sur[0]))
                ):
                    return 0
            else:
                return 0

        if self.board[self.sur[1]][self.sur[0]][0] in [5, 11]:  # kralovna
            if abs(x - self.sur[0]) == abs(y - self.sur[1]):  # je strelec
                h, v = (
                    1 if x - self.sur[0] > 0 else -1,
                    1 if y - self.sur[1] > 0 else -1,
                )
                for i in range(1, 10):
                    if self.sur[0] + h * i == x and self.sur[1] + v * i == y:
                        break
                    if self.board[self.sur[1] + v * i][self.sur[0] + h * i][0] != 0:
                        return 0

            elif x == self.sur[0] and y != self.sur[1]:  # je veza
                if any(
                    self.board[i][x][0] != 0
                    for i in range(min(y, self.sur[1]) + 1, max(y, self.sur[1]))
                ):
                    return 0
            elif x != self.sur[0] and y == self.sur[1]:
                if any(
                    self.board[y][i][0] != 0
                    for i in range(min(x, self.sur[0]) + 1, max(x, self.sur[0]))
                ):
                    return 0
            else:
                return 0

        if self.board[self.sur[1]][self.sur[0]][0] == 6:  # kralb
            if abs(y - self.sur[1]) > 1 or abs(x - self.sur[0]) > 1:
                if y - self.sur[1] != 0:
                    return 0
                if self.rbl == 0 and self.rbp == 0:
                    return 0
                if abs(x - self.sur[0]) != 2:
                    return 0
                if x > self.sur[0]:
                    if not self.rbp or any(
                        [self.board[7][i][0] != 0 for i in range(5, 7)]
                    ):
                        return 0
                    self.board[7][7][0] = 0
                    self.board[7][5][0] = 4
                else:
                    if not self.rbl or any(
                        [self.board[7][i][0] != 0 for i in range(1, 4)]
                    ):
                        return 0
                    self.board[7][0][0] = 0
                    self.board[7][3][0] = 4

        if self.board[self.sur[1]][self.sur[0]][0] == 12:  # kralc
            if abs(y - self.sur[1]) > 1 or abs(x - self.sur[0]) > 1:
                if y - self.sur[1] != 0:
                    return 0
                if self.rcl == 0 and self.rcp == 0:
                    return 0
                if abs(x - self.sur[0]) != 2:
                    return 0
                if x > self.sur[0]:
                    if not self.rcp or any(
                        [self.board[0][i][0] != 0 for i in range(5, 7)]
                    ):
                        return 0
                    self.board[0][7][0] = 0
                    self.board[0][5][0] = 10
                else:
                    if not self.rcl or any(
                        [self.board[0][i][0] != 0 for i in range(1, 4)]
                    ):
                        return 0
                    self.board[0][0][0] = 0
                    self.board[0][3][0] = 10

        return 1

    def ai_move(self):
        import time

        start = time.perf_counter()
        from copy import deepcopy

        sur = deepcopy(self.sur)

        moves = []
        figures = []
        for y in range(8):
            for x in range(8):
                if self.board[y][x][0] > 6:
                    figures.append((y, x))
        for y, x in figures:
            self.sur = [x, y]
            for yn in range(8):
                for xn in range(8):
                    if self.valid(yn, xn):  #! damy neda naspet pri pesiakoch
                        moves.append((self.get_score(yn, xn), y, x, yn, xn))
        self.sur = sur
        vys = -10000000000
        best = []
        moves.sort(reverse=1)
        for s, y, x, yn, xn in moves:
            v = self.find_best(y, x, yn, xn, 0, 0, vys)
            if v > vys:
                best = [y, x, yn, xn]
                vys = v

        y, x, yn, xn = best
        self.sur = [x, y]
        self.validator(yn, xn)
        self.board[yn][xn] = self.board[y][x]
        self.board[y][x] = [0, 0]
        self.create_board()
        print(self.counter, time.perf_counter() - start)
        self.counter = 0

    def find_best(self, y, x, yn, xn, isblack, depth, best):

        from copy import deepcopy

        old = deepcopy(self.board[yn][xn])
        self.board[yn][xn] = deepcopy(self.board[y][x])
        self.board[y][x] = [0, 0]
        if depth < self.maxdepth:
            moves = []
            for yl in range(8):
                for xl in range(8):
                    if (
                        self.board[yl][xl][0] > 6
                        and isblack
                        or 0 < self.board[yl][xl][0] < 7
                        and not isblack
                    ):
                        self.sur = [xl, yl]
                        for ynl in range(8):
                            for xnl in range(8):
                                if self.valid(ynl, xnl):
                                    moves.append(
                                        (self.get_score(yn, xn), yl, xl, ynl, xnl)
                                    )
            vys = -10000000000 if isblack else 1000000000
            moves.sort(reverse=isblack)

            for s, yl, xl, ynl, xnl in moves:
                v = self.find_best(yl, xl, ynl, xnl, not isblack, depth + 1, vys)
                if isblack and vys >= best or not isblack and vys <= best:
                    break
                vys = max(vys, v) if isblack else min(vys, v)
            self.board[y][x] = deepcopy(self.board[yn][xn])
            self.board[yn][xn] = old

            return vys

        score = self.score()
        self.board[y][x] = deepcopy(self.board[yn][xn])
        self.board[yn][xn] = old
        self.counter += 1
        return score

    def score(self):
        return sum(
            self.get_score(y, x) for y, x in itertools.product(range(8), range(8))
        )

    def get_score(self, y, x):
        dic = {
            0: 0,
            1: -1,
            2: -3,
            3: -3,
            4: -5,
            5: -9,
            6: -10000,
            7: 1,
            8: 3,
            9: 3,
            10: 5,
            11: 9,
            12: 10000,
        }
        return dic[self.board[y][x][0]]


# run
game = Game()
