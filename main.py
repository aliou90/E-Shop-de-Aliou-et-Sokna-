#-------------------------------------------------------------
# Author      :   Aliou Mbengue  & Sokhna Ndioba Mbacké Faye
# -------------------------------------------------------------
from library import *
#----------------------------------------------------------------------------
#--INITIALISATION DE LA BASE DE DONNÉES
#----------------------------------------------------------------------------
from connexion import *
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
def login(event):
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
    close_alert['image'] = ss_ico
    
#----------------------------------------------------------------------------------
#-----------------------------FONCTIONS DES INSIGHTS
#---------------------------------------------------------------------------------
def insights_actualisation(event):
    #-----------------------------------------------------------------------------
    #----------REQUËTES VERS LA BASE DE DONNÉES
    #-----------------------------------------------------------------------------
    conn = sqlite3.connect ('shop.db')
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
    for x in table.get_children():
        table.delete(x)
    #Ajout de la barre de recherche
    search_label['text'] = 'Rechercher un client par '
    search_combo['values'] = ["Nom","Tél"]
    search_combo.current(0)
    search_entry.bind('<Return>', customers_search)
    
    #Ajout des entêtes
    table.heading(1, text = 'ID')
    table.heading(2, text = 'NOM COMPLET')
    table.heading(3, text = 'TÉLÉPHONE')
    table.heading(4, text = 'EMAIL')
    table.heading(5, text = '')
    #Ajout des colonnes
    table.column(1, width = 10)
    table.column(2, width = 200)
    table.column(3, width = 100)
    table.column(4, width = 100)

    #------------------------------------------------------------------------------------------------------------
    #----------AFFICHAGE DE LA LISTE  DES CLIENTS
    #-----------------------------------------------------------------------------------------------------------
    conn = sqlite3.connect ('shop.db')
    cur = conn.cursor()
    select = cur.execute("SELECT * FROM customers")
    for row_customers in select:
        table.insert('', END, value = row_customers)
    conn.close()
    
    #-----------Événement à la selection d'un enregistrement
    table.bind('<<TreeviewSelect>>', customers_view)

def customers_view(event):
    details_label['text'] = ''
    idSelect = table.item(table.selection())['values'][0]
    nameSelect = table.item(table.selection())['values'][1]
    phoneSelect = table.item(table.selection())['values'][2]
    emailSelect = table.item(table.selection())['values'][3]
    imgProfile = "files/img/customers/profile_" + str(idSelect) + "." + "jpg"
    load = Image.open(imgProfile)
    load.thumbnail((100, 100))
    sphoto = ImageTk.PhotoImage(load)    
    profile[1] = sphoto
    lblImage['image'] = sphoto
    lblImage.place(x=700, y=490, width =100, height =100 )
    lab1['text'] = "NOM COMPLET :  " + str(nameSelect)
    lab1.place(x=800, y=500)
    lab2['text'] = "TÉLÉPHONE :  " + str(phoneSelect)
    lab2.place(x=800, y=520)
    lab3['text'] = "EMAIL :  " + str(emailSelect)
    lab3.place(x=800, y=540)
    lab4['text'] = ""
    btn_update_button['text'] = 'Modifier'
    btn_update_button['command'] = customers_confirm_update
    btn_update_button.place(x=805, y=565)
    btn_delete_button['text'] ='Supprimer'
    btn_delete_button['command'] = customers_confirm_delete
    btn_delete_button.place(x=875, y=565)
    
def customers_confirm_delete():
    nameSelect = table.item(table.selection())['values'][1]
    lab1['text'] = "Supprimer le client \n {0} ?".format(nameSelect)
    lab2['text'] = ''
    lab3['text'] = ''
    lab1['font'] =('Times new roman', 12) 
    btn_delete_button['text'] = "Confirmer"
    btn_delete_button['command'] = customers_delete
    btn_update_button['text'] ="Annuler"
    btn_update_button['command'] = customers_cancel

