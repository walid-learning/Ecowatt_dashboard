from tkinter import *
from tkinter import ttk
from database import Database
import sys
import os
import time
sys.path.append( os.path.dirname(os.path.abspath(__file__))[:-3] + "\\cfg")
from config import PATH, info, warning, debug, log_config
import webbrowser
DB = Database(host='localhost', user='root', database='ecowatt', auth_plugin='mysql_native_password')

log_config("Application")


class Application:
    def __init__(self):

        self.appli=Tk()
        self.appli.title("Gestion de la consommation d'énergie")
        self.appli.minsize(480,360)
        self.appli.geometry("720x480")
        self.appli.config(background = '#fff3e3')    

        self.frame = Frame (self.appli,  bg ='#c8ffab')          # Frame principale
        self.frame_connection = Frame (self.appli, bg ='#c8ffab')     # Frame secondaire
        self.frame_query = Frame (self.appli, bg ='#2D13ED')     # Frame secondaire
        self.frame_option = Frame(self.appli, bg='#c8ffab')      # frame options
        self.frame_consommation = Frame(self.appli, bg='#2D13ED')      # frame consommation


    def help(self):
        webbrowser.open('https://github.com/anesnabti/Database_Exploitation') 


    def show(self):
        p = password.get() #get password from entry
        return p


    def have_frame(self, old_frame, new_frame):
        old_frame.destroy()
        new_frame.pack(expand = YES)


    def display_connection(self, passwd):
        result = DB.connect(passwd)
        text = Text(self.frame_connection, height=10, width=30)
        text.grid(pady=25)
        if result[1] is False:
            debug('Mot de passe incorrecte')
            text.insert(END, result[0])
        if result[1] is True:
            text.insert(END, result[0])
            time.sleep(2)
            self.have_frame(self.frame_connection, self.frame_option)

    def menu(self):
        info('Instanciation du menu')
        menu_bar = Menu (self.appli)
        file_menu = Menu (menu_bar, tearoff = 0)
        file_menu.add_command (label = "A propos", command = self.help)            # Help
        file_menu.add_command(label = "Quitter", command = self.appli.destroy)    # Quitter
        menu_bar.add_cascade(label = "Paramètres",menu = file_menu)    # ajouter le menu 
        self.appli.config(menu = menu_bar)

    def continuer (self) : 
        info('Passage à la frame de choix des options')
        self.frame.destroy ()
        self.frame_connection.pack (expand= YES)


    def welcome (self):
        info('Frame du welcome')
        label_title = Label (self.frame,
                     text = "Bienvenue dans la plate-fomre de gestion des consommations et production énergétique",
                     font =("Courrier",25), bg = '#064A14', fg = 'white')
        label_title.grid (row = 0,column = 0,sticky = N)

        #ajouter un bouton
        b_continuer = Button (self.frame, text = "Continuer", font =('Courrier',20), bg = "white",
                            fg = "#FF335B", command = self.continuer)

        b_continuer.grid (pady = 25)       # padding sur y (espace avec l'écriture) | 
                                        # remplissage sur x (occuper tout l'espace sur x)

    def connection(self):
        label_title = Label (self.frame_connection,
                     text = "Merci de vous connecter à la base de donnée",
                     font =("Courrier",15), bg = '#75394d', fg = 'white')
        label_title.grid (row = 0,column = 0,sticky = N)

        password = StringVar() #Password variable
        passEntry = Entry(self.frame_connection, textvariable=password, show='*')
        info('Récupération du mot de passe')
        mdp = Label(self.frame_connection, text='')
        submit = Button(self.frame_connection, text='Connection', command=lambda: mdp.config(text=self.display_connection(passEntry.get())))

        passEntry.grid(pady=25)
        submit.grid(pady=25)


    def option(self):
        label_title = Label (self.frame_option,
                text = "Veuillez séléctionner une option",
                font =("Courrier",25), bg = '#75394d', fg = 'white')
        label_title.grid (row = 0,column = 0,sticky = N)
        info('Choix des options')
        #ajouter un bouton production
        production = Button (self.frame_option, text = "Production", font =('Courrier',20), bg = "white",
                            fg = "#FF335B", command = self.production)

        production.grid (pady = 25)       # padding sur y (espace avec l'écriture) |  # remplissage sur x (occuper tout l'espace sur x)

                #ajouter un bouton production
        consommation = Button (self.frame_option, text = "Consommation", font =('Courrier',20), bg = "white",
                            fg = "#FF335B", command = self.consommation)

        consommation.grid (pady = 25)       # padding sur y (espace avec l'écriture) |  # remplissage sur x (occuper tout l'espace sur x)
                                        
                                        
                #ajouter un bouton production
        prediction = Button (self.frame_option, text = "Prédiction", font =('Courrier',20), bg = "white",
                            fg = "#FF335B", command = self.prediction)

        prediction.grid (pady = 25)       # padding sur y (espace avec l'écriture) |  # remplissage sur x (occuper tout l'espace sur x)
                                        


    def production(self):
        info("Résultats de la production de l'énergie")
        os.system('python ' + PATH + '\\src\\app_prod.py')

    def consommation(self):
        info("Résultats de la consommation de l'énergie")
        os.system('python ' + PATH + '\\src\\app_conso.py')
        
    def prediction(self):
        info("Résultats de la prediction")
        os.system('python ' + PATH + '\\src\\prediction.py')


    def pack(self):
        self.frame.pack (expand = YES)
        self.appli.mainloop()



appli = Application()
appli.welcome()
appli.menu()
appli.connection()
appli.option()
appli.pack()
