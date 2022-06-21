#--------------------------------------
# Author      :   Aliou Mbengue
# ------------------------------------
# -*- coding: utf-8 -*-
from cProfile import label
from fileinput import filename
import profile
import tkinter as tk
from tkinter import *
from tkinter import ttk

from tkinter import filedialog 
import os

from PIL import Image, ImageTk
import sqlite3

from matplotlib import image, style



#----------------------------------------------------------------------------
#--VARIABLES GLOBALES POUR LES FONCTIONS
#----------------------------------------------------------------------------
#---Dictionnaire des noms de profile
profile = {1: ''}
bg_success = "greenyellow"
bg_fail = "red"
bg_primary = "white"
cover_x = 0
cover_y = 70
cover_w = 700
cover_h = 420
#----------------------------------------------------------------------------------
#-----------------------------FONCTIONS DE CONNEXION
#---------------------------------------------------------------------------------
def connexion(event):
    if connexion_entry.get() == "ss2022":
        connexion_msg.destroy()
        connexion_entry.destroy()
        connexion_label.destroy()
        root.config(menu = my_menu, width = 200)
        ok = "Bienvenue dans votre boutique.... !"
        alert_msg['text'] = ok
        alert_msg['bg'] = bg_success
    else:
        root.bell()
        nook = "Mot de passe incorecte"
        connexion_msg['text'] = nook
        

#----------------------------------------------------------------------------------
#-----------------------------FONCTIONS DE LA BARRE D'ALERTE
#---------------------------------------------------------------------------------
def alert_close():
    alert_msg['text'] = ''
    alert_msg['bg'] = bg_primary  
    close_alert['command'] = None
    close_alert['image'] = clean_ico
    
#----------------------------------------------------------------------------------
#-----------------------------FONCTIONS DES INSIGHTS
#---------------------------------------------------------------------------------
def insights_actualisation(event):
    #-----------------------------------------------------------------------------
    #----------REQUËTES VERS LA BASE DE DONNÉES
    #-----------------------------------------------------------------------------
    conn = sqlite3.connect ('database.db')
    cur = conn.cursor()
    select_all_ranges = cur.execute("SELECT * FROM ranges")
    nb_ranges = 0
    nb_products = 0
    nb_customers = 0
    for row_ranges in select_all_ranges:
        nb_ranges += 1
    cur = conn.cursor()
    select_all_products = cur.execute("SELECT * FROM products")

    for row_products in select_all_products:
        nb_products += 1
    cur = conn.cursor()
    select_all_customers = cur.execute("SELECT * FROM customers")
    for row_customers in select_all_customers:
        nb_customers += 1

    insight_ranges_label['text'] = "Total Gammes :  " 
    insight_ranges_info['text'] = nb_ranges
    insight_products_label['text'] = "Total Produits :  "
    insight_products_info['text'] = nb_products
    insight_customers_label['text'] = "Total Clients :  "
    insight_customers_info['text'] = nb_customers
    

#----------------------------------------------------------------------------------
#-----------------------------FONCTIONS DES CLIENTS
#---------------------------------------------------------------------------------
def customers_display():
    #----Vider le tableau
    for x in customers.get_children():
        customers.delete(x)
    #Ajout de la barre de recherche
    search_label['text'] = 'Rechercher un client par '
    search_combo['values'] = ["Nom","Tél"]
    search_combo.current(0)
    search_entry.bind('<Return>', customers_search)
    
    #Ajout des entêtes
    customers.heading(1, text = 'ID')
    customers.heading(2, text = 'NOM COMPLET')
    customers.heading(3, text = 'TÉLÉPHONE')
    customers.heading(4, text = '')
    customers.heading(5, text = '')
    #Ajout des colonnes
    customers.column(1, width = 10)
    customers.column(2, width = 300)
    customers.column(3, width = 200)

    #------------------------------------------------------------------------------------------------------------
    #----------AFFICHAGE DE LA LISTE  DES CLIENTS
    #-----------------------------------------------------------------------------------------------------------
    conn = sqlite3.connect ('database.db')
    cur = conn.cursor()
    select = cur.execute("SELECT * FROM customers")
    for row_customers in select:
        customers.insert('', END, value = row_customers)
    conn.close()
    
    #-----------Événement à la selection d'un enregistrement
    customers.bind('<<TreeviewSelect>>', customers_view)

