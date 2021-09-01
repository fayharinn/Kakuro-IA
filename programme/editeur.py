from tkinter import *
from tkinter.messagebox import * #Gestion des boites de dialogue
from tkinter.filedialog import *
from random import randint
import pickle


    
class PlateauEditeur(list):
    def __init__(self,plateau,solution=[]):
        list.__init__(self,plateau)
        self.solution=solution


    def interdireCase(self,x,y):
        self[x][y]=-1
    
    def autoriserCase(self,x,y):
        self[x][y]=0
        
    def autreCase(self,x,y,x1,y2):
        self[x][y]=(x1,y2)

    def getLongueur(self):
        return len(self)

    def getLargeur(self):
        return len(self[0])


class Plateau(PlateauEditeur):
    def __init__(self,plateau,solution=[]):
        PlateauEditeur.__init__(self,plateau,solution)
    

def sauvegardeobj(obj, chemin):
    file=open(chemin, 'wb')
    pickle.dump(obj,file, pickle.HIGHEST_PROTOCOL)

def chargerobj(chemin):
    entree=open(chemin, 'rb')
    res = pickle.load(entree)
    return res


class Sakura(Canvas): # animation de petales de cerisier pour le theme sakuro
    
    def __init__(self,can,root,f1="images/im1.gif",f2="images/im2.gif"):
        self.p=PhotoImage(file=f1 )
        self.p2=PhotoImage(file=f2)
        self.l=[self.p,self.p2]
        self.img=randint(0,1)
        self.can=can
        self.root=root
        self.r=randint(-5,5)
        self.x=randint(-10,500)
        self.y=randint(-500,0)
        self.petale=self.can.create_image(self.x,self.y,image=self.l[self.img],tags=["theme","petale"])
        self.creer(self.x,self.y)

    def creer(self,x=0,y=0):
        self.can.coords(self.petale,x+self.r,y+5)
        if y>600:
            y=randint(-500,0)
            x=randint(-10,500)
        self.root.after(50,lambda:self.creer(x+self.r,y+5))




