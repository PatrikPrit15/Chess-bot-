
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
