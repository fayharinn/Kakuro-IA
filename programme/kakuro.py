from tkinter import *
from tkinter.messagebox import * #Gestion des boites de dialogue
from random import randint
from tkinter.filedialog import * # pour les askopenfilename
import gc # pour libérer la mémoire
import pickle # pour sauvegarder les plateaux
from editeur import sauvegardeobj,chargerobj
from os import system as python
import subprocess

class Plateau(list):
    def __init__(self,plateau,solution):
        list.__init__(self,plateau)
        self.solution=solution

    def getLongueur(self):
        return len(self)

    def getLargeur(self):
        return len(self[0])



class PlateauEditeur(Plateau):
    def __init__(self,plateau,solution):
        Plateau.__init__(plateau,solution)
        
        
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




class Application(Tk):
    def __init__(self,plateau):
        Tk.__init__(self)
        self.plateau=plateau
        self.longueurCan=640
        self.largeurCan=480
        self.taillePlateau =IntVar()
        self.taillePlateau.set(60) # Plus la valeur est grande et plus le plateau est graphiquement gros
        self.x0,self.y0=20,20  # Position du plateau
        self.nombreaentrer="0"
        self.style="Helvetica 13 bold italic" # font des nombres écrits sur la grille
        self.title('Kakuro')
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
        option.add_command(label="Charger un plateau",command=self.chargerPlateau)
        option.add_command(label="Enregistrer la partie",command=self.sauvegardePlateau)
        option.add_command(label="Enregistrer en tant que correction",command=self.sauvegardeCorrection)
        option.add_command(label="Mode Editeur",command=self.edit)
        option.add_separator()
        option.add_command(label="Quitter",command=self.quitter)
        cadre=Frame(self, padx=5) # cadre des boutons
        cadre.pack(side=RIGHT)
        labelAide = Label(cadre, text="Proposition d'aide : ") #Label non dynamique
        labelAide.pack()
        self.infoAideVar=StringVar() #texte dynamique de l'info
        infoAide = Label(cadre, textvariable=self.infoAideVar) #label contenant le texte dynamique
        infoAide.pack()
        bverif=Button(cadre,width=10,text="Vérifier",font=self.style,command=self.verifier)
        bverif.pack()
        breset=Button(cadre,width=10,text="Reset",font=self.style,command=self.reset)
        breset.pack()
        self.var1 = IntVar()
        self.var2 = IntVar()
        check1 = Checkbutton(cadre, text="Aide fausse valeur", variable=self.var1, onvalue=1, offvalue=0)
        check2 = Checkbutton(cadre, text="Aide case facile", variable=self.var2,onvalue=1, offvalue=0)
        check1.pack()
        check2.pack()
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
        
    def sauvegardePlateau(self):
        try:
            file = asksaveasfilename(title="Enregistrer le plateau édité",filetypes=[('fichier dat','.dat')],initialfile="Sauvegarde.dat")
            sauvegardeobj((self.plateau,self.taillePlateau.get()),file)
        except:pass

    def sauvegardeCorrection(self):
         try:
            file = asksaveasfilename(title="Enregistrer en tant que correction",filetypes=[('fichier corr','.corr')],initialfile="Sauvegarde.corr")
            sauvegardeobj((self.plateau,self.taillePlateau.get()),file)
         except:pass       
        

                
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


    def reset(self):
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                if type(self.plateau[i][j]) is int:
                    if self.plateau[i][j]>0:
                        self.plateau[i][j]=0
        self.redraw()

    def edit(self):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #si.wShowWindow = subprocess.SW_HIDE # default
        subprocess.call('python editeur.py', startupinfo=si)

    
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
                            
                            can.create_image(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),image=self.giftbox)
                        elif self.specialtheme=="Halloweeno":
                            
                            can.create_image(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),image=self.sorcer)
                        elif self.specialtheme=="Sakuro":
                            char=randint(0,len(self.japanesechar)-1) 
                            can.create_image(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),image=self.listeimjap[char])
                            
                        can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="black",stipple='gray25')
                    
                    elif self.plateau[i][j]!=0: # si un nb est deja entré dans la case
                        can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="#DAD3D3",tags=[str(i)+","+str(j)])
                        can.create_text(x0 +taillePlateau*(j+0.5),y0+taillePlateau*(i+0.5),text=str(self.plateau[i][j]),font=style,tags=[str(i)+";"+str(j)])
                        can.tag_bind(str(i)+","+str(j), '<ButtonPress-1>', lambda event, i=i,j=j:self.onClick(event,(i,j)))
                        can.tag_bind(str(i)+";"+str(j), '<ButtonPress-1>', lambda event, i=i,j=j:self.onClick(event,(i,j)))
                        can.tag_bind(str(i)+","+str(j), '<Button-3>', lambda event, i=i,j=j:self.clickAide(event,i,j))
                        can.tag_bind(str(i)+";"+str(j), '<Button-3>', lambda event, i=i,j=j:self.clickAide(event,i,j))
                        
                    else: # si la case est vide
                        can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="white",tags=str(i)+","+str(j))
                        can.tag_bind(str(i)+","+str(j), '<ButtonPress-1>', lambda event, i=i,j=j:self.onClick(event,(i,j)))
                        can.tag_bind(str(i)+","+str(j), '<Button-3>', lambda event, i=i,j=j:self.clickAide(event,i,j))
                        
                else:
                    can.create_rectangle(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1),fill="grey")
                    can.create_line(x0 +taillePlateau*j,y0+taillePlateau*i,x0 +taillePlateau*(j+1),y0+taillePlateau*(i+1))
                    if self.plateau[i][j][0]>0:
                        can.create_text(x0 +taillePlateau*(j+0.2),y0+taillePlateau*(i+0.8),text=str(self.plateau[i][j][0]))
                    if self.plateau[i][j][1]>0:
                        can.create_text(x0 +taillePlateau*(j+0.8),y0+taillePlateau*(i+0.2),text=str(self.plateau[i][j][1]))
                    
                               
                    
        
    def onClick(self,event,liste):
        self.redraw()
        i=liste[0]
        j=liste[1]
        self.can.itemconfigure(str(i)+","+str(j),fill="#DAD3D3")
        self.nombreaentrer=str(self.plateau[i][j])
        self.bind_all('<Key>',lambda event : self.printer(event,liste)) # Action pour entrer les nombres
        
    def clickAide(self,envent,i,j):
        aide=proposeAide(self.plateau,i,j)
        self.infoAideVar.set(str(aide))
        #print(aide)
        

    def printer(self,event,liste):
        gc.collect()
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
        try:
            listeobj=self.can.find_all()
            for x in listeobj:
                if "theme" not in self.can.gettags(x):
                    self.can.delete(x)
        except:
            pass
        self.plateau[i][j]=int(self.nombreaentrer)
        self.dessinePlateau(self.can,self.plateau.getLongueur(),self.plateau.getLargeur())
        #case les plus facile a colorier
        if self.var2.get()==1:
            self.plusFacileColoration()
        #verifie si la case est fausse grâce au CSP
        if self.var1.get()==1:
            self.verifInstantanne(i,j)


        #self.entreenombre=self.can.create_text(self.x0 +self.taillePlateau.get()*(j+0.5),self.y0+self.taillePlateau.get()*(i+0.5),text=self.nombreaentrer,font=self.style)

    def quitter(self):
        self.destroy()

    def verifier(self):
        if len(self.plateau.solution)==0:
            if est_rempli(self.plateau):
                if est_solvable(self.plateau):
                    showinfo("Bravo","La grille est correcte")
                else:
                    showinfo("Erreur","Une ou plusieurs cases sont incorrectes")
            if est_solvable(self.plateau):
                showinfo("Erreur","Une ou plusieurs cases sont incorrectes")
            else:
                showinfo("Attention","Complétez entièrement la grille pour vérifier")
            return 
        if self.plateau==self.plateau.solution:
            showinfo("Bravo","La grille est correcte")
        else:
            nombredefautes=0
            for  i in range (len(self.plateau)):
                for j in range (len(self.plateau[i])):
                    if self.plateau[i][j]!=self.plateau.solution[i][j]:
                        nombredefautes+=1
                        self.can.create_rectangle(self.x0 +self.taillePlateau.get()*j,self.y0+self.taillePlateau.get()*i,self.x0 +
                                                  self.taillePlateau.get()*(j+1),self.y0+self.taillePlateau.get()*(i+1),fill="red",stipple='gray12',tags=str(i)+","+str(j))
                        
                    
            showinfo("Faux","Il y a "+str(nombredefautes)+" cases incorectes")


    def verifInstantanne(self,i,j):
        if len(self.plateau.solution)==0:
            if self.plateau[i][j] not in proposeAide(self.plateau,i,j):
                self.can.create_rectangle(self.x0 +self.taillePlateau.get()*j,self.y0+self.taillePlateau.get()*i,self.x0 +
                                          self.taillePlateau.get()*(j+1),self.y0+self.taillePlateau.get()*(i+1),fill="red",stipple='gray12',tags=str(i)+","+str(j))
        else:
            for  i in range (len(self.plateau)):
                for j in range (len(self.plateau[i])):
                    if self.plateau[i][j]!=self.plateau.solution[i][j] and self.plateau[i][j]!=0:
                        self.can.create_rectangle(self.x0 +self.taillePlateau.get()*j,self.y0+self.taillePlateau.get()*i,self.x0 +
                                                  self.taillePlateau.get()*(j+1),self.y0+self.taillePlateau.get()*(i+1),fill="red",stipple='gray12',tags=str(i)+","+str(j))
            
    def plusFacileColoration(self):
        for  i in range (len(self.plateau)):
            for j in range (len(self.plateau[i])):
                if len(proposeAide(self.plateau,i,j))==1 and self.plateau[i][j]!= -1 and type(self.plateau[i][j])!= tuple :
                    self.can.create_rectangle(self.x0 +self.taillePlateau.get()*j,self.y0+self.taillePlateau.get()*i,self.x0 +
                                              self.taillePlateau.get()*(j+1),self.y0+self.taillePlateau.get()*(i+1),fill="blue",stipple='gray12',tags=str(i)+","+str(j))
                        
            

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
        
            


