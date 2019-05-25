#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
import os, sys
#Importation des bibliothèques
import tkinter as tk
from tkinter import *
import random as rd
import pygame
from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import sqlite3
import pygameMenu
from pygameMenu.locals import *
from pygame.locals import *
from random import randrange
import os
#********************************************#

pygame.init()

s=0
def lettre_dans_mot(lettre) :
    global s
    global partie_en_cours, mot_partiel, mot_choisi, nb_echecs, image_pendu,nomE
    if partie_en_cours : 
        nouveau_mot_partiel = ""
        lettre_dans_mot = False
        i=0
        while i<len(mot_choisi):
            if mot_choisi[i]==lettre:
                nouveau_mot_partiel = nouveau_mot_partiel + lettre
                lettre_dans_mot = True 
            else:
                nouveau_mot_partiel = nouveau_mot_partiel + mot_partiel[i]
            i+=1
        mot_partiel = nouveau_mot_partiel  
        afficher_mot(mot_partiel)
        if not lettre_dans_mot :# lettre fausse. Changer le dessin.
            nb_echecs += 1
            nomFichier = "C:/Users/Hp/Desktop/projet intégré/pendu_"+str(nb_echecs)+".gif"
            photo=PhotoImage(file=nomFichier)
            image_pendu.config(image=photo)
            image_pendu.image=photo
            if nb_echecs == 7:  # trop d'erreurs. Fini.
                partie_en_cours = False
                afficher_mot(mot_choisi)
        elif mot_partiel == mot_choisi:# le mot a été trouvé !
            set_score()
            scor=charger_score()
            afficher_score(scor)  
            partie_en_cours = False
 

def afficher_mot(mot):
    global lettres
    mot_large = ""
    i=0
    while i<len(mot):  # ajoute un espace entre les lettres
        mot_large = mot_large + mot[i] + " "
        i+=1
    canevas.delete(lettres)
    lettres = canevas.create_text(320,60,text=mot_large,fill='blue',font='Courrier 30') 
    
    

def afficher_theme(th):
    global theme
    canevas.delete(theme)
    theme=canevas.create_text(320,150,text=th,fill='black',font='Courrier 30')
    
def afficher_score(scor):
    global sc
    canevas.delete(sc)
    sc=canevas.create_text(35,20,text="Score: "+str(scor),fill='red',font='Courrier 12')
def init_jeu():
    global mot_choisi, mot_partiel, image_pendu, lettres,theme,sc
    global nb_echecs, partie_en_cours, liste_mots,nomE
    
    r = sr.Recognizer()
    nb_echecs = 0
    partie_en_cours = True
    L=liste_BD()
    rd.shuffle(L)
    aleat=rd.choice(L)
    mot_choisi =aleat[0]
    th=aleat[1]
    print(mot_choisi)
    mot_choisi = mot_choisi.upper()
    mot_partiel = "-" * len(mot_choisi)
    afficher_mot(mot_partiel)
    afficher_theme(th)
    scor=charger_score()
    afficher_score(scor)
    photo=PhotoImage(file="C:/Users/Hp/Desktop/projet intégré/pendu_0.gif")
    image_pendu.config(image=photo)
    image_pendu.image=photo
    
def liste_BD():

    
    DBfile = 'C:/Users/Hp/Desktop/projet intégré/mots.db'
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    
    SQL = 'SELECT * FROM Mots;'
    
    cursor.execute(SQL)
    L=cursor.fetchall()
    conn.close()
    return L
def charger_score():
   
    global nomE
    DBfile = 'C:/Users/Hp/Desktop/projet intégré/score.db'
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    
    SQL = 'SELECT score FROM ScoreT where user=? ;'
    
    cursor.execute(SQL,[nomE])
    L=cursor.fetchall()
    conn.close()
    return L[0][0]   
    
