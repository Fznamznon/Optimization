import tkinter.ttk
from tkinter.messagebox import *
from tkinter.simpledialog import *
from math import *

H = 0
W = 0
MX = 0
MY = 0
L = 0
R = 0
T = 0
B = 0
LL = 0

STEP = 0.001


def clear():
    canvas.delete('all')


def redraw_callback(event):
    global H, W
    H = event.height
    W = event.width


def draw_point(x, y, color='black', size=1):
    px = (x - LL) * MX
    py = (T - y) * MY
    canvas.create_oval(px, py, px + size, py + size, fill=color)


def draw_points(points, color='black', size=1):
    for x, y in points:
        draw_point(x, y, color, size)


def draw_line(x1, y1, x2, y2, color='black', width=1):
    px1 = (x1 - LL) * MX
    px2 = (x2 - LL) * MX
    py1 = (T - y1) * MY
    py2 = (T - y2) * MY
    canvas.create_line(px1, py1, px2, py2, fill=color, width=width)


def draw_serif(x, height=0.4, color='black', width=2):
    draw_line(x, -height / 2, x, height / 2, color=color, width=width)


def draw_axis():
    if B <= 0 <= T:
        canvas.create_line(0, T * MY, W, T * MY, arrow='last', width=2)
    if L <= 0 <= R:
        canvas.create_line((0 - LL) * MX, H, (0 - LL) * MX, 0, arrow="last", width=2)


def prepare_drawing(func, left, right):
    global H, W, MX, MY, L, R, T, B, LL
    L = left
    LL = left - 0.5
    R = right
    MX = W / (right - left + 1)

    x = left - 0.5
    points = []
    iteration = 0
    min_y = max_y = 0
    while x <= right + 0.5:
        if x < 0:
            f = func.replace('x', '(' + str(x) + ')')
        else:
            f = func.replace('x', str(x))
        y = eval(f)
        points.append((x, y))
        if iteration == 0 or y < min_y:
            min_y = y
        if iteration == 0 or y > max_y:
            max_y = y
        iteration += 1
        x += STEP

    T = max_y + 1
    B = min_y - 1
    if B > 0:
        B = -1
    MY = H / (T - B)

    return points


def get_L(X, r):
    max_l = 0
    for i in range(len(X)):
        for j in range(len(X)):
            if i == j:
                continue
            else:
                lk = abs(X[j][1] - X[i][1]) / abs(X[j][0] - X[i][0])
                if lk > max_l:
                    max_l = lk
    if max_l == 0:
        return 1
    else:
        return r * max_l


def get_Rt(X, L):
    min_r = 0
    min_index = -1
    for i in range(len(X) - 1):
        R = (X[i][1] + X[i + 1][1]) / 2 - L * (X[i + 1][0] - X[i][0]) / 2
        if min_index == -1:
            min_r = R
            min_index = i
        else:
            if R < min_r:
                min_r = R
                min_index = i
    return (min_index, min_r)


def get_new_x(X, L, t):
    return (X[t][0] + X[t + 1][0]) / 2 - (X[t + 1][1] - X[t][1]) / (2 * L)

def get_strongin_Rt(X, L):
    min_r = 0
    min_index = -1
    for i in range(len(X) - 1):
        dx = X[i + 1][0] - X[i][0]
        dq = X[i + 1][1] - X[i][1]
        R = (X[i][1] + X[i + 1][1]) / 2 - L * (X[i + 1][0] - X[i][0]) / 2 * (1 + pow((dq/dx * 1/L),2)) / 2
        if min_index == -1:
            min_r = R
            min_index = i
        else:
            if R < min_r:
                min_r = R
                min_index = i
    return (min_index, min_r)


def brute_method():
    n = askinteger("Введите число измерений", '')
    x = L
    f = functionBox.get().strip().replace("x", str(x))
    y = eval(f)
    min_y = y
    return_x = L
    step = (R - L) / (n + 1)
    draw_serif(L, color='green')
    while x <= R:
        x += step
        if x > R:
            break
        draw_serif(x, color='green')
        if x < 0:
            f = functionBox.get().strip().replace('x', '(' + str(x) + ')')
        else:
            f = functionBox.get().strip().replace('x', str(x))
        y = eval(f)
        if y < min_y:
            min_y = y
            return_x = x
    draw_serif(return_x, height=0.6, color='red', width=3)
    showinfo('Результат работы метода',
                                "Выполнено " + str(n) + " итераций. Ответ: x = " + str(return_x) + ", y = " + str(
                                    min_y))
    return return_x


