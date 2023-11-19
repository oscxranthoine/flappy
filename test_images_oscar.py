import pyxel, random

class Jeu:
    def __init__(self):
        """ definition des differentes variables """
     

        pyxel.init(128, 128, title="Flappy birdy") # taille de la fenetre + titre 
        self.x = 60                                # position du flappy sur l'ecran au debut 
        self.y = 40                                # position du flappy sur l'ecran au debut
        self.scroll_y = 0                          # variable pour le defilement du fond 
        self.ennemis_liste = []                    # liste pour le tuyau n°1 
        self.ennemis_liste1 = []                   # liste pour le tuyau n°2
        self.vies = 1                              # le flappy a 1 vie
        self.score = 0                             # le score part commence à 0 
        self.h = 1                                 # variable qui va : tant que le flappy reste en vie augmente le score 
        self.affichage_x = 0                       # variable qui change le flappy avec le pyxres
        self.affichage_y = 0                       # variable qui change le flappy avec le pyxres
        musique = True                             # variable pour lancer la musique
        pyxel.run(self.update, self.draw)
        


    def vaisseau_deplacement(self):
        """ déplacement avec la touche ESPACE,

        - - quand espace est pressé - - 
            - changement de flappy(battement des ailes)
            - le flappy va monter dans les airs
            
        - - quand espace n'est pas pressé - - 
            - le flappy va descendre dans les airs
            
        """
        
        if pyxel.btn(pyxel.KEY_SPACE) and self.y>-2  :                 # -2  : pour la limite du ciel dans le jeu
            self.y += -0.9                 # le flappy monte 
            self.affichage_x = 0           # position du flappy sur le pyxres
            self.affichage_y = 16          # position du flappy sur le pyxres
            
            
        if not pyxel.btn(pyxel.KEY_SPACE)  and self.y < 90 :            # 90  : pour la limite du sol dans le jeu 
            self.y += 1                    # le flappy descend 
            self.affichage_x = 0           # position du flappy sur le pyxres
            self.affichage_y = 0           # position du flappy sur le pyxres
            
    
    
    def ennemis_creation(self):
        """ création aléatoire des tuyaux,

        - à partir de la droite de l'ecran
        - un tuyau en haut et un en bas
        - avec un ecart entre les tuyau de 70
        
        """
        
        if (pyxel.frame_count % 80 == 0):               # taux d'apparition des tuyaux dans le jeu 
            a = random.randint(0,70)                    # creation d'une taille aleatoire des  tuyaux avec un espacement de 70 
            self.ennemis_liste.append([128, 0, a])      # position - creation du tuyau haut
            self.ennemis_liste1.append([128, 0, 70-a])  # position - creation du tuyau bas 
            
    
    def ennemis_deplacement(self):
        """ déplacement des tuyaux, 

            - apparition a droite de l'ecran 
            - suppression s'ils sortent du cadre à gauche 
            
        """              

        for ennemi in self.ennemis_liste:              # creation d'une boucle for
            ennemi[0] -= 1                             # mouvement du tuyau haut 
            if  ennemi[0]< -20 :                       # si le tuyau arrive a gauche de la fenetre 
                self.ennemis_liste.remove(ennemi)      # le tuyau est supprime 
        
        for ennemi in self.ennemis_liste1:             # creation d'une boucle for 
            ennemi[0] -= 1                             # mouvement du tuyau bas
            if  ennemi[0]<-20:                         # si le tuyau arrive a gauche de la fenetre
                self.ennemis_liste1.remove(ennemi)     # le tuyau est supprime 
                 
    def contact(self):
        """ disparition du flappy,

            - quand il y a un contact avec un tuyau ( celui du haut -- ennemi liste ou celui du bas -- ennemi liste 1 )
            - si contact avec un tuyau, game over --> car plus de vie 

        """

        for ennemi in self.ennemis_liste:                                                             # creation boucle for pour le tuyau haut 
            if ennemi[0]-12 <= self.x+10  and ennemi[0]+12 >= self.x+10 and ennemi[2] >= self.y :     # quand le flappy rentre en contact avec la position du tuyau haut
                self.vies = 0                                                                         # alors, il n'a plus de vie 
                self.h = 0                                                                            # la fonction qui augmente le score s'arrete

        for ennemi in self.ennemis_liste1:                                                             # creation boucle for pour le tuyau bas
            if ennemi[0]-6 <= self.x+10  and ennemi[0]+10  >= self.x  and self.y >= (90 - ennemi[2] ): # quand le flappy rentre en contact avec la position du tuyau bas
                self.vies = 0                                                                          # alors ,  il n'a plus de vie 
                self.h = 0                                                                             # la fonction qui augmente le score s'arrete
                 
    def scroll(self):
        """ defilement du fond d'ecran,

            - a la vitesse 1
            - si le fond depasse 500 alors il revient a zero pour qu'il soit infini 

        """    
        if self.scroll_y> 500 :         # si le fond depasse la position 500
            self.scroll_y = 0           # alors il revient a la position 0 
            
        if self.scroll_y>20:            # si le fond depasse la position 20
            self.scroll_y += 1          # alors vitesse du fond a 1 
        else :
            self.scroll_y =70           # sinon vitesse 70
            
       
    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables """

        # deplacement du flappy 
        self.vaisseau_deplacement()
        
        # fond qui defile 
        self.scroll()
        
        # creation des tuyaux 
        self.ennemis_creation()
        
        # deplacement des tuyaux 
        self.ennemis_deplacement()
        
        # suppression du flappy si contact avec un tuyau 
        self.contact()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
    
        global musique 
        pyxel.cls(0)                 # vide la fenetre
        pyxel.load("oscar.pyxres")   # charger les fonds + musique 
        
        """ tant que le flappy est en vie,


            - deplacement du flappy + du fond d'ecran
            - creation des tuyaux ( 1 en bas et 1 en haut ) - 
                - - de couleur verte
                - - de forme rectangulaire
            - augmentation du score au fur et a mesure que le flappy reste en vie
            - le score est en haut a gauche 
            """
        
        if self.vies > 0:                                                                   # tant que le flappy est en vie
            
            pyxel.playm(0, loop=True)                                                       # jouer la partition 0
            pyxel.bltm(0, 0, 0, self.scroll_y, 0, 256, 256,1)                               # chargement du fond 
            pyxel.blt(self.x, self.y, 0, self.affichage_x, self.affichage_y, 16, 16 ,1)     # chargement du flappy 
            
            for ennemi in self.ennemis_liste:                   
                pyxel.rect(ennemi[0], 0, 18, ennemi[2]  , 3)             # creation du tuyau haut -- rectangle vert 
            for ennemi in self.ennemis_liste1:    
                pyxel.rect(ennemi[0], 104-ennemi[2], 18, ennemi[2] , 3)  # creation du tuyau bas -- rectangle vert   
                
            pyxel.text(0,0, 'Score : ' + str(self.score),7)    # positionnement du score 
            if self.h == 1:                                    # tant que la variable de vie est a 1, c'est a dire que le flappy est en vie 
                self.score += 1                                # alors le score augmente 
            
        
            """ si le flappy n'a plus de vie,

                - le fond reste en mouvement
                - le score / game over est ecrit
                - possibilite de bouger la souris
                - creation du contour d'un rectangle autour de "rejouer" et "arreter"
                    - si la souris rentre  dans le rectangle "rejouer" et qu'on appuie sur la touche espace alors le jeu se relance
                    - si la souris rentre  dans le rectangle "arreter" et qu'on appuie sur la touche espace alors on quitte le jeu 
            
            """
       
        else:
            pyxel.playm(1)                                       # joue la partition 1 
            pyxel.bltm(0, 0, 0, self.scroll_y, 0, 256, 256,1)    # afficher le fond 
            
            pyxel.text(39,29, '--GAME OVER--', 15)             # affichage du texte game over en beige 
            
            pyxel.rectb(17, 43, 32, 10, 3)                     # creation du contour d'un rectangle
            pyxel.text(20,45, 'rejouer', 3)                    # affichage du texte rejouer en vert 
            
            pyxel.rectb(78, 43, 32, 10, 8)                     # creation du contour d'un rectangle
            pyxel.text(80 ,45, 'quitter', 8)                   # affichage du texte quitter en rouge
            
            pyxel.text(36,64, '--Score : ' + str(self.score) + '--',15)   # affichage du score en beige
            pyxel.blt(pyxel.mouse_x,pyxel.mouse_y,0,16,64,16,16, 1)       # affichage du la souris 
            
            if  pyxel.mouse_x > 11 and pyxel.mouse_y >34 and pyxel.mouse_x < 45 and pyxel.mouse_y < 48 and pyxel.btn(pyxel.KEY_SPACE) : # si la souris est dans le rectangle rejouer et qu'on appuie sur espace 
                self.vies = 1                                                                                                           # relance le jeu
                self.ennemis_liste = []
                self.ennemis_liste1 = []
                self.x = 60
                self.y = 40
                self.scroll_y = 0
                self.score = 0
                self.h = 1
                self.affichage_x = 0
                self.affichage_y = 0
                pyxel.run(self.update, self.draw)
                
            if  pyxel.mouse_x > 72 and pyxel.mouse_y >34 and pyxel.mouse_x < 105 and pyxel.mouse_y < 48 and pyxel.btn(pyxel.KEY_SPACE) : # si la souris est dans le rectangle quitter et qu'on appuie sur espace
                quit()                                                                                                                   # quitte le jeu 
                

            
        
Jeu()             