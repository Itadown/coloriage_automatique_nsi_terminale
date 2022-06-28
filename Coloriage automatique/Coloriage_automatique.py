"""
Les numéros à partir de #500 en début de commentaire permettent de relier
différentes parties du code avec ctrl-f pour mieux comprendre.
"""

#-*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk, ImageGrab
from os import rename, remove
import copy



############################################################



def choix_image():
    """
    choix_image() permet de lancer la première fenêtre vue
    par l'utilisateur et permet de choisir l'image
    et une fois l'image sélectionné, de lancer la fonction
    coloriage_image() pour commencer le coloriage.
    """
    global win, image_choisie, liste_imgCombo, variable_stop

    image_choisie = 0

    variable_stop = False

    win = Tk()
    win.geometry("600x400")
    win.title("Choix d'image")
    win.config(bg = "#282828")

    liste_img = ["Toad [par défaut]", "Mario", "Bowser", "Koopa"]

    espace = Label(win, width = 1, height = 1, anchor = CENTER) #label qui sert d'espace pour rendre plus propre
    espace.config(bg = "#282828")
    espace.pack()

    apercu_images = Image.open("../Coloriage automatique/apercu_image.jpg")
    apercu_images.load()
    ap_images = ImageTk.PhotoImage(apercu_images)

    canv = Canvas(win, height = ap_images.height(), width = ap_images.width(), highlightthickness = 0)
    canv.create_image(0, 0, anchor = NW, image = ap_images)
    canv.pack()

    espace = Label(win, width = 1, height = 1, anchor = CENTER) #label qui sert d'espace pour rendre plus propre
    espace.config(bg = "#282828")
    espace.pack()


    liste_imgCombo = ttk.Combobox(win, values = liste_img)
    liste_imgCombo.current(0)
    liste_imgCombo.pack()

    liste_imgCombo.bind('<<ComboboxSelected>>', selected)

    win.protocol("WM_DELETE_WINDOW", lambda : stop_choix_image()) #quand on clique sur la croix ou on fait alt + f4, ça lance stop_choix_image()

    espace = Label(win, width = 1, height = 1, anchor = CENTER) #label qui sert d'espace pour rendre plus propre
    espace.config(bg = "#282828")
    espace.pack()

    button = Button(win, text = 'Sélectionner cette image', command = win.destroy)
    button.pack()
    win.mainloop()

    if variable_stop == False:
        coloriage_image()


##############################


def stop_choix_image():
    """
    stop_choix_image() sert à stopper la fonction choix_image()
    quand on clique sur la croix et permet donc d'éviter de
    continuer le programme alors que l'utilisateur ne veut pas
    frocément le continuer.
    """
    global variable_stop
    variable_stop = True
    win.destroy()


##############################


def selected(event):
    """
    selected() permet de créer une variable global : image_choisie
    qui permettra de choisir l'image dans coloriage_image() (voir #508)
    """
    global image, image_choisie
    image = liste_imgCombo.get()
    if image == "Toad [par défaut]":
        image_choisie = 0
    if image == "Mario":
        image_choisie = 1
    if image == "Bowser":
        image_choisie = 2
    if image == "Koopa":
        image_choisie = 3



############################################################