def customers_delete():
    idSelect = table.item(table.selection())['values'][0]
    nameSelect = table.item(table.selection())['values'][1]
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()
    delete = cur.execute("DELETE FROM customers WHERE id = {} ".format(idSelect))
    conn.commit()
    conn.close()
    imgProfile = "files/img/customers/profile_" + str(idSelect) + "." + "jpg"
    os.remove(imgProfile)
    table.delete(table.selection())
    alert_msg['text'] = "Dernière action : Le client " + str(nameSelect) + " a été supprimé..."
    alert_msg['bg'] = bg_success
    close_alert['image'] = close_ico
    print("\a")
    lblImage['image'] = ''
    lab1['text'] =''
    lab2['text'] =''
    lab3['text'] =''
    lab4['text'] =''
    lab5['text'] =''
    btn_update_button['text'] =''
    btn_update_button['command'] =''
    btn_delete_button['text'] =''
    btn_delete_button['command'] =''
def customers_cancel():
    lab1['text'] = "NOM COMPLET :  " + str(table.item(table.selection())['values'][1] )
    lab2['text'] = "TÉLÉPHONE :  " + str(table.item(table.selection())['values'][2])
    lab3['text'] = "EMAIL :  " + str(table.item(table.selection())['values'][3])
    btn_delete_button['text'] ='Supprimer'
    btn_delete_button['command'] = customers_confirm_delete
    btn_update_button['text'] ='Modifier'
    
def customers_confirm_update():
    ...

def customers_search(event):
    if search_combo.get() == 'Nom':
        for x in table.get_children():
            table.delete(x)
        name = search_entry.get()
        conn = sqlite3.connect('shop.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM customers WHERE name = (?)', (name,))
        conn.commit()
        for row in select:
            table.insert('', END, values = row)
        conn.close()
    if search_combo.get() == 'Tél':
        for x in table.get_children():
            table.delete(x)
        phone = search_entry.get()
        conn = sqlite3.connect('shop.db')
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
    for x in table.get_children():
        table.delete(x)
    #Ajout des entêtes
    search_label['text'] = 'Rechercher un produit par '
    search_combo['values'] = ["Nom","Gamme"]
    search_combo.current(0)
    search_entry.bind('<Return>', products_search)
    table.heading(1, text = 'ID')
    table.heading(2, text = 'NOM PRODUIT')
    table.heading(3, text = 'GAMME D\'APPARTENANCE')
    table.heading(4, text = 'PRIX')
    table.heading(5, text = 'DATE DE STOCK')
    #Ajout des colonnes
    table.column(1, width = 10)
    table.column(2, width = 130)
    table.column(3, width = 130)
    table.column(4, width = 50)
    table.column(5, width = 120)
    #AFFICHAGE DE LA LISTE  DES CLIENTS
    conn = sqlite3.connect ('shop.db')
    cur = conn.cursor()
    select = cur.execute("SELECT * FROM products")
    for row_products in select:
        table.insert('', END, value = row_products)
    conn.close()
    #-----------Événement à la selection d'un enregistrement
    table.bind('<<TreeviewSelect>>', products_view)


def products_view(event):
    details_label['text'] = ''
    name = table.item(table.selection())['values'][1]
    range = table.item(table.selection())['values'][2]
    cost = table.item(table.selection())['values'][3]
    imgProfile = "files/img/products/product-ico.png"
    load = Image.open(imgProfile)
    load.thumbnail((100, 100))
    sphoto = ImageTk.PhotoImage(load)    
    profile[1] = sphoto
    lblImage['image'] = sphoto
    lblImage.place(x=700, y=490, width =100, height =100 )
    lab1['text'] = "NOM PRODUIT:  " + str(name)
    lab1.place(x=800, y=500)
    lab2['text'] = "GAMME:  " + str(range)
    lab2.place(x=800, y=520)
    lab3['text'] = "PRIX PAR UNITÉ :  " + str(cost)
    lab3.place(x=800, y=540)
    btn_update_button['text'] = 'Modifier'
    btn_update_button['command'] = products_confirm_update
    btn_update_button.place(x=805, y=565)
    btn_delete_button['text'] ='Supprimer'
    btn_delete_button['command'] = products_confirm_delete
    btn_delete_button.place(x=875, y=565)

