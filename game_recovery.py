import os
from tkinter import *
from tkinter import messagebox
import random
import time
import sqlite3_connect_db
import menu


def setup(grid_height, grid_width, mines_num, square_size=50, mines=set(), clear=set(), marked=set(), marked_grid=set()):
    def grid(c, grid_height, grid_width, square_size):
        for i in range(grid_width):
            for j in range(grid_height):
                c.create_rectangle(i * square_size, j * square_size,
                                   i * square_size + square_size,
                                   j * square_size + square_size, fill='gray')

        for item in range(grid_width*grid_height + 1):
            if item in marked:
                c.itemconfig(item, fill='orange')
            if item in clear:
                c.itemconfig(item, fill='green')
            if item in marked_grid:
                c.itemconfig(item, fill='yellow')
        for item in clear:
            print_neighbors(item)

    def close_window():

        def save():
            print('[ Log ]: starting saving process...')
            game_time = time.time() - start_time
            game_time += pre_gametime
            save_file = open("save_"+username+".txt", "w")
            save_file.write(str(username) + '\n'
                            + str(level) + '\n'
                            + str(mines) + '\n'
                            + str(clear) + '\n'
                            + str(marked) + '\n'
                            + str(marked_grid) + '\n'
                            + str(game_time))
            save_file.close()
            print('[ Log ]: save file '+str(save_file.name)+' created successfully!')
            save_window.destroy()

        def exit():
            save_window.destroy()

        root.destroy()
        save_window = Tk()
        save_window.title("Minesweep Game")

        l1 = Label(save_window, text='Do you want to save this game ?',
                   font="Arial 16")
        l1.pack()

        b1 = Button(save_window, text='Save',
                    width=15, height=3)
        b1.config(command=save)
        b1.pack()

        b2 = Button(save_window, text='Exit',
                    width=15, height=3)
        b2.config(command=exit)
        b2.pack()

    clicked = set()

    start_time = time.time()
    root = Tk()  # Основное окно программы
    root.protocol("WM_DELETE_WINDOW", close_window)
    root.title("Minesweep Game")
    c = Canvas(root, width=grid_width * square_size,
               height=grid_height * square_size)  # Задаем область на которой будем рисовать
    c.pack()

    GRID_SIZE = grid_height

    def check_mines(neighbors):
        return len(mines.intersection(neighbors))

    def generate_neighbors(square):
        """ Возвращает клетки соседствующие с square """
        # Левая верхняя клетка
        if square == 1:
            data = {grid_height + 1, 2, grid_height + 2}
            # print('left top')
        # Правая нижняя
        elif square == (grid_height * grid_width):
            data = {square - GRID_SIZE, square - 1, square - GRID_SIZE - 1}
            # print('right bottom')
        # Левая нижняя
        elif square == grid_height:
            data = {grid_height - 1, grid_height * 2, grid_height * 2 - 1}
            # print('left bottom')
        # Верхняя правая
        elif square == (grid_height * grid_width) - grid_height + 1:
            data = {square + 1, square - grid_height, square - grid_height + 1}
            # print('right top')
        # Клетка в левом ряду
        elif square < grid_height:
            data = {square + 1, square - 1, square + GRID_SIZE,
                    square + GRID_SIZE - 1, square + GRID_SIZE + 1}
            # print('left row')
        # Клетка в правом ряду
        elif square > (grid_height * grid_width) - grid_height:
            data = {square + 1, square - 1, square - GRID_SIZE,
                    square - GRID_SIZE - 1, square - GRID_SIZE + 1}
            # print('right row')
        # Клетка в нижнем ряду
        elif square % grid_height == 0:
            data = {square + GRID_SIZE, square - GRID_SIZE, square - 1,
                    square + GRID_SIZE - 1, square - GRID_SIZE - 1}
            # print('bottom row')
        # Клетка в верхнем ряду
        elif square % grid_height == 1:
            data = {square + GRID_SIZE, square - GRID_SIZE, square + 1,
                    square + GRID_SIZE + 1, square - GRID_SIZE + 1}
            # print('top row')
        # Любая другая клетка
        else:
            data = {square - 1, square + 1, square - GRID_SIZE, square + GRID_SIZE,
                    square - GRID_SIZE - 1, square - GRID_SIZE + 1,
                    square + GRID_SIZE + 1, square + GRID_SIZE - 1}
            # print('another')
        return data

    def print_neighbors(ids):
        ids_neigh = generate_neighbors(ids)  # Получаем все соседние клетки
        around = check_mines(ids_neigh)  # высчитываем количество мин вокруг нажатой клетки
        c.itemconfig(ids, fill="green")  # окрашиваем клетку в зеленый

        # Если вокруг мин нету
        if around == 0:
            # Создаем список соседних клеток
            neigh_list = list(ids_neigh)
            # Пока в списке соседей есть клетки
            while len(neigh_list) > 0:
                # Получаем клетку
                item = neigh_list.pop()
                # Окрашиваем ее в зеленый цвет
                c.itemconfig(item, fill="green")
                # Получаем соседение клетки данной клетки
                item_neigh = generate_neighbors(item)
                # Получаем количество мин в соседних клетках
                item_around = check_mines(item_neigh)
                # Если в соседних клетках есть мины
                if item_around > 0:
                    # Делаем эту проверку, чтобы писать по нескольку раз на той же клетке
                    if item not in clicked:
                        # Получаем координаты этой клетки
                        x1, y1, x2, y2 = c.coords(item)
                        # Пишем на клетке количество мин вокруг
                        c.create_text(x1 + square_size / 2,
                                      y1 + square_size / 2,
                                      text=str(item_around),
                                      font="Arial {}".format(int(square_size / 2)),
                                      fill='yellow')
                # Если в соседних клетках мин нету
                else:
                    # Добавляем соседние клетки данной клетки в общий список
                    neigh_list.extend(set(item_neigh).difference(clicked))
                    # Убираем повторяющиеся элементы из общего списка
                    neigh_list = list(set(neigh_list))
                # Добавляем клетку в нажатые
                clicked.add(item)
                clear.add(item)
        # Если мины вокруг есть
        else:
            # Высчитываем координаты клетки
            x1, y1, x2, y2 = c.coords(ids)
            # Пишем количество мин вокруг
            c.create_text(x1 + square_size / 2,
                          y1 + square_size / 2,
                          text=str(around),
                          font="Arial {}".format(int(square_size / 2)),
                          fill='yellow')

    def gameover():
        messagebox.showwarning(title='Oops!', message='Game Over !')
        # save_results()
        root.destroy()
        os.remove("save_"+str(username)+".txt")
        menu.display()

    def save_results():
        game_time = time.time() - start_time
        game_time += pre_gametime
        print('Game time: ' + str(game_time))
        sqlite3_connect_db.cursor.execute("INSERT INTO results VALUES (?, ?, ?)", (username, level, str(round(game_time))))
        sqlite3_connect_db.conn.commit()

    def check_win():
        if (grid_width * grid_height) - len(mines) == len(clear) and len(marked) == len(mines):
            for mark in marked:
                if mark not in mines:
                    return False
            os.remove("save_" + str(username) + ".txt")
            save_results()
            return True

    # events
    def click(event):
        ids = c.find_withtag(CURRENT)[0]  # Определяем по какой клетке кликнули
        if ids not in marked:
            if ids in mines and len(clear) == 0:
                print('[ Log ]: first click on mine detected !')
                mines.remove(ids)
                print('[ Log ]: mine id = ' + str(ids) + ' removed from mines list')
                print('[ Log ]: generating new mine...')
                while True:
                    new_mine = random.randint(1, grid_height * grid_width + 1)
                    print('[ Log ]: mine id = ' + str(new_mine) + ' generated, checking...')
                    if new_mine in mines:
                        continue
                    else:
                        mines.add(new_mine)
                        print('[ Log ]: new mine id = ' + str(new_mine) + ' has been added to mines list !')
                        break
            if ids not in mines:
                print_neighbors(ids)
                x1, y1, x2, y2 = c.coords(ids)
                clear.add(ids)
                if check_win():
                    messagebox.showwarning(title='Congratulations !', message='You won this game !')
                    root.destroy()
                    return 0

            if ids in mines:
                if ids in marked:
                    pass
                else:
                    c.itemconfig(CURRENT, fill="red")  # Если кликнули по клетке с миной - красим ее в красный цвет
                    gameover()
                    return 0

            elif ids not in clicked:
                c.itemconfig(CURRENT, fill="green")  # Иначе красим в зеленый
            c.update()

    def mark_grid(event):
        ids = c.find_withtag(CURRENT)[0]
        # Если мы не кликали по клетке - красим ее в желтый цвет, иначе - в серый
        if ids not in clicked:
            clicked.add(ids)
            x1, y1, x2, y2 = c.coords(ids)
            c.itemconfig(CURRENT, fill='yellow')
            marked_grid.add(ids)
        else:
            clicked.remove(ids)
            marked_grid.remove(ids)
            c.itemconfig(CURRENT, fill="gray")

    # Функция для обозначения мин
    def mark_mine(event):
        ids = c.find_withtag(CURRENT)[0]
        # Если мы не кликали по клетке - красим ее в желтый цвет, иначе - в серый
        if ids not in clicked:
            clicked.add(ids)
            marked.add(ids)
            l2.config(text='Marked: ' + str(len(marked)))
            c.itemconfig(CURRENT, fill="orange")
            x1, y1, x2, y2 = c.coords(ids)
            if check_win():
                messagebox.showwarning(title='Congratulations !', message='You won this game !')
                root.destroy()
        else:
            clicked.remove(ids)
            marked.remove(ids)
            l2.config(text='Marked: ' + str(len(marked)))
            c.itemconfig(CURRENT, fill="gray")

    c.bind("<Button-1>", click)
    c.bind("<Button-3>", mark_mine)
    c.bind("<MouseWheel>", mark_grid)

    grid(c, grid_height, grid_width, square_size)

    print(mines)

    l1 = Label(root, text="Mines: " + str(len(mines)),
               font="Arial 16")
    l1.pack()

    l2 = Label(root, text="Marked: " + str(len(marked)),
               font="Arial 16")
    l2.pack()

    root.mainloop()


if __name__ == '__main__':
    setup(9, 9, 18)
else:
    start_time = 0
    username = ''
    level = ''
    pre_gametime = 0