#==============================================================CSP==============================================================

def getLigne(p,i,j,c2=0):
    ligne=[]
    ##recupere les valeurs de la ligne
    #apres
    for caseColonne in range(j+1,len(p)):
        if type(p[i][caseColonne]) != tuple and p[i][caseColonne] != -1  and p[i][caseColonne]!=c2:
            ligne.append(p[i][caseColonne])
        if type(p[i][caseColonne]) == tuple or type(p[i][caseColonne]) == -1:
            break
        
    #avant
    for caseColonne in range(j-1,0,-1):
        if type(p[i][caseColonne]) != tuple and p[i][caseColonne] != -1  and p[i][caseColonne]!=c2:
            ligne.append(p[i][caseColonne])
        if type(p[i][caseColonne]) == tuple or type(p[i][caseColonne]) == -1:
            break

    return ligne

def getColonne(p,i,j,c2=0):
    colonne=[]
    ##recupere les valeurs de la ligne
    #apres la case j (non compris)
    for caseLigne in range(i+1,len(p)):
        if type(p[caseLigne][j]) != tuple and p[caseLigne][j] != -1 and p[caseLigne][j]!=c2 :
            colonne.append(p[caseLigne][j])
        if type(p[caseLigne][j]) == tuple or type(p[caseLigne][j]) == -1:
            break
        
    #avant la case j
    for caseLigne in range(i-1,0,-1):
        if type(p[caseLigne][j]) != tuple and p[caseLigne][j] != -1  and p[caseLigne][j]!=c2:
            colonne.append(p[caseLigne][j])
        if type(p[caseLigne][j]) == tuple or type(p[caseLigne][j]) == -1:
            break

    return colonne