def set_score():  
    
    global nomE
    
    DBfile = 'C:/Users/Hp/Desktop/projet intégré/score.db'
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    
    SQL = 'UPDATE ScoreT SET score=score+1 where user=? ;'
    
    cursor.execute(SQL,[nomE])
    conn.commit()
    conn.close()
def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        text = r.recognize_google(audio,language='fr')
        lettre_dans_mot(text[-1]) 
        print(text)
# crÃ©ation du widget principal

fenetre =Tk()
fenetre.title("The War Of Words")

canevas = Canvas(fenetre, bg='white', height=650, width=600)
canevas.pack(side=BOTTOM)

bouton = [0]*26
for i in range(26):
    bouton[i] = Button(fenetre,text=chr(i+65),command=lambda x=i+65:lettre_dans_mot(chr(x)))
    bouton[i].pack(side=LEFT)

bouton2 = Button(fenetre,text='',command=fenetre.destroy)
bouton2.pack(side=RIGHT)
bouton1 = Button(fenetre,text='',command=init_jeu)
bouton1.pack(side=RIGHT)
bouton3 = Button(fenetre,text='',command=listen)
bouton3.pack(side=RIGHT)

photo=PhotoImage(file="C:/Users/Hp/Desktop/projet intégré/pendu_0.gif")
image_pendu = Label(canevas, image=photo, border=0)
image_pendu.place(x=50, y=220)
lettres = canevas.create_text(320,60,text="",fill='black',font='Courrier 30') 
theme=canevas.create_text(320,150,text="",fill='black',font='Courrier 30')
sc=canevas.create_text(35,20,text="",fill='red',font='Courrier 12')
voc=PhotoImage(file="C:/Users/Hp/Desktop/projet intégré/voc.gif")
bouton3.config(image=voc,compound=RIGHT)
bouton3.config(image=voc)
rec=PhotoImage(file="C:/Users/Hp/Desktop/projet intégré/rec.gif")
bouton1.config(image=voc,compound=RIGHT)
bouton1.config(image=rec)
ex=PhotoImage(file="C:/Users/Hp/Desktop/projet intégré/exit.gif")
bouton2.config(image=ex,compound=RIGHT)
bouton2.config(image=ex)
    