def coloriage_image():
    """
    coloriage_image() est la fonction qui crée la deuxième fenêtre
    vue par l'utilisateur et où il y a toute la présentation de la
    fenêtre ainsi que tout les lancements de fonctions qui permettent
    des modifications.
    """
    global data, fen, photo, pixels, img, can, creation_image, pas_de_couleur, image_redo, image_undo, panel, enregistrer_ou_non

    data = []

    enregistrer_ou_non = True #variable permettant de savoir si il y a eut des modfications ou non sur l'image depuis le dernier enregistrement

    pas_de_couleur = True


    #Création fenêtre
    fen = Tk()
    fen.geometry("600x400")
    fen.title('Coloriage')
    fen.config(bg = "#282828")


    #Création menu (fichier, éditer, aide)
    menubar = Menu(fen)

    menu1 = Menu(menubar, tearoff = 0)
    menu1.add_command(label="Enregistrer", command = lambda : enregistrer(""), accelerator = "Ctrl+S") #502
    menu1.add_command(label="Enregistrer sous...", command = lambda : enregistrer_sous(""), accelerator = "Ctrl+Maj+S") #503
    menubar.add_cascade(label="Fichier", menu = menu1)

    menu2 = Menu(menubar, tearoff = 0)
    menu2.add_command(label="Changer d'image",command = lambda : changement_image(1), accelerator = "Ctrl+A") #505
    menu2.add_separator()
    menu2.add_command(label="Annuler", command = lambda : retour_arriere(""), accelerator = "Ctrl+Z") #506
    menu2.add_command(label="Refaire", command = lambda : refaire(""), accelerator = "Ctrl+Y") #507
    menubar.add_cascade(label="Editer", menu = menu2)

    menu3 = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label = "Aide", menu = menu3)
    menuaide1 = Menu(menu3, tearoff = 0)
    menuaide2 = Menu(menuaide1, tearoff = 0)
    menuaide3 = Menu(menuaide2, tearoff = 0)
    menuaide4 = Menu(menuaide3, tearoff = 0)
    menu3.add_cascade(label="A propos", underline=0, menu = menuaide1)
    menuaide1.add_cascade(label="Il n'y a pas", underline=0, menu = menuaide2)
    menuaide2.add_cascade(label="d'aide.", underline=0, menu = menuaide3)
    menuaide3.add_cascade(label="Désolé", underline=0, menu = menuaide4)
    menuaide4.add_command(label=";(")

    fen.config(menu = menubar)


    #L'image choisie va être ouverte ici
    #508
    if image_choisie == 0:
        photo = Image.open("toad_nb.jpg")
    if image_choisie == 1:
        photo = Image.open("mario_nb.jpg")
    if image_choisie == 2:
        photo = Image.open("bowser_nb.jpg")
    if image_choisie == 3:
        photo = Image.open("koopa_nb.jpg")

    espace = Label(fen, width = 0, height = 2, anchor = CENTER) #label qui sert d'espace pour rendre plus propre
    espace.config(bg = "#282828")
    espace.grid(column = 1, row = 0)


    #Création de l'image choisie
    pixels = photo.load()
    img = ImageTk.PhotoImage(photo)
    can = Canvas(fen, height = img.height(), width = img.width(), highlightthickness = 0)
    creation_image = can.create_image(0, 0, anchor = NW, image = img)
    can.grid(column = 1, row = 1)
    can.bind('<Button-1>', colorie) #500 Quand on clique sur l'image choisis, ça lance colorie


    espace = Label(fen, width = 5, height = 0, anchor = CENTER) #label qui sert d'espace pour rendre plus propre
    espace.config(bg = "#282828")
    espace.grid(column = 0, row = 1)

    espace = Label(fen, width = 2, height = 0, anchor = CENTER) #label qui sert d'espace pour rendre plus propre
    espace.config(bg = "#282828")
    espace.grid(column = 2, row = 1)


    #Création du panel de couleur
    panel = Image.open("panel_color.jpg")
    img_panel = photo
    panel_can = ImageTk.PhotoImage(panel)
    img_can = ImageTk.PhotoImage(photo)

    can_couleur = Canvas(fen, height = panel_can.height(), width = panel_can.width(), highlightthickness = 0)
    can_couleur.create_image(0, 0, anchor = NW, image = panel_can)
    can_couleur.grid(column = 5, row = 1)
    can_couleur.bind('<Button-1>', panel_couleurs) #501, quand on clique sur le panel de couleur, ça lance panel_couleurs

    getData_panel()


    #Racourcis clavier
    fen.bind_all("<Control-s>", enregistrer) #502
    fen.bind_all("<Control-Shift-KeyPress-S>", enregistrer_sous) #503
    fen.bind_all("<Control-a>", changement_image) #505
    fen.bind_all("<Control-z>", retour_arriere) #506
    fen.bind_all("<Control-y>", refaire) #507

    fen.protocol("WM_DELETE_WINDOW", lambda : quitter("")) #504


    #Création variables pour la fonction retour_arriere() et refaire(), et enregistrement de la première image undo
    image_redo = 0
    image_undo = 0
    photo.save("undo" + str(image_undo) + ".jpg")


    fen.mainloop()



############################################################



def colorie(event):
    """
    colorie() sert à prendre la position du click grâce à la
    commande #500 (cherchez avec ctrl-f) et lance les fonctions
    getdata(), remplir_rec() et update(),
    la fonction sert aussi à savoir si on clique sur une bordure
    ou un endroit déjà colorié et ne lance pas les autres fonctions
    si on est pas sur du blanc en renvoyant un message d'erreur à
    l'utilisateur.
    """
    X = event.x
    Y = event.y

    global pas_de_couleur, image_redo, image_undo, data, enregistrer_ou_non

    if pas_de_couleur == True:
        return

    getData()

    if data[Y-1][X-1][0] >= 180 and data[Y-1][X-1][1] >= 180 and data[Y-1][X-1][2] >= 180:
        remplir_rec(data, X, Y)
        update()
        image_undo = image_undo + 1
        photo.save("undo" + str(image_undo) + ".jpg")
        while image_redo > 0:
            remove("redo" + str(image_redo) + ".jpg")
            image_redo = image_redo - 1
        enregistrer_ou_non = False
    else:
        messagebox.showwarning(title = "Ne cliquez pas là !", message = "Ne cliquez pas sur une bordure ou une zone colorié !!")
        return