class ApplicationEditeur(Tk):
    def __init__(self,plateau):
        Tk.__init__(self)
        self.plateau=plateau
        self.longueurCan=640
        self.largeurCan=480
        self.taillePlateau=IntVar()
        self.taillePlateau.set(60) # Plus la valeur est grande et plus le plateau est graphiquement gros
        self.x0,self.y0=20,20  # Position du plateau
        self.nombreaentrer="0"
        self.style="Helvetica 13 bold italic" # font des nombres écrits sur la grille
        self.title('Kakuro Editeur')
        self.specialtheme=""
        self.can= Canvas(self,width=self.longueurCan,height=self.largeurCan,bg="khaki")
        self.can.focus_set()
        self.can.pack(side=LEFT)
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())
        barre = Menu(self)
        option=Menu(barre,tearoff=0)
        edit=Menu(barre,tearoff=0)
        affichage=Menu(barre,tearoff=0)
        aide=Menu(barre,tearoff=0)
        theme=Menu(affichage,tearoff=0)
        log=Menu(aide,tearoff=0)
        self.config(menu=barre)
        aide.add_cascade(label="Version du logiciel",menu=log)
        barre.add_cascade(label="Fichier",menu=option)
        barre.add_cascade(label="Edition",menu=edit)
        barre.add_cascade(label="Affichage",menu=affichage)
        affichage.add_cascade(label="Thème",menu=theme)
        log.add_cascade(label="VERSION PaB Bêta 2")
        barre.add_cascade(label="Aide",menu=aide)
        theme.add_command(label="Special Sakuro",command=lambda : self.changertheme("Sakuro","pink"))
        theme.add_command(label="Special Halloweeno",command=lambda : self.changertheme("Halloweeno","orange"))
        theme.add_command(label="Special Wintero",command=lambda : self.changertheme("Wintero","grey"))
        theme.add_command(label="Special PaBlo",command=lambda : self.changertheme("PaBlo","orange"))
        theme.add_command(label="Classico",command=lambda : self.changertheme(background="white"))
        theme.add_command(label="Cortado",command=lambda : self.changertheme())
        theme.add_command(label="Negro",command=lambda : self.changertheme(background="black"))
        theme.add_command(label="Verdado",command=lambda : self.changertheme(background="green"))
        option.add_command(label="Modifier un plateau",command=self.chargerPlateau)
        option.add_command(label="Enregistrer le plateau",command=self.sauvegardePlateau)
        option.add_separator()
        option.add_command(label="Quitter",command=self.quitter)
        cadre=Frame(self, padx=5) # cadre des boutons
        cadre.pack(side=RIGHT)
        #4baide=Button(cadre,width=10,text="Résoudre",font=self.style)
        #baide.pack()
        bverif=Button(cadre,width=15,text="Importer solution",font=self.style,command=self.chargerSolution)
        bverif.pack()
        scalevit = Scale(cadre,length=100,variable=self.taillePlateau, from_=30, to=100,orient=HORIZONTAL,label="Taille du plateau",command=lambda x:self.redraw())
        scalevit.pack()
        cadre2=Frame(cadre,padx=5)
        cadre2.pack()
        Label(cadre2,text="Nombre de colonnes").pack()
        Button(cadre2,text="+",padx=5,command=lambda:self.changeWidth(1)).pack(side=LEFT)
        Button(cadre2,text="-",padx=5,command=lambda:self.changeWidth(-1)).pack(side=LEFT)
        cadre3=Frame(cadre,padx=5)
        cadre3.pack()
        Label(cadre3,text="Nombre de lignes").pack()
        Button(cadre3,text="+",padx=5,command=lambda:self.changeHeight(1)).pack(side=LEFT)
        Button(cadre3,text="-",padx=5,command=lambda:self.changeHeight(-1)).pack(side=LEFT)
        self.giftbox=PhotoImage(file="images/giftbox.gif")
        self.sorcer=PhotoImage(file="images/sorcer.gif")
        self.japanesechar="abcd"
        self.listeimjap=[]
        for car in self.japanesechar:
            self.listeimjap.append(PhotoImage(file="images/"+car+".gif"))
            
        self.mainloop()



    def chargerPlateau(self):
        try:
            file= askopenfilename(title="Modifier le plateau",filetypes=[('fichier dat','.dat')])
            brut=chargerobj(file)
            self.plateau=brut[0]
            self.plateau.solution=brut[2]
            self.taillePlateau.set(brut[1])
            self.redraw()
        except:pass


    def chargerSolution(self):
        try:
            file= askopenfilename(title="Ajouter une solution au plateau",filetypes=[('fichier corr','.corr')])
            brut=chargerobj(file)
            if len(self.plateau)==len(brut[0]) and len(self.plateau[0])==len(brut[0][0]):
                self.plateau.solution=brut[0]
                showinfo("Importation réussie","La grille possède maintenant une solution")
            else:
                showinfo("Importation annulée","Importation annulée : la grille de solution doit avoir la même taille que la grille normale")
        except:pass
        
    def sauvegardePlateau(self):
        file = asksaveasfilename(title="Enregistrer le plateau édité",filetypes=[('fichier dat','.dat')],initialfile="Sauvegarde.dat")
        sauvegardeobj((self.plateau,self.taillePlateau.get(),self.plateau.solution),file)
        

    
    def dessinePlateau(self,can,n,m):
        # m est la longueur du plateau
        taillePlateau=self.taillePlateau.get() 
        style=self.style
        x0,y0=self.x0,self.y0
        

            
        for i in range(n):
            for j in range(m):
                if type(self.plateau[i][j]) is int:
                    if self.plateau[i][j]==-1:   # si la case est grisée
                        if self.specialtheme=="Wintero":
                            
                            can.create_image(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),image=self.giftbox,tags=[str(i)+","+str(j)])
                        elif self.specialtheme=="Halloweeno":
                            
                            can.create_image(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),image=self.sorcer,tags=[str(i)+","+str(j)])
                        elif self.specialtheme=="Sakuro":
                            char=randint(0,len(self.japanesechar)-1) 
                            can.create_image(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),image=self.listeimjap[char],tags=[str(i)+","+str(j)])
                            
                        can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="black",stipple='gray25',tags=[str(i)+","+str(j)])
                        can.tag_bind(str(i)+","+str(j), '<Button-1>', lambda event, i=i,j=j:self.editCase(i,j))
                        can.tag_bind(str(i)+","+str(j), '<Double-Button-1>', lambda event, i=i,j=j:self.infoCase(i,j))
                    elif self.plateau[i][j]!=0: # si un nombre est déjà entré dans la case
                        can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="#DAD3D3",tags=[str(i)+","+str(j)])
                        can.create_text(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),text=str(self.plateau[i][j]),font=style,tags=[str(i)+";"+str(j)])
                        can.tag_bind(str(i)+","+str(j), '<Button-1>', lambda event, i=i,j=j:self.onClick(event,(i,j)))
                        can.tag_bind(str(i)+";"+str(j), '<Button-1>', lambda event, i=i,j=j:self.onClick(event,(i,j)))
                        can.tag_bind(str(i)+","+str(j), '<Button-3>', lambda event, i=i,j=j:self.forbideCase(i,j))
                        can.tag_bind(str(i)+";"+str(j), '<Button-3>', lambda event, i=i,j=j:self.forbideCase(i,j))
                        
                    else: # si la case est vide
                        can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="white",tags=str(i)+","+str(j))
                        can.tag_bind(str(i)+","+str(j), '<Button-1>', lambda event, i=i,j=j:self.onClick(event,(i,j)))
                        can.tag_bind(str(i)+","+str(j), '<Button-3>', lambda event, i=i,j=j:self.forbideCase(i,j))
                        can.tag_bind(str(i)+","+str(j), '<Double-Button-1>', lambda event, i=i,j=j:self.infoCase(i,j))
                else:
                    can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="grey",tags=[str(i)+","+str(j)])
                    can.create_line(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),tags=[str(i)+","+str(j)])
                    if self.plateau[i][j][0]>0:
                        can.create_text(x0 +taillePlateau*(j+0.2),y0+taillePlateau*(i+0.8),text=str(self.plateau[i][j][0]),tags=[str(i)+","+str(j)])
                    if self.plateau[i][j][1]>0:
                        can.create_text(x0 +taillePlateau*(j+0.8),y0+taillePlateau*(i+0.2),text=str(self.plateau[i][j][1]),tags=[str(i)+","+str(j)])

                    can.tag_bind(str(i)+","+str(j), '<Button-1>', lambda event, i=i,j=j:self.editCase(i,j))
                    


        
             
    def deleteAllCanvas(self): # supprime tout sauf le thème
        try:
            listeobj=self.can.find_all()
            for x in listeobj:
                if "theme" not in self.can.gettags(x):
                    self.can.delete(x)
        except:
            pass

    def redraw(self):
        self.deleteAllCanvas()
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())

    def changeWidth(self,nb):
        if nb<0:
            if self.plateau.getLargeur()>3:
                for i in range(len(self.plateau)):
                    self.plateau[i]=self.plateau[i][:-1]
        else:
            
            for i in range(len(self.plateau)):
                for j in range(nb):
                    self.plateau[i].append(0)
        self.redraw()
            

    def changeHeight(self,nb):
        if nb<0:
            if self.plateau.getLongueur()>3:
                del(self.plateau[-1])
        else:
            for i in range(nb):
                self.plateau.append([0 for i in range(len(self.plateau[0]))])
        self.redraw()


    def forbideCase(self,x,y):
        self.deleteAllCanvas()
        self.plateau.interdireCase(x,y)
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())
        
    def editCase(self,x,y):
        self.deleteAllCanvas()
        self.plateau.autoriserCase(x,y)
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())

    def infoCase(self,x,y):
        self.redraw()
        self.can.itemconfigure(str(x)+","+str(y),fill="#DAD3D3")
        try:
            self.toplevel.destroy()
        except:pass
        self.toplevel=Toplevel(self)
        t=self.toplevel
        t.wm_attributes("-topmost", 1)
        Label(t,text="Case gauche").pack()
        casehaut=Entry(t, width=3)
        casehaut.pack()
        Label(t,text="Case droite").pack()
        casebas=Entry(t, width=3)
        casebas.pack()
        Button(t,text="Confirmer",command= lambda:self.changeInfoCase(x,y,casehaut.get(),casebas.get(),t)).pack()

    def changeInfoCase(self,x,y,x1,x2,toplevel):
        try:
            x1=int(x1)
            x2=int(x2)
            self.deleteAllCanvas()
            self.plateau.autreCase(x,y,x1,x2)
            self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())
            toplevel.destroy()
        except:
            raise ValueError("veuillez entrer un nombre correct")
        
    def onClick(self,event,liste):
        self.deleteAllCanvas()
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())
        i=liste[0]
        j=liste[1]
        self.can.itemconfigure(str(i)+","+str(j),fill="#DAD3D3")
        self.nombreaentrer=str(self.plateau[i][j])
        #self.bind_all('<Key>',lambda event : self.printer(event,liste)) # Action pour entrer les nombres
        

        

    def printer(self,event,liste):
        i=liste[0]
        j=liste[1]
        if event.char=="": # touche backspace
            if len(self.nombreaentrer)==1:
                self.nombreaentrer="0"
            else:
                self.nombreaentrer=self.nombreaentrer[0:-1]
        elif len(self.nombreaentrer)<=1 and event.char=="0":
            return 0
            
        else:
            try:
                int(event.char)
                if len(self.nombreaentrer)<4:
                    self.nombreaentrer+=str(event.char)
            except:
                return 0
        self.deleteAllCanvas()
        self.plateau[i][j]=int(self.nombreaentrer)
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())

        #self.entreenombre=self.can.create_text(self.x0 +self.taillePlateau.get()*(j+0.5),self.y0+self.taillePlateau.get()*(i+0.5),text=self.nombreaentrer,font=self.style)

    def quitter(self):
        self.destroy()


                    


    def changertheme(self,specialtheme="",background="khaki",forbiddencase="",emptycase="",normalcase=""):
        self.can.config(bg=background)
        self.can.delete(ALL)
        if specialtheme=="Sakuro":
            for i in range(30):
                Sakura(self.can,self)
            self.specialtheme="Sakuro"
        elif specialtheme=="Halloweeno":
            for i in range(30):
                Sakura(self.can,self,"images/halloween.gif","images/halloween.gif")
            self.specialtheme="Halloweeno"
            
        elif specialtheme=="Wintero":
             for i in range(100):
                Sakura(self.can,self,"images/winter.gif","images/winter.gif")
             self.specialtheme="Wintero"
        else:
            self.specialtheme=""
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())
        
            



        
exemple = PlateauEditeur([[-1, -1, (4, 0), (10, 0), -1, -1, -1],
                          [-1, (0, 4), 0, 0, -1, (3, 0), (4, 0)], [-1, (0, 3), 0, 0, (11, 4), 0, 0],
                          [-1, (3, 0), (4, 10), 0, 0, 0, 0], [(0, 11), 0, 0, 0, 0, (4, 0), -1],
                          [(0, 4), 0, 0, (0, 4), 0, 0, -1], [-1, -1, -1, (0, 3), 0, 0, -1]])    


##exemple = Plateau([[-1,-1,(4,0),(10,0),-1,-1,-1],[-1,(0,4),0,1,-1,(3,0),(4,0)],[-1,(0,3),1,2,(11,4),0,3],
##[-1,(3,0),(4,10),4,3,2,1],
##[(0,11),2,1,3,5,(4,0),-1],
##[(0,4),1,3,(0,4),1,3,-1],
##[-1,-1,-1,(0,3),2,1,-1]
##],[[-1,-1,(4,0),(10,0),-1,-1,-1],[-1,(0,4),3,1,-1,(3,0),(4,0)],[-1,(0,3),1,2,(11,4),1,3],
##[-1,(3,0),(4,10),4,3,2,1],
##[(0,11),2,1,3,5,(4,0),-1],
##[(0,4),1,3,(0,4),1,3,-1],
##[-1,-1,-1,(0,3),2,1,-1]
##])

if __name__=="__main__":
    app=ApplicationEditeur(exemple)