def jeux():
    
    ABOUT = ['AUTHORS: METRANE Abdelmounim , LABZAGUI Nassima , ','ETTAHI Yahya et MANDOR Loubna',
            'EMAIL : groupeG.GInfo@gmail.com','LIEU : Ecole Mohammedia Des Ingenieurs']
    INFO=['WAR OF WORDS est un jeu educatif qui a pour but de',' trouver le mot choisit (au hasard) en utilisant la commande',' vocale pour entrer une lettre(e.g: dire :la lettre A) qui va',' se placer automatiquement , si elle figure a son / ses',' emplacements existants.',' En cas de lettre n appartenant pas au mot, une chance va',' etre retranchee des 7 autres offertes (augmentation du niveau ','d eau) . Le jeu se termine lors de l epuisement des 7 chances.'," ",'########## A vos lettres , pret ? Partez !##########']        
    score=charger_score()
    Compte=["UTILISATEUR : "+str(nomE),PYGAMEMENU_TEXT_NEWLINE,"Votre Score est : "+str(score),PYGAMEMENU_TEXT_NEWLINE,]        
    COLOR_BACKGROUND = (155,136, 134)
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    Font=pygameMenu.fonts.FONT_ROSE
    MENU_BACKGROUND_COLOR =(155,136, 134)
    WINDOW_SIZE = (700, 600)
    
    # creation du Menu de jeu#
    
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('The War Of Words Menu')
    
    
    def initialisation():
        global fenetre,pygame
        pygame.quit()
        init_jeu()
        fenetre.mainloop()
        
    def main_background():
        fond = pygame.image.load("C:/Users/Hp/Desktop/pyprog/background.jpeg").convert()
        surface.blit(fond, (0,0))
    
    
    # -----------------------------------------------------------------------------
    # PLAY MENU
    play_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=Font,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    play_menu.add_option('Start',  initialisation)
    play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)
    
    
    # ABOUT MENU
    about_menu = pygameMenu.TextMenu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    font=Font,
                                    font_color=COLOR_BLACK,
                                    font_size_title=30,
                                font_title=pygameMenu.fonts.FONT_LEAD,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_color_title=COLOR_WHITE,
                                    menu_height=int(WINDOW_SIZE[1] * 0.7),
                                    menu_width=int(WINDOW_SIZE[0] * 0.7),
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
                                    option_shadow=False,
                                    text_color=COLOR_BLACK,
                                    text_fontsize=15,
                                    title='ABOUT',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
    for m in ABOUT:
        about_menu.add_line(m)
        about_menu.add_line(" ")
    about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
    about_menu.add_option('Return to menu', PYGAME_MENU_BACK)                                       
    # Info Menu
    info_menu = pygameMenu.TextMenu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    font=Font,
                                    font_color=COLOR_BLACK,
                                    font_size_title=30,
                                    font_title=pygameMenu.fonts.FONT_LEAD,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_color_title=COLOR_WHITE,
                                    menu_height=int(WINDOW_SIZE[1] * 0.8),
                                    menu_width=int(WINDOW_SIZE[0] * 0.9),
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
                                    option_shadow=False,
                                    text_color=COLOR_BLACK,
                                    text_fontsize=20,
                                    title='Info',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
    for m in INFO:
        info_menu.add_line(m)
    info_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
    info_menu.add_option('Return to menu', PYGAME_MENU_BACK)
    # Profile Menu
    compte_menu =  pygameMenu.TextMenu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    font=Font,
                                    font_color=COLOR_BLACK,
                                    font_size_title=30,
                                    font_title=pygameMenu.fonts.FONT_LEAD,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_color_title=COLOR_WHITE,
                                    menu_height=int(WINDOW_SIZE[1] * 0.5),
                                    menu_width=int(WINDOW_SIZE[0] * 0.5),
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
                                    option_shadow=False,
                                    text_color=COLOR_BLACK,
                                    text_fontsize=20,
                                    title='Votre compte',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
    for m in Compte:
        compte_menu.add_line(m)
    compte_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
    compte_menu.add_option('Return to menu',PYGAME_MENU_BACK)  
        
    # MAIN MENU
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=Font,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                title='Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.add_option('Play', play_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', PYGAME_MENU_EXIT)
    main_menu.add_option('Info',info_menu)
    main_menu.add_option('Compte',compte_menu)
    
    
    # -----------------------------------------------------------------------------
    # Main loop
    def main_loop():
        global fenetre
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    exit()
        
            
            main_menu.mainloop(events)
        
            
            pygame.display.flip()
    pygame.mixer.music.load("C:/Users/Hp/Desktop/pyprog/son1.wav")
    pygame.mixer.music.play()  
    pygame.mixer.music.set_volume(0.2)
    main_loop() 
    
#Creation de login
def check_user():
    global nomE,pnomE,roots
    import sqlite3
    
    DBfile = 'C:/Users/Hp/Desktop/projet intégré/score.db'
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    
    SQL = 'SELECT * FROM ScoreT;'
    c=0
    cursor.execute(SQL)
    L=cursor.fetchall()
    for enr in L:
        if enr[0]==nomE:
            c=1
            break
    if c==1: jeux()
    else:
       req='insert into ScoreT values(?,?);'
       cursor.execute(req,[nomE,0])
       conn.commit()
       jeux()   