def customers_view(event):
    details_label.destroy()
    idSelect = customers.item(customers.selection())['values'][0]
    nameSelect = customers.item(customers.selection())['values'][1]
    phoneSelect = customers.item(customers.selection())['values'][2]
    moreSelect = customers.item(customers.selection())['values'][3]
    imgProfile = "files/img/customers/profile_" + str(idSelect) + "." + "jpg"
    load = Image.open(imgProfile)
    load.thumbnail((100, 100))
    sphoto = ImageTk.PhotoImage(load)    
    profile[1] = sphoto
    lblImage = Label(root, image = sphoto)
    lblImage.place(x=700, y=490, width =100, height =100 )
    lid['text'] = "L'ID :  " + str(idSelect)
    lid.place(x=800, y=500)
    lname['text'] = "NOM COMPLET :  " + str(nameSelect)
    lname.place(x=800, y=520)
    lphone['text'] = "TÉLÉPHONE :  " + str(phoneSelect)
    lphone.place(x=800, y=540)
    Tmore.insert(END, "Plus d'infos :  \n" + str (moreSelect))
    Tmore.place(x=1000, y=490, width=200, height = 100)
    Tmore.configure(state='disabled')
    customer_update_button['text'] = 'Modifier'
    customer_update_button['command'] = customers_confirm_update
    customer_update_button.place(x=805, y=565)
    customers_delete_button['text'] ='Supprimer'
    customers_delete_button['command'] = customers_confirm_delete
    customers_delete_button.place(x=875, y=565)
    
def customers_confirm_delete():
    top = Toplevel(root)
    top.geometry("300x100")
    nameSelect = customers.item(customers.selection())['values'][1]
    confirm_label =tk.Label(top, text="Vous êtes sur le point de supprimer le client \n {0} ".format(nameSelect), font =('Times new roman', 12) )
    confirm_label.pack()
    btn_delete = tk.Button(top, text="Confirmer", bg= "red", fg="black", border = 5 ,command = customers_delete)
    btn_delete.place(x=50,y=50, width=100)
    btn_cancel = tk.Button(top, text="Annuler", bg= "white", fg="black", border = 5, command = top.destroy)
    btn_cancel.place(x=150,y=50, width=100)

def customers_delete():
    idSelect = customers.item(customers.selection())['values'][0]
    nameSelect = customers.item(customers.selection())['values'][1]
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    delete = cur.execute("DELETE FROM customers WHERE id = {} ".format(idSelect))
    conn.commit()
    conn.close()
    imgProfile = "files/img/customers/profile_" + str(idSelect) + "." + "jpg"
    os.remove(imgProfile)
    customers.delete(customers.selection())
    alert_msg['text'] = "Dernière action : Le client " + str(nameSelect) + " a été supprimé..."
    alert_msg['bg'] = bg_success
    close_alert['image'] = close_ico
    print("\a")

def customers_confirm_update():
    ...

def customers_search(event):
    if search_combo.get() == 'Nom':
        for x in customers.get_children():
            customers.delete(x)
        name = search_entry.get()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM customers WHERE name = (?)', (name,))
        conn.commit()
        for row in select:
            customers.insert('', END, values = row)
        conn.close()
    if search_combo.get() == 'Tél':
        for x in customers.get_children():
            customers.delete(x)
        phone = search_entry.get()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM customers WHERE phone = (?)', (phone,))
        conn.commit()
        print(select)
        for row in select:
            customers.insert('', END, values = row)
        conn.close()