def piyavskii_method(left, right):
    E = askfloat("Введите точность", '')
    r = askfloat("Введите параметр надежности", '')
    X = []
    if left < 0:
        f = functionBox.get().strip().replace('x', '(' + str(left) + ')')
    else:
        f = functionBox.get().strip().replace('x', str(left))
    X.append((left, eval(f)))

    if right < 0:
        f = functionBox.get().strip().replace('x', '(' + str(right) + ')')
    else:
        f = functionBox.get().strip().replace('x', str(right))
    X.append((right, eval(f)))

    if X[0][1] > X[1][1]:
        min_q = X[1][1]
        min_x = X[1][0]
    else:
        min_q = X[0][1]
        min_x = X[0][0]
    draw_serif(min_x, color='green')
    k = 1
    L = get_L(X, r)
    t, Rt = get_Rt(X, L)
    while abs(min_q - Rt) > E:
        new_x = get_new_x(X, L, t)
        if new_x < 0:
            f = functionBox.get().strip().replace('x', '(' + str(new_x) + ')')
        else:
            f = functionBox.get().strip().replace('x', str(new_x))
        new_q = eval(f)
        X.append((new_x, new_q))
        if min_q > new_q:
            min_q = new_q
            min_x = new_x
        draw_serif(new_x, color='green')
        k += 1
        X.sort()
        L = get_L(X, r)
        t, Rt = get_Rt(X, L)

    draw_serif(min_x, color='red', height=0.6, width=3)

    showinfo('Результат работы метода',
                                "Выполнено " + str(k) + " итераций. Ответ: x = " + str(min_x) + ", y = " + str(min_q))
    return min_q

def strongin_method(left, right):
    E = askfloat("Введите точность", '')
    r = askfloat("Введите параметр надежности", '')
    X = []
    if left < 0:
        f = functionBox.get().strip().replace('x', '(' + str(left) + ')')
    else:
        f = functionBox.get().strip().replace('x', str(left))
    X.append((left, eval(f)))

    if right < 0:
        f = functionBox.get().strip().replace('x', '(' + str(right) + ')')
    else:
        f = functionBox.get().strip().replace('x', str(right))
    X.append((right, eval(f)))

    if X[0][1] > X[1][1]:
        min_q = X[1][1]
        min_x = X[1][0]
    else:
        min_q = X[0][1]
        min_x = X[0][0]
    draw_serif(min_x, color='green')
    k = 1
    L = get_L(X, r)
    t, Rt = get_strongin_Rt(X, L)
    while abs(X[t][0] - X[t + 1][0]) > E:
        new_x = get_new_x(X, L, t)
        if new_x < 0:
            f = functionBox.get().strip().replace('x', '(' + str(new_x) + ')')
        else:
            f = functionBox.get().strip().replace('x', str(new_x))
        new_q = eval(f)
        X.append((new_x, new_q))
        if min_q > new_q:
            min_q = new_q
            min_x = new_x
        draw_serif(new_x, color='green')
        k += 1
        X.sort()
        L = get_L(X, r)
        t, Rt = get_strongin_Rt(X, L)

    draw_serif(min_x, color='red', height=0.6, width=3)

    showinfo('Результат работы метода',
             "Выполнено " + str(k) + " итераций. Ответ: x = " + str(min_x) + ", y = " + str(min_q))
    return min_q

def methodButton_click(event):
    if listBox.curselection()[0] == 0:
        brute_method()
    if listBox.curselection()[0] == 1:
        piyavskii_method(L, R)
    if listBox.curselection()[0] == 2:
        strongin_method(L, R)



def drawButton_click(event):
    clear()
    if not leftBox.get().strip():
        showerror(title="Error!", message="Вы не ввели левую границу отрезка!")
    else:
        left = float(leftBox.get().strip())

        if not rightBox.get().strip():
            showerror(title="Error!", message="Вы не ввели правую границу отрезка!")
        else:
            right = float(rightBox.get().strip())
            if not functionBox.get().strip():
                showerror(title="Error!", message="Вы не ввели функцию!")
            else:
                points = prepare_drawing(functionBox.get().strip(), left, right)
                draw_axis()
                draw_points(points, color='blue')


root = tkinter.Tk()
root.title("Optimization")
root.geometry("800x600")
root.configure(background='#dcdad5')

canvas = tkinter.Canvas()
canvas.configure(bg="white")
canvas.grid(sticky="nsew", row=0, column=0, rowspan=2, columnspan=4)

listBox = tkinter.Listbox(selectmode="single")
listBox.insert(0, "Равномерный поиск")
listBox.insert(1, "Метод Пиявского")
listBox.insert(2, "Метод Стронгина")
listBox.grid(row=0, column=4)

methodButton = tkinter.ttk.Button(text="Запустить метод")
methodButton.grid(row=1, column=4)

label1 = tkinter.ttk.Label(text="f(x)=")
label1.grid(row=2, column=0)

label2 = tkinter.ttk.Label(text="Xmin")
label2.grid(row=3, column=0)

label3 = tkinter.ttk.Label(text="Xmax")
label3.grid(row=3, column=2)

functionBox = tkinter.ttk.Entry()
functionBox.grid(row=2, column=1, columnspan=3, sticky="ew")

leftBox = tkinter.ttk.Entry()
leftBox.grid(row=3, column=1, sticky="ew")
leftBox.insert(0, '-5')

rightBox = tkinter.ttk.Entry()
rightBox.grid(row=3, column=3, sticky="ew")
rightBox.insert(0, '5')

drawButton = tkinter.ttk.Button(text="Draw")
drawButton.grid(row=2, column=4, rowspan=2, sticky="nsew", padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=5)
root.columnconfigure(4, weight=1)
root.rowconfigure(0, weight=10)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

canvas.bind('<Configure>', redraw_callback)
drawButton.bind('<ButtonPress>', drawButton_click)
methodButton.bind('<ButtonPress>', methodButton_click)

style = tkinter.ttk.Style()
style.theme_use(themename='clam')

style.configure('TButton', background='#eee')

listBox.selection_set(0)
functionBox.focus_set()

root.mainloop()