def allDifferent(p,i,j,nb): #plateau, coordonné ligne, coordonné colonne, nb qu'on place
    colonne=getColonne(p,i,j)
    ligne=getLigne(p,i,j)
    if nb in colonne:
        return False 
    if nb in ligne:
        return False
    return True

def getSomme(p,i,j):
    s1=0
    s2=0
    for y in range(j,-1,-1):
        if type(p[i][y])==tuple:
            s1=p[i][y][1]
            break # por recuperer que  le premier
    for x in range(i,-1,-1):
        if type(p[x][j])==tuple:
            s2=p[x][j][0]
            break
    return(s1,s2)

def contrainteSomme(p,i,j,nb): #la somme avec le nb doit etre plus petit
    colonne=getColonne(p,i,j)
    ligne=getLigne(p,i,j)
    sommeligne=getSomme(p,i,j)[0]
    sommecolonne=getSomme(p,i,j)[1]
    sligne=0
    scolonne=0
    if nb==sommeligne or nb==sommecolonne:
        return False
    for x in ligne:
        sligne+=x
    if sligne+nb>sommeligne:
        if sommeligne!=0:
            return False
    for x in colonne:
        scolonne+=x
    if scolonne+nb>sommecolonne:
        if sommecolonne!=0:
            return False
    return True