#----------------------------------------------------------------------------------
#-----------------------------FONCTIONS DES PRODUITS
#---------------------------------------------------------------------------------
def products_display():
    #----Vider le tableau
    for x in customers.get_children():
        customers.delete(x)
    #Ajout des entêtes
    search_label['text'] = 'Rechercher un produit par '
    search_combo['values'] = ["Nom","Gamme"]
    search_combo.current(0)
    search_entry.bind('<Return>', products_search)
    customers.heading(1, text = 'ID')
    customers.heading(2, text = 'NOM PRODUIT')
    customers.heading(3, text = 'GAMME D\'APPARTENANCE')
    customers.heading(4, text = 'UNITÉS')
    customers.heading(5, text = 'DATE DE STOCK')
    #Ajout des colonnes
    customers.column(1, width = 10)
    customers.column(2, width = 150)
    customers.column(3, width = 150)
    customers.column(4, width = 50)
    customers.column(5, width = 150)
    #AFFICHAGE DE LA LISTE  DES CLIENTS
    conn = sqlite3.connect ('database.db')
    cur = conn.cursor()
    select = cur.execute("SELECT * FROM products")
    for row_products in select:
        customers.insert('', END, value = row_products)
    conn.close()
    #-----------Événement à la selection d'un enregistrement
    customers.bind('<<TreeviewSelect>>', products_view)


def products_view(event):
    details_label.destroy()
    name = customers.item(customers.selection())['values'][1]
    range = customers.item(customers.selection())['values'][2]
    cost = customers.item(customers.selection())['values'][3]
    units = customers.item(customers.selection())['values'][4]
    last_up = customers.item(customers.selection())['values'][5]
    imgProfile = "files/img/products/product-ico.png"
    load = Image.open(imgProfile)
    load.thumbnail((100, 100))
    sphoto = ImageTk.PhotoImage(load)    
    profile[1] = sphoto
    lblImage = Label(root, image = sphoto)
    lblImage.place(x=700, y=490, width =100, height =100 )
    lid['text'] = "NOM PRODUIT:  " + str(name)
    lid.place(x=800, y=500)
    lname['text'] = " GAMME:  " + str(range)
    lname.place(x=800, y=520)
    lphone['text'] = "PRIX :  " + str(cost)
    lphone.place(x=800, y=540)
    Tmore.insert(END, "Prix du produit :" + str (cost) + "\nDate du dernier stock : \n" +str (last_up) )
    Tmore.place(x=1000, y=490, width=200, height = 100)
    Tmore.configure(state='disabled')
    customer_update_button['text'] = 'Modifier'
    customer_update_button['command'] = products_confirm_update
    customer_update_button.place(x=805, y=565)
    customers_delete_button['text'] ='Supprimer'
    customers_delete_button['command'] = products_confirm_delete
    customers_delete_button.place(x=875, y=565)

def products_confirm_delete():
    ...

def products_confirm_update():
    ...

def products_search(event):
    customers.heading(1, text = 'ID')
    customers.heading(2, text = 'NOM PRODUIT')
    customers.heading(3, text = 'GAMME D\'APPARTENANCE')
    customers.heading(4, text = 'UNITÉS')
    customers.heading(5, text = 'DATE DE STOCK')
    
    #Ajout des colonnes
    customers.column(1, width = 10)
    customers.column(2, width = 150)
    customers.column(3, width = 150)
    customers.column(4, width = 50)
    customers.column(5, width = 150)
    #-------RECHERCHER PRODUIT PAR NOM
    if search_combo.get() == 'Nom':
        for x in customers.get_children():
            customers.delete(x)
        name = search_entry.get()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM products WHERE name_product = (?)', (name,))
        conn.commit()
        for row in select:
            customers.insert('', END, values = row)
        conn.close()
    #-------RECHERCHER PRODUIT PAR GAMME
    if search_combo.get() == 'Gamme':
        for x in customers.get_children():
            customers.delete(x)
        gamme = search_entry.get()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM products WHERE name_range = (?)', (gamme,))
        conn.commit()
        for row in select:
            customers.insert('', END, values = row)
        conn.close()    

def affiche():
    print("fonction affiche")

def calcul():
    print("fonction calcul ", 3 * 4)

def ajoute_bouton () :
    global nb
    nb += 1
    b = tk.Button (text = "bouton " + str (nb))
    b.pack()



