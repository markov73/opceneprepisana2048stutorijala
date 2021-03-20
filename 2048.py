import tkinter as tk
import bojice
import random

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(self, bg=bojice.GRID_COLOR, bd=3, width=600, height=700)
        self.main_grid.grid(pady=(200,0))
        self.sucelje()
        self.kreni()
        self.master.bind("<Left>", self.leva)
        self.master.bind("<Right>", self.desna)
        self.master.bind("<Up>", self.gore)
        self.master.bind("<Down>", self.dole)
        self.mainloop()

    def sucelje(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg=bojice.EMPTY_CELL_COLOR, width=150, height=150)
                cell_frame.grid(row=i, column=j, padx=3, pady=3)
                cell_number = tk.Label(self.main_grid, bg=bojice.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        f = open("skor.txt", "r")
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=75, anchor="center")
        tren = f.readline()
        print (tren)
        skor = "Zadnji haj skor: "+tren+"\nReza"
        tk.Label(score_frame, text=skor, font=bojice.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=bojice.SCORE_FONT)
        self.score_label.grid(row=1)


        f.close()

    def kreni(self):
        self.matrix = [[0]*4 for _ in range(4)]
        row = random.randint(0,3)
        col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=bojice.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=bojice.CELL_COLORS[2], fg=bojice.CELL_NUMBER_COLORS[2], font=bojice.CELL_NUMBER_FONTS[2], text="2")
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=bojice.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=bojice.CELL_COLORS[2], fg=bojice.CELL_NUMBER_COLORS[2], font=bojice.CELL_NUMBER_FONTS[2], text="2")

        self.score = 0

    def stack(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position +=1
        self.matrix = new_matrix


    def spoji(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *=2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]
                    f = open("skor.txt", "r")
                    tren = f.read()
                    print (len(tren))
                    f.close()
                    haj = 0;
                    for i in range(len(tren)):
                        haj+=int(tren[i])*pow(10,i)
                    if  haj < self.score:
                        f = open("skor.txt", "w")
                        f.write(str(self.score))
                        f.close()

    def preokreni(self):
         new_matrix = []
         for i in range(4):
             new_matrix.append([])
             for j in range(4):
                 new_matrix[i].append(self.matrix[i][3-j])
         self.matrix = new_matrix

    def dijagonala(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j]= self.matrix[j][i]
        self.matrix = new_matrix

    def nova(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = random.randint(1,2)*2


    def updejtaj(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=bojice.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=bojice.EMPTY_CELL_COLOR, text=" ")
                else:
                    self.cells[i][j]["frame"].configure(bg=bojice.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=bojice.CELL_COLORS[cell_value], fg=bojice.CELL_NUMBER_COLORS[cell_value], font=bojice.CELL_NUMBER_FONTS[cell_value], text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()


    def leva(self, event):
        self.stack()
        self.spoji()
        self.stack()
        self.nova()
        self.updejtaj()
        self.game_over()

    def desna(self, event):
        self.preokreni()
        self.stack()
        self.spoji()
        self.stack()
        self.preokreni()
        self.nova()
        self.updejtaj()
        self.game_over()

    def gore(self, event):
        self.dijagonala()
        self.stack()
        self.spoji()
        self.stack()
        self.dijagonala()
        self.nova()
        self.updejtaj()
        self.game_over()

    def dole(self, event):
        self.dijagonala()
        self.preokreni()
        self.stack()
        self.spoji()
        self.stack()
        self.preokreni()
        self.dijagonala()
        self.nova()
        self.updejtaj()
        self.game_over()

    def provjera_hor(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    def provjera_ver(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="JU VIN", bg=bojice.WINNER_BG, fg=bojice.GAME_OVER_FONT_COLOR, font=bojice.GAME_OVER_FONT).pack()


        elif not any(0 in row for row in self.matrix) and not self.provjera_hor() and not self.provjera_ver():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="GEJM OVER", bg=bojice.LOSER_BG, fg=bojice.GAME_OVER_FONT_COLOR, font=bojice.GAME_OVER_FONT).pack()


def main():
    Game()

if __name__ == "__main__":
    main()

#
#
#
#
#
#
#
#
#