def products_confirm_delete():
    lab1['text'] =''
    lab2['text'] =''
    lab3['text'] =''
    lab4['text'] =''
    lab5['text'] =''
    btn_delete_button['text'] = ""
    btn_update_button['text'] =""
    nameSelect = table.item(table.selection())['values'][1]
    units = table.item(table.selection())['values'][4]
    lab1['text'] = "Supprimer le produit {0} ?".format(nameSelect)
    lab1['font'] = ('Times new roman', 12) 
    btn_delete_button['text'] = "Confirmer"
    btn_delete_button['command'] = products_delete
    btn_delete_button.place(x=875, y=565)
    btn_update_button['text'] ="Annuler"
    btn_update_button['command'] = products_cancel
    btn_update_button.place(x=805, y=565)

def products_delete():
    idSelect = table.item(table.selection())['values'][0]
    nameSelect = table.item(table.selection())['values'][1]
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()
    delete = cur.execute("DELETE FROM products WHERE id_product = {} ".format(idSelect))
    conn.commit()
    conn.close()
    #imgProfile = "files/img/products/profile_" + str(idSelect) + "." + "jpg"
    #os.remove(imgProfile)
    table.delete(table.selection())
    alert_msg['text'] = "Dernière action : Le produit " + str(nameSelect) + " a été supprimé..."
    alert_msg['bg'] = bg_success
    close_alert['image'] = close_ico
    print("\a")
    lblImage['image'] = ''
    lab1['text'] =''
    lab2['text'] =''
    lab3['text'] =''
    lab4['text'] =''
    lab5['text'] =''
    btn_update_button['text'] =''
    btn_update_button['command'] =''
    btn_delete_button['text'] =''
    btn_delete_button['command'] =''
def products_cancel():
    lab1['text'] = "NOM PRODUIT:  " + str(table.item(table.selection())['values'][1])
    lab2['text'] ="GAMME:  " + str(table.item(table.selection())['values'][2])
    lab3['text'] ="PRIX:  " + str(table.item(table.selection())['values'][3])
    lab4['text'] =''
    lab5['text'] =''
    btn_delete_button['text'] = "Supprimer"
    btn_delete_button['command'] = products_confirm_delete
    btn_update_button['text'] ="Modifier"
def products_confirm_update():
    ...

def products_search(event):
    table.heading(1, text = 'ID')
    table.heading(2, text = 'NOM PRODUIT')
    table.heading(3, text = 'GAMME D\'APPARTENANCE')
    table.heading(4, text = 'UNITÉS')
    table.heading(5, text = 'DATE DE STOCK')
    
    #Ajout des colonnes
    table.column(1, width = 10)
    table.column(2, width = 150)
    table.column(3, width = 150)
    table.column(4, width = 50)
    table.column(5, width = 150)
    #-------RECHERCHER PRODUIT PAR NOM
    if search_combo.get() == 'Nom':
        for x in table.get_children():
            table.delete(x)
        name = search_entry.get()
        conn = sqlite3.connect('shop.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM products WHERE name_product = (?)', (name,))
        conn.commit()
        for row in select:
            table.insert('', END, values = row)
        conn.close()
    #-------RECHERCHER PRODUIT PAR GAMME
    if search_combo.get() == 'Gamme':
        for x in table.get_children():
            table.delete(x)
        gamme = search_entry.get()
        conn = sqlite3.connect('shop.db')
        cur = conn.cursor()
        select = cur.execute('SELECT * FROM products WHERE name_range = (?)', (gamme,))
        conn.commit()
        for row in select:
            table.insert('', END, values = row)
        conn.close()
        
        
#-----------------------------------------------------------------------------------------------
#-------------FONCTONS DES COMMANDES
#----------------------------------------------------------------------------------------------
def orders_display():
    ...


def add_product():
    print("fonction calcul ", 3 * 4)

def add_range() :
    global nb
    nb += 1
    b = tk.Button (text = "bouton " + str (nb))
    b.pack()

def add_order():
    ...

#-------------------------------------------------------------------------------
#-------------------------------FENËTRE INITIAL
#--------------------------------------------------------------------------------
root = tk.Tk() 
root.title("Gestion de boutique")
root.geometry("1200x600")
root.resizable(False,False )
        