#-------------------------------------------------------------------------------
#-------------------------------FENËTRE INITIAL
#--------------------------------------------------------------------------------
root = tk.Tk() 
root.title("Gestion de boutique")
root.geometry("1200x600")
root.resizable(False,False )
        
#================================================================================
#-----------------------------------ICÖNE------------------------------------------------------------------
#================================================================================
ico = PhotoImage(file = 'files/img/icones/logo.png') 
root.iconphoto(False, ico)
#================================================================================
#-----------------------------------ENTËTE------------------------------------------------------------------
#================================================================================
lab_head = tk.Label(root ,text="Sama Shop", width = 1200,bd=9,relief=GROOVE,font=("Wide latin",16,"bold"),bg="white", fg = "blue").pack()
#---------------------------------------------------------------------------------------
#---BARE DE NAVIGATION
#---------------------------------------------------------------------------------------
my_menu = tk.Menu(root)
sub_menu1 = tk.Menu(root)
sub_menu2 = tk.Menu(root)

my_menu.add_cascade (label = "Administration", menu = sub_menu1)
my_menu.add_cascade (label = "Gestion des produits", menu = sub_menu2)

nb = 0

sub_menu1.add_command (label = "Changer mot de passe", command = affiche)
sub_menu1.add_command (label = "Se déconnecter", command = root.destroy)
sub_menu2.add_command (label = "Vendre produit", command = calcul )
sub_menu2.add_command (label = "Ajouter produit", command = ajoute_bouton)
sub_menu2.add_command (label = "Voir mes clients", command = ajoute_bouton)

#================================================================================
#-----------------------------------BARE D'ALERT'-------------------------------
#================================================================================
alert_msg = tk.Label(root, text="...", font = ("Times new roman" , 16),anchor='w')
alert_msg.place(x=0,y=45,width = 700)
clean_img = 'files/img/icones/ss-logo3.png'
close_img ='files/img/icones/del.png'
close_load = Image.open(close_img)
clean_load = Image.open(clean_img)
close_load.thumbnail((20, 20))
clean_load.thumbnail((20, 20))
close_ico = ImageTk.PhotoImage(close_load)
clean_ico = ImageTk.PhotoImage(clean_load) 
close_alert = tk.Button(root, image = close_ico, width = 20, height = 20,bg = 'white', command = alert_close)
close_alert.place(x=677,y=45)
#-----------------------------------------------------------------------------------
#---------------------------------CONTENEUR GAUCHE----------------------------------
#-----------------------------------------------------------------------------------
cover=PhotoImage(file='files/img/covers/ss-cover2.png')
lab_left = tk.Label(root,image=cover, bg="white")
lab_left.place(x=cover_x,y=cover_y, width = cover_w, height = cover_h)
#-----------------------------------------------------------------------------------
#---------------------------------CONTENEUR DROITE----------------------------------
#-----------------------------------------------------------------------------------
lab_right = tk.Label(root, bg="black")
lab_right.place(x=705,y=70, width = 500,height = 525)

#--------------------------------------------------------------------------------------
#-------------------------------BOUTONS LISTE DES PRODUITS ET DES CLIENTS--------------
#-------------------------------------------------------------------------------------
customers_head = tk.Button(root, text="Listes des produits", font = ("Times new roman", 12),border=5,bg='blueviolet',fg='white', command=products_display)
customers_head.place(x=705, y=45, width = 250)
products_head = tk.Button(root, text="Listes des clients", font = ("Times new roman", 12),border=5,bg='blueviolet',fg='white',command=customers_display)
products_head.place(x=955, y=45, width = 250)

#------------------------------------------------------------------------------------------------
#----------------------------------BARE DE RECHERCHE---------------------------------------------
#------------------------------------------------------------------------------------------------
search_label = tk.Label(root, font = ("Times new roman" ,  11), bg="white", fg="black")
search_label.place(x=706,y=75, width = 160,height = 25)
search_combo = ttk.Combobox(root)
search_combo.place(x=865, y=75, width = 85, height = 25)
search_entry = tk.Entry(root, font = ("Arial" ,  10))
search_entry.place(x=950, y=75, width = 355, height = 25)


