#!/usr/bin/env python

import math
import sys
import time

from Tkinter import *

class Karel(object):

    x = 0
    y = 0
    otoc = 0

    def __init__(self):

        self.root = Tk()
        self.root.wm_title("KAREL")

        self.frame = Frame(self.root)
        self.frame.pack(side=LEFT)

        self._prompt = StringVar()
        self._prompt.set("ZADEJ PRIKAZ (krok, vlevo, poloz, zvedni, prace, konec, ...) A STISNKNI ENTER")
        self.prompt = Label(self.frame, textvariable=self._prompt)
        self.prompt.pack()

        self._prikaz = StringVar()
        self.prikaz = Entry(self.frame, textvariable=self._prikaz)
        self.prikaz.pack()
        self.prikaz.focus()

        self.canvas = Canvas(self.frame, width=600, height=600)
        self.canvas.pack(fill=BOTH, expand=1)

        self.canvas.create_rectangle(10, 100, 90, 30, fill="white", tags=("karel"))
        self.canvas.create_rectangle(25, 30, 75, 1, fill="white", tags=("karel"))
        self.canvas.create_oval(40, 15, 45, 10, fill="black", tags=("karel"))
        self.canvas.create_oval(60, 15, 65, 10, fill="black", tags=("karel"))
        self.sipka = [(40, 70), (60, 60), (40, 50)]
        self.canvas.create_polygon(self.sipka, fill="black", tags=("karel", "sipka"))

        self.text = Text(self.root, width=32)
        self.text.pack(side=LEFT, fill=Y, expand=1)
        self.load_txt()

        self.prikaz.bind("<Return>", self.on_prikaz_return)

        self.root.mainloop()

    def on_prikaz_return(self, event):
        prikaz = self._prikaz.get().strip().lower()
        self.vykonej(prikaz)

    def vykonej(self, prikaz):
        if prikaz == "krok":
            self.krok()
        elif prikaz == "vlevo":
            self.vlevo()
        elif prikaz == "prace":
            self.prace()
        elif prikaz == "poloz":
            self.poloz()
        elif prikaz == "zvedni":
            self.zvedni()
        elif prikaz == "konec":
            self.konec()
        else:
            programy = self.nacti_programy()
            if prikaz in programy.keys():
                self.vykonej_program(programy[prikaz], 0)
            else:
                self._prompt.set("NEZNAMY PRIKAZ!")

    def krok(self):
        uhel = float(self.otoc)/360.*2.*math.pi
        dx = 100.*math.cos(uhel)
        dy = -100.*math.sin(uhel)
        self.x += dx
        self.y += dy
        eps = 1.e-8
        if self.x >= -eps and self.x < self.canvas.winfo_width()-100 and self.y > -eps and self.y < self.canvas.winfo_height()-100:
            self.canvas.move("karel", dx, dy)
            self._prompt.set("UDELAL JSEM KROK")
        else:
            self.x -= dx
            self.y -= dy
            self._prompt.set("JE TAM ZED!")
        
    def vlevo(self):
        self.otoc = self.otoc + 90
        if self.otoc > 360:
            self.otoc = self.otoc - 360
        uhel = float(self.otoc)/360.*2.*math.pi
        self.canvas.delete("sipka")
        sipka = []
        x0 = 50
        y0 = 60
        for x, y in self.sipka:
            x2 = x0 + self.x + (x-x0)*math.cos(uhel) + (y-y0)*math.sin(uhel)
            y2 = y0 + self.y - (x-x0)*math.sin(uhel) + (y-y0)*math.cos(uhel)
            sipka.append(x2)
            sipka.append(y2)
        self.canvas.create_polygon(sipka, fill="black", tags=("karel", "sipka"))
        self._prompt.set("OTOCIL JSEM SE VLEVO")

    def poloz(self):
        self.canvas.create_oval(self.x+5, self.y+10, self.x+15, self.y, fill="blue", outline="cyan", width=1, tags=("znacka"))
        self._prompt.set("POLOZIL JSEM ZNACKU")

    def zvedni(self):
        item = self.canvas.find_closest(self.x+10, self.y+5)[0]
        tag = self.canvas.gettags(item)[0]
        if tag == "znacka":
            self.canvas.delete(item)
            self._prompt.set("ZVEDNUL JSEM ZNACKU")
        else:
            self._prompt.set("NENI TU ZNACKA!")

    def load_txt(self):
        f = open("karel.txt", "r")
        txt = f.read()
        f.close()
        self.text.delete(0.0, 8192.0)
        self.text.insert(0.0, txt)

    def save_txt(self):
        txt = self.text.get(0.0, 8192.0).strip()
        f = open("karel.txt", "w")
        f.write(txt)

    def nacti_programy(self):
        txt = self.text.get(0.0, 8192.0).strip()
        programy = {}
        nazev = ""
        for line in txt.split("\n"):
            if len(line) > 0:
                l = line.split()
                if l[0] == "prog":
                    nazev = l[1]
                    programy[nazev] = ""
                elif len(nazev) > 0:
                    programy[nazev] += l[0] + "\n"
        return programy

    def vykonej_program(self, program, i):
        prikazy = program.split()
        if (i < len(prikazy)):
            print i, prikazy[i], program.replace("\n", "\\n")
            self.vykonej(prikazy[i])
            i += 1
            self.root.after(300, self.vykonej_program, program, i)
            self._prompt.set("TVRDE PRACUJI")
        else:
            self._prompt.set("SKONCIL JSEM PRACI, BYLA TO FUSKA")

    def prace(self):
        program = """
krok
krok
krok
krok
krok
vlevo
vlevo
krok
krok
krok
krok
krok
vlevo
vlevo
krok
krok
krok
krok
krok
vlevo
vlevo
krok
krok
krok
krok
krok
vlevo
vlevo
"""
        self.vykonej_program(program, 0)

    def konec(self):
        self.save_txt()
        self.root.destroy()

def main():
    karel = Karel()

if __name__ == "__main__":
    main()