##############################


def getData():
    """
    getData() sert à modifier data pour qu'il apprenne
    les couleurs des pixels de l'image.
    """
    width, height = photo.size
    for y in range(height):
        ligne = []
        for x in range(width):
            ligne.append(pixels[x, y])
        data.append(ligne)


##############################


def remplir_rec(tab, x, y):
    """
    remplir_rec() a en entré un tableau de pixel et leur couleur et des
    entiers x et y qui servent à prendre la position dans le tableau, et
    renvoie le tableau de l'image modifié, cette fonction fonctionne par
    récursivité.
    """
    if y-1 >= len(tab) or x-1 >= len(tab[y-1]):
        return tab

    if tab[y-1][x-1][0] <= 180 and tab[y-1][x-1][1] <= 180 and tab[y-1][x-1][2] <= 180 :
        return tab

    if x == 0 or y == 0:
        return ("Erreur ce pixel n'existe pas")

    if tab[y-1][x-1][0] >= 180 and tab[y-1][x-1][1] >= 180 and tab[y-1][x-1][2] >= 180 :
        tab[y-1][x-1] = RGB[0]

        remplir_rec(tab, x, y+1) #Vers en bas
        remplir_rec(tab, x, y-1) #Vers en haut
        remplir_rec(tab, x+1, y) #Vers la droite
        remplir_rec(tab, x-1, y) #Vers la gauche
    return tab


##############################


def update():
    """
    update() permet de modifier l'image après le coloriage effectué.
    """
    width, height = photo.size  #Taille de l'image
    for y in range(height):
        for x in range(width):
            pixels[x, y] = data[y][x]
    img.paste(photo)



############################################################



data_panel = []
RGB = []               #Tableau avec un tuppple RGB exemple : [(255,255,255)]
def getData_panel():
    """
    getData_panel() sert à modifier data_panel afin qu'il contienne
    les couleurs de chaque pixel du panel de couleur vu par l'utilisateur.
    """
    pixel_panel = panel.load()

    width, height = panel.size
    for y in range(height):
        ligne = []
        for x in range(width):
            ligne.append(pixel_panel[x, y])
        data_panel.append(ligne)


##############################


def panel_couleurs(event):
    """
    panel_couleurs() permet de prendre la couleur au clique sur
    le panel de couleur grâce à la commande #501 et change le curseur
    une fois la couleur choisie.
    """
    global pas_de_couleur
    pas_de_couleur = False

    X = event.x
    Y = event.y
    RGB.append(data_panel[Y-1][X-1])
    if len(RGB)-1 > 0:        #Sert à enlever l'ancienne valeur RGB selectionner
        RGB.pop(0)
    can.config(cursor = "spraycan") #Permet de changer le curseur
    return RGB



############################################################



def enregistrer(event):
    """
    enregistrer() permet grâce à la commande ctrl + s ou en cliquant
    sur enregistrer dans la section du menu fichier d'enregistrer à
    l'endroit choisis par l'utilisateur (voir #502).
    """
    global enregistrer_ou_non, image_choisie
    if image_choisie == 0:
        photo.save("Toad - New.jpg")
    if image_choisie == 1:
        photo.save("Mario - New.jpg")
    if image_choisie == 2:
        photo.save("Bowser - New.jpg")
    if image_choisie == 3:
        photo.save("Koopa - New.jpg")
    enregistrer_ou_non = True


##############################


def enregistrer_sous(event):
    """
    enregistrer_sous() permet grâce à la commande ctrl + maj + s ou en cliquant
    sur enregistrer sous... dans la section du menu fichier d'enregistrer à
    l'endroit choisis par l'utilisateur (voir #503).
    """
    global enregistrer_ou_non
    fichier = filedialog.asksaveasfilename(title = "Enregistrez où vous le souhaitez !", defaultextension='.jpg', filetypes = [('JPEG', '*.jpg;*.jpeg;*.jpe;*.jfif')])
    if fichier != "":
        photo.save(fichier)
        enregistrer_ou_non = True


##############################


