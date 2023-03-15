from tkinter import *
from PIL import Image, ImageTk
from   random import *
class Window_Controller(Tk):
    def __init__(self):
        super().__init__()
        self["bg"]="#73c2fa"
        self.geometry("1200x800")
        self.resizable(width=False, height=False)


class MenuPrincipal():
    def __init__(self,root):
        self.root=root
        root.columnconfigure(0,weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        # Logo
        self.originalLogo = Image.open('../sprite/Logo.png').convert('RGB')
        self.imageLogo = ImageTk.PhotoImage(self.originalLogo.resize((400, 300), Image.NEAREST))
        self.Logo = Canvas(root, height=300, width=400, borderwidth=0, highlightthickness=0)
        self.Logo.create_image(0, 0, image=self.imageLogo, anchor='nw')
        # BoutonJouer
        self.originalBouton1 = Image.open("../sprite/Bouton1.png")
        self.originalBouton2 = Image.open("../sprite/Bouton2.png")
        self.imageBouton1 = ImageTk.PhotoImage(self.originalBouton1.resize((400, 200), Image.NEAREST))
        self.imageBouton2 = ImageTk.PhotoImage(self.originalBouton2.resize((400, 200), Image.NEAREST))
        self.Bouton = Canvas(root, height=200, width=400, borderwidth=0, highlightthickness=0)
        self.Bouton.create_image(0, 0, image=self.imageBouton1, anchor="nw", tag="IMG")
        self.Bouton.bind("<Enter>", self.EnterBouton)
        self.Bouton.bind("<Leave>", self.LeaveBouton)
        self.Bouton.bind("<Button-1>", self.BoutonJouerClick)
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
        Fenetre_de_jeu(self.root).LancerJeu()

class Fenetre_de_jeu(MenuPrincipal):

        def __init__(self,root):
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=0)
            root.rowconfigure(1, weight=0)
            root.columnconfigure(16,weight=1)
            self.root=root
            global sprite
            sprite=[]
            self.focus = (None, None)
            self.grilledebas = genere_alea(3)
            for i in ["PierreBleu","PierreJaune","PierreRouge","PierreVerte"]:
                sprite.append(ImageTk.PhotoImage(Image.open("../sprite/"+i+".png").resize((48, 48), Image.NEAREST)))
        def LancerJeu(self):


            self.grille_element=[]
            self.root.bind("<Button-3>", lambda x: self.backgroundclick())
            for i in range(len(self.grilledebas)):
                ligne_element=[]
                for j in range(len(self.grilledebas[0])):
                    tmp=Canvas( height=50, width=50, bd=0, highlightthickness=0,bg="#73c2fa")
                    #tmp.create_text(0,0,text="Bob",anchor="center")
                    tmp.create_image(0, 0, image=sprite[self.grilledebas[i][j]], anchor="nw", tag="nw")
                    tmp.grid(row=i+1,column=j+1,padx=1,pady=1)
                    tmp.bind("<Button-1>", lambda x,_i=i,_j=j: self.gemeclique(_i,_j,self.grilledebas[_i][_j]))

                    ligne_element.append(tmp)
                self.grille_element.append(ligne_element)

        def backgroundclick(self):
            print("Click background")
            if self.focus!=(None,None):
                self.offFocus()
                self.focus = (None, None)

        def gemeclique(self,i,j,v):
                if self.focus==(None,None):
                    print(f"Nouveau Focus {i} {j}")
                    self.focus = (i, j)
                    self.onFocus(i, j)
                elif (i-self.focus[0])**2+(j-self.focus[1])**2!=1:
                    print(f"Nouveau Focus {i} {j}")
                    self.offFocus()
                    self.focus=(i,j)
                    self.onFocus(i,j)
                else:
                    self.grilledebas[i][j],self.grilledebas[self.focus[0]][self.focus[1]]=self.grilledebas[self.focus[0]][self.focus[1]],self.grilledebas[i][j]
                    self.focus=(None,None)
                    self.LancerJeu()
                #print(f"je suis une gemme de type { {0:'Bleu',1:'Jaune',2:'Rouge',3:'Verte'}[v]} au coordonné {i} {j}")
        def onFocus(self,i,j):
            if j!=0 and j!=14 and i!=0 and j!=14:
                self.grille_element[i-1][j].config(bg="#FFFFFF")
                self.grille_element[i+1][j].config(bg="#FFFFFF")
                self.grille_element[i][j+1].config(bg="#FFFFFF")
                self.grille_element[i][j-1].config(bg="#FFFFFF")
        def offFocus(self):
            i=self.focus[0]
            j=self.focus[1]
            if j!=0 and j!=14 and i!=0 and j!=14:
                self.grille_element[i-1][j].config(bg="#73c2fa")
                self.grille_element[i+1][j].config(bg="#73c2fa")
                self.grille_element[i][j+1].config(bg="#73c2fa")
                self.grille_element[i][j-1].config(bg="#73c2fa")
def genere_alea(nb_max):
    return  [[randint(0,nb_max) for i in range(15)] for j in range(15)]
fenetre=Window_Controller()
menu=MenuPrincipal(fenetre)
menu.root.mainloop()