def contrainteSomme2(p,i,j,nb): #quand il manque plus qu'un chiffre sur la ligne à remplir
    ligne=getLigne(p,i,j,-1)
    sligne=0

    sommeligne=getSomme(p,i,j)[0]

    if 0 in ligne:
        return True
    
    for x in ligne:
        sligne+=x

    if sligne+nb!=sommeligne:
        return False
    
    return True


def contrainteSomme3(p,i,j,nb): #quand il manque plus qu'un chiffre sur la colonne à remplir
    colonne=getColonne(p,i,j,-1)
    scolonne=0

    sommecolonne=getSomme(p,i,j)[1]

    if 0 in colonne:
        return True
    
    for x in colonne:
        scolonne+=x

    if scolonne+nb!=sommecolonne:
        return False
    
    return True

def proposeAideEasy(p,i,j): #aide qui propose n'importe qu'elle chiffre 
    proposition=[]
    colonne=getColonne(p,i,j)
    ligne=getLigne(p,i,j)

    for nb in range(1,9):
        if nb not in ligne or nb not in colonne:
            proposition.append(nb)
    return proposition


def proposeAide(p,i,j): #aide qui propose n'importe qu'elle chiffre suivant la somme
    proposition=[]
    colonne=getColonne(p,i,j)
    ligne=getLigne(p,i,j)

    for nb in range(1,9):
        if (allDifferent(p,i,j,nb)) and contrainteSomme(p,i,j,nb) and contrainteSomme2(p,i,j,nb) and contrainteSomme3(p,i,j,nb):
            proposition.append(nb)
    return proposition
    
#================================================================RESOLUTION===============================================================
def est_solvable(plateau):
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if type(plateau[i][j]) is int:
                if plateau[i][j]>=0:
                    if len(proposeAide(plateau,i,j))==0:
                        print("e")
                        return False
    return True



def is_numberCase(i,j,plateau):
    nb=plateau[i][j]
    if type(nb) is int:
        if nb>=0:
            return True
    return False


def liste_possible(plateau):
    asuivre={}
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if is_numberCase(i,j,plateau):
                liste_possible=proposeAide(plateau,i,j)
                if len(liste_possible)>0:
                    asuivre[(str(i)+","+str(j))]=liste_possible
    return asuivre
                            
                                    
                                    
def remplir_evidence(plateau):
    dic_possible=liste_possible(plateau)
    for case in dic_possible:
        if len(dic_possible[case])==1:
            (i,j)=case.split(",")
            print(i)
            print(j)
            plateau[int(i)][int(j)]=dic_possible[case][0]



def resoudre(plateau): # pas terminé
    dic={}
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if is_numberCase(i,j,plateau):
                dic[str(i)+","+str(j)]=proposeAide(plateau,i,j)
    return dic




def est_rempli(plateau):
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j]==0:
                return False
    return True


exemple = Plateau([[-1,-1,(4,0),(10,0),-1,-1,-1],[-1,(0,4),0,0,-1,(3,0),(4,0)],[-1,(0,3),0,0,(11,4),0,0],
[-1,(3,0),(4,10),0,0,0,0],
[(0,11),0,0,0,0,(4,0),-1],
[(0,4),0,0,(0,4),0,0,-1],
[-1,-1,-1,(0,3),0,0,-1]
],[[-1,-1,(4,0),(10,0),-1,-1,-1],[-1,(0,4),3,1,-1,(3,0),(4,0)],[-1,(0,3),1,2,(11,4),1,3],
[-1,(3,0),(4,10),4,3,2,1],
[(0,11),2,1,3,5,(4,0),-1],
[(0,4),1,3,(0,4),1,3,-1],
[-1,-1,-1,(0,3),2,1,-1]
])


                        

Application(exemple)