def quitter(event):
    """
    quitter() permet grâce à la commande alt + f4 ou en cliquant sur
    la croix en haut à droite (voir #504) à fermer la fenêtre (si l'image n'est pas
    enregistrer alors cette fonction ouvre une fenêtre pour avertir).
    Elle supprime également toutes les images undo et redo.
    """
    global image_undo, image_redo, fen, enregistrer_ou_non
    if enregistrer_ou_non == False: #Sert à dire d'enregistrer avant de quitter avec un avertissement
        if askyesno('Ne faîtes pas ça', "Êtes-vous sur de vouloir quitter ? \n(Enregistrez bien avant, sinon vous perdrez votre image)"):
            while image_undo >= 0:
                remove("undo" + str(image_undo) + ".jpg")
                image_undo = image_undo - 1
            while image_redo > 0:
                remove("redo" + str(image_redo ) + ".jpg")
                image_redo = image_redo - 1
            fen.destroy()
    else: #Vu que c'est déjà enregistrer, ne met pas d'avertissement et quitte
        while image_undo >= 0:
            remove("undo" + str(image_undo) + ".jpg")
            image_undo = image_undo - 1
        while image_redo > 0:
            remove("redo" + str(image_redo ) + ".jpg")
            image_redo = image_redo - 1
        fen.destroy()
    return


##############################


def changement_image(event):
    """
    changement_image() permet grâce à la commande ctrl + a ou en cliquant sur
    éditer/changer d'image (voir #505), de changer d'image en fermant la fenêtre actuelle
    (si l'image n'est pas enregistrer alors cette fonction ouvre une fenêtre pour avertir).
    Elle supprime également toutes les images undo et redo et relance choix_image().
    """
    global image_undo, image_redo, fen, enregistrer_ou_non
    if enregistrer_ou_non == False: #Sert à dire d'enregistrer avant de changer d'image avec un avertissement
        if askyesno('Attention', "Êtes-vous sur de vouloir changer d'image ? \n(Enregistrez bien avant, sinon vous perdrez votre image)"):
                while image_undo >= 0:
                    remove("undo" + str(image_undo) + ".jpg")
                    image_undo = image_undo - 1
                while image_redo > 0:
                    remove("redo" + str(image_redo ) + ".jpg")
                    image_redo = image_redo - 1
                fen.destroy()
                choix_image()
    else: #Vu que c'est déjà enregistrer, ne met pas d'avertissement et chnage d'image
        while image_undo >= 0:
            remove("undo" + str(image_undo) + ".jpg")
            image_undo = image_undo - 1
        while image_redo > 0:
            remove("redo" + str(image_redo ) + ".jpg")
            image_redo = image_redo - 1
        fen.destroy()
        choix_image()


##############################


def retour_arriere(event):
    """
    retour_arriere() permet grâce à la commande ctrl + z ou en cliquant sur
    éditer/annuler (voir #506), d'enlever la dernière couleure effectuer et
    reset donc data.
    """
    global image_undo, image_redo, data, photo, pixels, img, can, enregistrer_ou_non
    if image_undo == 0:
        return
    data = []
    photo = Image.open("undo" + str(image_undo - 1) + ".jpg")
    pixels = photo.load()
    img = ImageTk.PhotoImage(photo)
    can.itemconfig(creation_image, image = img)

    image_redo = image_redo + 1
    rename("undo" + str(image_undo) + ".jpg", "redo" + str(image_redo) + ".jpg")
    image_undo = image_undo - 1
    enregistrer_ou_non = False


##############################


def refaire(event):
    """
    refaire() permet grâce à la commande ctrl + y ou en cliquant sur
    éditer/refaire (voir #507), de remettre la dernière couleure enlever et
    reset donc data.
    """
    global image_undo, image_redo, data, photo, pixels, img, can, enregistrer_ou_non
    if image_redo == 0:
        return
    data = []
    photo = Image.open("redo" + str(image_redo) + ".jpg")
    pixels = photo.load()
    img = ImageTk.PhotoImage(photo)
    can.itemconfig(creation_image, image = img)

    image_undo = image_undo + 1
    rename("redo" + str(image_redo) + ".jpg", "undo" + str(image_undo) + ".jpg")
    image_redo = image_redo - 1
    enregistrer_ou_non = False


############################################################

choix_image()



print("#####    ##    ## ##            ##      ##     ##")
print("##   ##   ##  ##  ##           ####     ####   ##")
print("##    ##    ##    ##          ##  ##    ## ##  ##")
print("##    ##    ##    ##         ########   ##  ## ##")
print("##   ##     ##    ##        ##      ##  ##   ####")
print("#####       ##    ######## ##        ## ##    ###")
print(" ")
print(" ")
print("######## ##########")
print("##           ##")
print("####         ##")
print("##           ##")
print("##           ##")
print("########     ##")
print(" ")
print(" ")
print("########## ##      ##  ########    ######    ##########  ##  ####    ####")
print("    ##     ##      ##  ##        ##      ##      ##          ## ##  ## ##")
print("    ##     ##########  ####     ##        ##     ##      ##  ##   ##   ##")
print("    ##     ##      ##  ##       ##        ##     ##      ##  ##        ##")
print("    ##     ##      ##  ##        ##      ##      ##      ##  ##        ##")
print("    ##     ##      ##  ########    ######        ##      ##  ##        ##")