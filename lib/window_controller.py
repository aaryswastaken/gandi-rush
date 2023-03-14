from tkinter import *
from PIL import Image, ImageTk
class Window_Controller(Tk):
    def __init__(self):
        super().__init__()
        self["bg"]="#73c2fa"
        self.geometry("1200x800")
        self.resizable(width=False, height=False)

class MenuPrincipal(Window_Controller):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        # Logo
        self.originalLogo = Image.open('../sprite/Logo.png').convert('RGB')
        self.imageLogo = ImageTk.PhotoImage(self.originalLogo.resize((400, 300), Image.NEAREST))
        self.Logo = Canvas(self, height=300, width=400, borderwidth=0, highlightthickness=0)
        self.Logo.create_image(0, 0, image=self.imageLogo, anchor='nw')
        # BoutonJouer
        self.originalBouton1 = Image.open("../sprite/Bouton1.png")
        self.originalBouton2 = Image.open("../sprite/Bouton2.png")
        self.imageBouton1 = ImageTk.PhotoImage(self.originalBouton1.resize((400, 200), Image.NEAREST))
        self.imageBouton2 = ImageTk.PhotoImage(self.originalBouton2.resize((400, 200), Image.NEAREST))
        self.Bouton = Canvas(self, height=200, width=400, borderwidth=0, highlightthickness=0)
        self.Bouton.create_image(0, 0, image=self.imageBouton1, anchor="nw", tag="IMG")
        self.Bouton.bind("<Enter>", self.EnterBouton)
        self.Bouton.bind("<Leave>", self.LeaveBouton)
        self.Bouton.bind("<Button-1>", self.LeaveMenu)
        self.Bouton.focus_set()
        self.Logo.grid(row=0, column=0, sticky="n")
        self.Bouton.grid(row=1, column=0, sticky="")
    def EnterBouton(self,f):
        self.Bouton.delete("IMG")
        self.Bouton.create_image(0, 0, image=self.imageBouton2,anchor="nw",tag="IMG")
    def LeaveBouton(self,f):
        self.Bouton.delete("IMG")
        self.Bouton.create_image(0, 0, image=self.imageBouton1, anchor="nw", tag="IMG")
    def LeaveMenu(self,f):
        self.Bouton.destroy()
        self.Logo.destroy()
    def BoutonJouerClick(self,f):
        self.LeaveMenu(None)



fenetre=MenuPrincipal()
fenetre.mainloop()