class Ui_Dialog(object):
    def check_user(self):
        global nomE,pnom
        nomE=self.nomu_lineEdit.text()
        pnomE=self.pass_lineEdit_2.text()
        DBfile = 'C:/Users/Hp/Desktop/projet intégré/score.db'
        conn = sqlite3.connect(DBfile)
        cursor = conn.cursor()
        
        SQL = 'SELECT * FROM ScoreT;'
        c=0
        cursor.execute(SQL)
        L=cursor.fetchall()
        for enr in L:
            if enr[0]==nomE:
                if enr[1]!=pnomE:
                    _translate = QtCore.QCoreApplication.translate
                    self.mtpinc_label.setText(_translate("Dialog", "  Mot de pass incorrect"))
                    self.mtpinc_label.setStyleSheet("color:rgb(240, 0, 0)")
                    self.pass_lineEdit_2.clear()
                    c=-1
                else:
                    c=1    
                    break
        if c==1:
            _translate = QtCore.QCoreApplication.translate
            self.mtpinc_label.setText(_translate("Dialog", ""))
            jeux()
        elif c==0:
            conn = sqlite3.connect(DBfile)
            cursor = conn.cursor()
            req='insert into ScoreT values(?,?,?);'
            cursor.execute(req,[nomE,pnomE,0])
            conn.commit()
            _translate = QtCore.QCoreApplication.translate
            self.mtpinc_label.setText(_translate("Dialog", ""))
            jeux() 
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(517, 358)
        Dialog.setStyleSheet("background-color:qconicalgradient(cx:1, cy:0, angle:0, stop:0 rgba(254, 255, 173, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 382, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 96, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 175, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.check_pushButton = QtWidgets.QPushButton(Dialog)
        self.check_pushButton.setGeometry(QtCore.QRect(300, 270, 75, 41))
        self.check_pushButton.clicked.connect(self.check_user)
        self.Quit_pushButton = QtWidgets.QPushButton(Dialog)
        self.Quit_pushButton.setGeometry(QtCore.QRect(130, 270, 75, 41))
        self.Quit_pushButton.clicked.connect(QtGui.QGuiApplication.quit)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.check_pushButton.setFont(font)
        self.check_pushButton.setStyleSheet("background-color:qconicalgradient(cx:1, cy:0, angle:0, stop:0 rgba(254, 255, 173, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))")
        self.check_pushButton.setObjectName("check_pushButton")
        self.Quit_pushButton.setFont(font)
        self.Quit_pushButton.setStyleSheet("background-color:qconicalgradient(cx:1, cy:0, angle:0, stop:0 rgba(254, 255, 173, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))")
        self.Quit_pushButton.setObjectName("Quit_pushButton")
        self.nomu_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.nomu_lineEdit.setGeometry(QtCore.QRect(200, 100, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        font.setItalic(True)
        self.nomu_lineEdit.setFont(font)
        self.nomu_lineEdit.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.nomu_lineEdit.setObjectName("nomu_lineEdit")
        self.pass_lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.pass_lineEdit_2.setGeometry(QtCore.QRect(200, 180, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        font.setItalic(True)
        self.pass_lineEdit_2.setFont(font)
        self.pass_lineEdit_2.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pass_lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_lineEdit_2.setObjectName("pass_lineEdit_2")
        self.mtpinc_label = QtWidgets.QLabel(Dialog)
        self.mtpinc_label.setGeometry(QtCore.QRect(300, 220, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.mtpinc_label.setFont(font)
        self.mtpinc_label.setStyleSheet("color:rgb(195, 128, 21)")
        self.mtpinc_label.setWordWrap(False)
        self.mtpinc_label.setObjectName("mtpinc_label")
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.check_pushButton.raise_()
        self.pass_lineEdit_2.raise_()
        self.nomu_lineEdit.raise_()
        self.mtpinc_label.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "WOF login"))
        self.label.setText(_translate("Dialog", "Welcome to The War Of Words V1.0"))
        self.label_2.setText(_translate("Dialog", "Nom d\'utilisateur :"))
        self.label_3.setText(_translate("Dialog", "Mot de passe         :"))
        self.check_pushButton.setText(_translate("Dialog", "Check"))
        self.mtpinc_label.setText(_translate("Dialog", ""))
        self.Quit_pushButton.setText(_translate("Dialog", "Quit"))

if __name__ == "__main__":
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    nomE=ui.nomu_lineEdit.text()
    pnomE=ui.pass_lineEdit_2.text()