#------------------------------------------------------------------------------------------------------------
#-------------------------------------CRÉATION DU TABLEAU D'AFFICHAGE DES CLIENTS
#-----------------------------------------------------------------------------------------------------------
customers = ttk.Treeview(root, columns = (1,2,3,4,5), height = 5, show = "headings" )
customers.place(x = 705, y = 100, width = 500, height = 390)



#------------------------------------------------------------------------------------------------------------
#-------------------------------------AFFICHAGE PAR DÉFAUT DES DÉTAILS DES CLIENTS
#-----------------------------------------------------------------------------------------------------------
#------Message par défaut
details_label = tk.Label(root, text="Sélectionnez un produit ou un client pour afficher les détails",bg="black", fg="white", border=2)
details_label.place(x = 800, y = 520)
#------Déclaration de widgets d'affichage
lid = Label(root, bg="black", fg="white")
lname = Label(root, bg="black", fg="white")
lphone = Label(root,bg="black", fg="white")
Tmore = Text(root)
customer_update_button = Button(root,bg="yellow")
customers_delete_button = Button(root,bg="red")

#------------------------------------------------------------------------------------------------------------
#-------------------------------------AFFICHAGE DES INSIGHTS
#-----------------------------------------------------------------------------------------------------------
insight_cover = tk.Label(root, text="",bg="black", fg="white", border=2)
insight_cover.place(x =0, y = 490, width = 700,height = 105)
insight_header = tk.Label (root, text= "Insights de ce mois ci ",bd=9,relief=GROOVE,font=("times new roman",16,"bold"),bg="white",fg="green")
insight_header.place(x=0, y=480,width=700)
#------------NOMBRE DE GAMMES
insight_ranges_label = tk.Label(root, text = "Total Gammes :  ",bg="black", fg="white",anchor='w')
insight_ranges_label.place(x=0, y=530)
insight_ranges_info = tk.Label(root, text = "Par defaut 0", font = ('Arial', 14,'bold'),bg="black", fg="white",anchor='w')
insight_ranges_info.place(x=100, y=525)
#------------NOMBRE DE PRODUITS
insight_products_label =tk.Label(root, text = "Total Produits :  ",bg="black", fg="white",anchor='w')
insight_products_label.place(x=0, y=550)
insight_products_info = tk.Label(root, text = "Par defaut 0", font = ('Arial', 14,'bold'),bg="black", fg="white",anchor='w')
insight_products_info.place(x=100, y=545)
#------------NOMBRE DE CLIENTS
insight_customers_label =tk.Label(root, text = "Total Clients :  ",bg="black", fg="white",anchor='w')
insight_customers_label.place(x=0, y=570)
insight_customers_info = tk.Label(root, text = "Par defaut 0", font = ('Arial', 14,'bold'),bg="black", fg="white",anchor='w')
insight_customers_info.place(x=100, y=565)

insight_best_ranges = tk.Label(root, text = "Gamme du mois :  ",bg="black", fg="white",anchor='w')
insight_best_ranges.place(x=400, y=530)
insight_best_products =tk.Label(root, text = "Produit du mois :  ",bg="black", fg="white",anchor='w')
insight_best_products.place(x=400, y=550)
insight_best_customers =tk.Label(root, text = "Client du mois :  ",bg="black", fg="white",anchor='w')
insight_best_customers.place(x=400, y=570)


root.bind('<Enter>', insights_actualisation)

#-------------------------------------------------------------------------------------------------
#--------FORMULAIRE DE CONNEXION------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
connexion_label=tk.Label(root, text="Entrez votre mot de passe \n svp",font=("Roboto" ,  18))
connexion_label.place(x=0,y=40, width=1200,height=570)
connexion_entry=tk.Entry(root, font=("Roboto" ,  15) )
connexion_entry.bind('<Return>', connexion)
connexion_entry.place(x=500,y=370, width=200)
connexion_msg = tk.Label(root)
connexion_msg.place(x=450,y=420, width=300,height=50)


    
    
root.mainloop() 


 