import tkinter as tk



main = tk.Tk()
canvas = tk.Canvas(width=1920, height=1080)
canvas.pack()
import time



# nic-0, pesiakb-1, konb-2, strelecb-3, vezab-4, kralovnab-5, kralb-6,pesiakc-7, konc-8, strelecc-9, vezac-10, kralovnac-11, kralc-12
pole = [
        [[10,0],[8,0],[9,0],[11,0],[12,0],[9,0],[8,0],[10,0]],
                [[7,0] for _ in range(8)],
                        [[0,0] for _ in range(8)],
                                [[0,0] for _ in range(8)],
                                        [[0,0] for _ in range(8)],
                                                [[0,0] for _ in range(8)],
                                                        [[1,0] for _ in range(8)],
                                                                [[4,0],[2,0],[3,0],[5,0],[6,0],[3,0],[2,0],[4,0]]
                                                                ]




                                                                sur=[-1,-1]
                                                                empasant=[-1,-1]
                                                                rbl,rbp,rcl,rcp=0,0,0,0