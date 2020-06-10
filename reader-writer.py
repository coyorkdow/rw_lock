import tkinter as tk
from tkinter import ttk


def getButton(root, text, bg, font, command, backcolor='#EFF7FD', relief="groove", width=15):
    canvas = tk.Canvas(root, relief="groove", bg=backcolor, highlightthickness=0)
    canvas.config(width=width * 10 + 3, height=35 + 3)

    def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True, outline="black")

    btn = round_rectangle(3, 3, width * 10 + 2, 35 + 2, radius=23, fill=bg, width=2)

    def left1(e):
        canvas.itemconfig(btn, fill='#F0F0F0', outline='white')
        command()

    def left2(e):
        canvas.itemconfig(btn, fill=bg, outline='black')

    canvas.bind('<ButtonPress>', left1)
    canvas.bind('<ButtonRelease>', left2)

    canvas.create_text((width * 10 + 2) / 2, (35 + 2) / 2, text=text, font=font)
    return canvas


def reader(num):
    # 执行操作
    pass


def writer():
    # 执行操作
    pass


# 界面的信息显示和操作
def show_main():
    total = tk.Tk()
    total.title("读者-写者问题模拟")
    total.resizable(0, 0)  # 宽可变, 高可变

    L_Frame = ttk.Notebook(total, width=240)

    L_Frame.pack(side=tk.LEFT, fill="y", ipadx=50)

    R_Frame = ttk.Notebook(total)
    Info_Frame = ttk.Notebook(total)
    # #####################
    # # tab01 = tk.Frame(Info_Frame, bg="#EFF7FD")  # Create a tab
    # # Info_Frame.add(tab01, text='个人信息')
    # # tk.Label(tab01, pady=40, text="", font=("楷体", 23), bg="#EFF7FD", ).pack()  # 自动调整布局
    # # root2 = tk.Label(tab01, width=80, bg="#EFF7FD")  # 个性头像
    # # root2.pack(fill=tk.X, padx=0, ipady=10)
    #
    # # R_Frame.pack(expand=1, fill="both")  # Pack to make visible
    # ###########################Left#################
    tab00 = tk.Frame(L_Frame, bg="#EFF7FD")  # Create a tab
    tab01 = tk.Frame(L_Frame, bg="#EFF7FD")  # Create a tab
    L_Frame.add(tab00, text='模拟方式1', )
    L_Frame.add(tab01, text='模拟方式2', )

    root = tk.LabelFrame(tab00, width=240, bg="#EFF7FD")

    root.pack(anchor=tk.S, fill=tk.BOTH, padx=0, ipady=0)

    tk.Label(root, text='读者数量:', font=("楷体", 15), bg="#EFF7FD").grid(row=0, column=0, pady=40)  # 对Label内容进行 表格式 布局
    tk.Label(root, text='写者数量:', font=("楷体", 15), bg="#EFF7FD").grid(row=1, column=0, pady=40)
    tk.Label(root, text='资源数量:', font=("楷体", 15), bg="#EFF7FD").grid(row=2, column=0, pady=40)
    ######zxh
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    e1 = tk.Entry(root, textvariable=v1, bg="#EFF7FD").grid(row=0, column=1, padx=5, pady=20)  # 用于储存 输入的内容
    e2 = tk.Entry(root, textvariable=v2, bg="#EFF7FD").grid(row=1, column=1, padx=5, pady=30)
    e3 = tk.Entry(root, textvariable=v3, bg="#EFF7FD").grid(row=2, column=1, padx=5, pady=20)  # 用于储存 输入的内容
    getButton(root, text='信息设置', relief="groove", bg="#EFF7FD", font=("楷体", 15), width=10,
              command=show_simulation1).grid(row=3,
                                             column=0,
                                             sticky=tk.W,
                                             padx=30,
                                             pady=10)
    getButton(root, text='退出', relief="groove", bg="#EFF7FD", font=("楷体", 15), width=10, command=total.quit).grid(row=3,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.E,
                                                                                                                  padx=30,
                                                                                                                  pady=10)
    total.mainloop()


def show_simulation1():
    total = tk.Tk()
    total.title("读者-写者问题模拟软件")
    total.resizable(0, 0)  # 宽可变, 高可变

    L_Frame = ttk.Notebook(total, width=240)
    L_Frame.pack(side=tk.LEFT, fill="y", ipadx=50)

    tab00 = tk.Frame(L_Frame, bg="#EFF7FD")  # Create a tab
    tab01 = tk.Frame(L_Frame, bg="#EFF7FD")  # Create a tab
    L_Frame.add(tab00, text='读者模拟', )
    L_Frame.add(tab01, text='写者模拟', )

    root = tk.LabelFrame(tab00, width=240, bg="#EFF7FD")

    root.pack(anchor=tk.S, fill=tk.BOTH, padx=0, ipady=0)

    tk.Label(root, text='读者序号:', font=("楷体", 15), bg="#EFF7FD").grid(row=0, column=0, pady=40)  # 对Label内容进行 表格式 布局
    tk.Label(root, text='资源序号:', font=("楷体", 15), bg="#EFF7FD").grid(row=1, column=0, pady=40)  # 对Label内容进行 表格式 布局
    ######zxh
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    e1 = tk.Entry(root, textvariable=v1, bg="#EFF7FD").grid(row=0, column=1, padx=5, pady=20)  # 用于储存 输入的内容
    e2 = tk.Entry(root, textvariable=v2, bg="#EFF7FD").grid(row=1, column=1, padx=5, pady=30)
    getButton(root, text='读取', relief="groove", bg="#EFF7FD", font=("楷体", 15), width=10,
              command=reader).grid(row=3,
                                   column=0,
                                   sticky=tk.W,
                                   padx=30,
                                   pady=10)
    getButton(root, text='退出', relief="groove", bg="#EFF7FD", font=("楷体", 15), width=10, command=total.quit).grid(row=3,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.E,
                                                                                                                  padx=30,
                                                                                                                  pady=10)

    root = tk.LabelFrame(tab01, width=240, bg="#EFF7FD")

    root.pack(anchor=tk.S, fill=tk.BOTH, padx=0, ipady=0)

    tk.Label(root, text='写者序号:', font=("楷体", 15), bg="#EFF7FD").grid(row=0, column=0, pady=40)  # 对Label内容进行 表格式 布局
    tk.Label(root, text='资源序号:', font=("楷体", 15), bg="#EFF7FD").grid(row=1, column=0, pady=40)  # 对Label内容进行 表格式 布局
    ######zxh
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    e3 = tk.Entry(root, textvariable=v3, bg="#EFF7FD").grid(row=0, column=1, padx=5, pady=20)  # 用于储存 输入的内容
    e4 = tk.Entry(root, textvariable=v4, bg="#EFF7FD").grid(row=1, column=1, padx=5, pady=30)
    getButton(root, text='改写', relief="groove", bg="#EFF7FD", font=("楷体", 15), width=10,
              command=writer).grid(row=3,
                                   column=0,
                                   sticky=tk.W,
                                   padx=30,
                                   pady=10)
    getButton(root, text='退出', relief="groove", bg="#EFF7FD", font=("楷体", 15), width=10, command=total.quit).grid(row=3,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.E,
                                                                                                                  padx=30,
                                                                                                                  pady=10)
    total.mainloop()


def main():
    show_main()
    pass


if __name__ == "__main__":
    main()