#================================================================================
#-----------------------------------ICÖNE ET COUVERTURE-----------------------
#================================================================================
ss_img = 'files/img/icones/logo.png'
ss_load = Image.open(ss_img)
ss_load.thumbnail((20, 20))
ss_ico = ImageTk.PhotoImage(ss_load) 

ico = PhotoImage(file = 'files/img/icones/logo.png') 
root.iconphoto(False, ss_ico)

#-----Photo de couverture
n = 4
cover=PhotoImage(file='files/img/covers/cover{0}.png'.format(n))

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
sub_menu3 = tk.Menu(root)

my_menu.add_cascade (label = "Administration", menu = sub_menu1)
my_menu.add_cascade (label = "Gestion des produits", menu = sub_menu2)
my_menu.add_cascade (label = "Gestion des commandes", menu = sub_menu3)

nb = 0


sub_menu1.add_command (label = "Se déconnecter", command = root.destroy)

sub_menu2.add_command (label = "Ajouter un produit", command = add_product)
sub_menu2.add_command (label = "Ajouter une gamme", command = add_range )
sub_menu3.add_command (label = "Nouvelle commande", command = add_order)

#================================================================================
#-----------------------------------BARE D'ALERT'-------------------------------
#================================================================================
alert_msg = tk.Label(root, text="...", font = ("Times new roman" , 16),anchor='w')
alert_msg.place(x=0,y=45,width = 700)
close_img ='files/img/icones/del.png'
close_load = Image.open(close_img)
close_load.thumbnail((20, 20))
close_ico = ImageTk.PhotoImage(close_load)
close_alert = tk.Button(root, image = close_ico, width = 20, height = 20,bg = 'white', command = alert_close)
close_alert.place(x=677,y=45)
#-----------------------------------------------------------------------------------
#---------------------------------CONTENEUR GAUCHE----------------------------------
#-----------------------------------------------------------------------------------
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
products_head = tk.Button(root, text="Listes des clients", font = ("Times new roman", 12),border=5,bg='blueviolet',fg='white',command=customers_display)
products_head.place(x=705, y=45, width = 175)
customers_head = tk.Button(root, text="Listes des produits", font = ("Times new roman", 12),border=5,bg='blueviolet',fg='white', command=products_display)
customers_head.place(x=880, y=45, width = 155)
orders_head = tk.Button(root, text="Listes des commandes", font = ("Times new roman", 12),border=5,bg='blueviolet',fg='white',command=orders_display)
orders_head.place(x=1035, y=45, width = 165)

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
table = ttk.Treeview(root, columns = (1,2,3,4,5), height = 5, show = "headings" )
table.place(x = 705, y = 100, width = 500, height = 390)



#------------------------------------------------------------------------------------------------------------
#-------------------------------------AFFICHAGE PAR DÉFAUT DES DÉTAILS DES CLIENTS
#-----------------------------------------------------------------------------------------------------------
#------Message par défaut
details_label = tk.Label(root, text="Sélectionnez un produit ou un client pour afficher les détails",bg="black", fg="white", border=2)
details_label.place(x = 800, y = 520)
#------Déclaration de widgets d'affichage
lblImage = Label(root)
lab1 = tk.Label(root, bg="black", fg="white")
lab2 = tk.Label(root, bg="black", fg="white")
lab3 = tk.Label(root,bg="black", fg="white")
lab4 = tk.Label(root,bg="black", fg="white", anchor='w')
lab5 = tk.Label(root,bg="black", fg="white", anchor='w')
btn_update_button = Button(root,bg="yellow")
btn_delete_button = Button(root,bg="red")


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

#------ÉVÉNEMENT D'ACTUALISATION DES INSIGHTS
root.bind('<Enter>', insights_actualisation)

#-------------------------------------------------------------------------------------------------
#--------FORMULAIRE DE CONNEXION------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
connexion_label=tk.Label(root, text="Entrez votre mot de passe \n svp",font=("Roboto" ,  18))
connexion_label.place(x=0,y=40, width=1200,height=570)
connexion_entry=tk.Entry(root, font=("Roboto" ,  15) )
connexion_entry.bind('<Return>', login)
connexion_entry.place(x=500,y=370, width=200)
connexion_msg = tk.Label(root)
connexion_msg.place(x=450,y=420, width=300,height=50)


    
    
root.mainloop() 


 