#!/usr/bin/env python3

from direct.showbase.ShowBase import ShowBase
base = ShowBase()

from panda3d.core import NodePath, TextNode,loadPrcFileData
from direct.gui.DirectGui import *
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import *
import sys
import random
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.filter.FilterManager import FilterManager
from panda3d.core import loadPrcFileData
loadPrcFileData("", "textures-power-2 none")
import time
import threading
import Pyro4.core
import os
import pause
from math import ceil
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties
props = WindowProperties()
props.setCursorHidden(True) 
base.win.requestProperties(props)

os.putenv('DISPLAY', ':0.0')
os.putenv('XAUTHORITY', '/home/pi/.Xauthority')

#base.setFrameRateMeter(True)


class Client():


    def __init__(self):

        self.connect() #fonction de connexion au daemon pyro
        self.flag=[False,False,False,False,False] #initialisation des variables aux valeurs par défaut
        self.temps=[0,0,0]
        self.etat=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.joysticks=[[0,0,0,0,0],[0,0,0,0,0]]
        self.h=0
        self.p=0
        self.r=0
        self.porte=[False,False]
        self.jumptry=False
        self.h2=0
        self.p2=0
        self.r2=0
        
    def connect(self):
        connected=False
        while connected==False:
            try:
                self.ipserveur="192.168.0.190" #ip du serveur pyro


                self.nameserver=Pyro4.locateNS(host=self.ipserveur,port=9090)  #localisation du serveur de nom pyro4
                self.uri = self.nameserver.lookup("lostserver")   #recherche de la classe partagée ayant l'id manitobaserver sur le serveur de nom
                self.server = Pyro4.Proxy(self.uri)  #liaison de la classe locale server à la classe partagée trouvée précédement
                connected=True #connexion réussie

            except:# sleep 5 secondes avant de retenter une connexion si serveur non accessible
                print("waiting for server")

                time.sleep(5)

    def refresh(self):  #refresh flags, state and temps from server each 500ms
        try:
            self.flag=self.server.getflag() #liste des flags: #1: run #2 win #3 lost #4 langue #5 alarme
            self.etat=self.server.getetat() #list of 16 int etat de chaque étape
            self.temps=self.server.gettemps() #1 time, #2 additionnal time #3 ending time
            self.porte=self.server.getporte()
        except:  #reconnexion en cas de perte de la connexion avec le serveur pyro
            print("Connection lost. REBINDING...")
            print("(restart the server now)")
            self.server._pyroReconnect()
            time.sleep(5)
        
        threading.Timer(0.5, script.refresh).start()

    def refreshjoy(self):
        try:
            self.joysticks = self.server.getjoysticks()
            #print (self.jumptry)
            self.jumptry = self.server.getjumptry()
            if self.jumptry==True:
                #print (self.jumptry)
                threading.Timer(0.01, w.jumpessai).start()
                #print ("signal saut reçu")
                self.jumptry=False
            #print (self.jumptry)
            #print ()
        except:
            print("erreur com serveur")
        #print (self.joysticks)
        if self.joysticks[0][1]==True:
                self.p=self.p+0.1
                if self.p>0.5:
                    self.p=0.5
                    
                self.p2=self.p2+1
                if self.p2==180:
                   self.p2=-180
                    
        if self.joysticks[0][3]==True:
                self.p=self.p-0.1
                if self.p<-0.5:
                    self.p=-0.5
                    
                self.p2=self.p2-1
                if self.p2==-180:
                   self.p2=180

        if self.joysticks[1][4]==True:
                self.h=self.h+0.1
                if self.h>0.5:
                    self.h=0.5
                    
                self.h2=self.h2+1
                if self.h2==180:
                   self.h2=-180
                    
        if self.joysticks[1][2]==True:
                self.h=self.h-0.1
                if self.h<-0.5:
                    self.h=-0.5
                    
                self.h2=self.h2-1
                if self.h2==-180:
                   self.h2=180
                    
        if self.joysticks[0][2]==True:
                self.r=self.r+0.1
                if self.r>0.5:
                    self.r=0.5
                    
                self.r2=self.r2+1
                if self.r2==180:
                   self.r2=-180

                    
        if self.joysticks[0][4]==True:
                self.r=self.r-0.1
                if self.r<-0.5:
                    self.r=-0.5
                    
                self.r2=self.r2-1
                if self.r2==-180:
                   self.r2=180

                    
        self.h=round(self.h,2)
        self.p=round(self.p,2)
        self.r=round(self.r,2)

        self.h2=int(self.h2)
        self.p2=int(self.p2)
        self.r2=int(self.r2)
        
        if self.h>0:
            self.h=self.h-0.05
        if self.h<0:
            self.h=self.h+0.05
            
        if self.p>0:
            self.p=self.p-0.05
        if self.p<0:
            self.p=self.p+0.05
            
        if self.r>0:
            self.r=self.r-0.05
        if self.r<0:
            self.r=self.r+0.05

        threading.Timer(0.1, script.refreshjoy).start()

class World(object):
    def __init__(self):

        random.seed()

        base.setBackgroundColor(0, 0, 0)  # Set the background to black

        base.camera.setPos(0, 0, 0)  # Set the camera position (X, Y, Z)
        base.camera.setHpr(93, 25, 98)  # Set the camera orientation
        base.disableMouse()
        render.setShaderAuto()
        


        self.current=0
        self.sauts= [False,False,False,False]
        self.orbitscale = 10  # Orbit scale
        self.sizescale = 0.3  # Planet size scale

        self.font = loader.loadFont('font.ttf')
        self.font.setPixelsPerUnit(120)
        self.cullManager = CullBinManager.getGlobalPtr()
        self.cullManager.addBin("onscreenImageBin", self.cullManager.BTFixed, 60)



        #creation des nodes

        
        self.scene0=render.attachNewNode("scene0")
        self.scene1=render.attachNewNode("scene1")
        self.scene2=render.attachNewNode("scene2")
        self.scene3=render.attachNewNode("scene3")
        self.prenode=render.attachNewNode("prenode")
        self.postnode=render.attachNewNode("postnode")
        self.scene0.detachNode()
        self.scene1.detachNode()
        self.scene2.detachNode()
        self.scene3.detachNode()
        self.prenode.detachNode()
        self.postnode.detachNode()

        self.scene0.reparentTo(self.prenode) 
        self.scene1.reparentTo(self.prenode)
        self.scene2.reparentTo(self.prenode)
        self.scene3.reparentTo(self.prenode)


        #creation du cadre et texte sur l'écran
        self.cadre = OnscreenImage(image = 'tex/cadre.png', pos = (0, 0, 0),scale=(1.8,1,1))
        self.cadre.setTransparency(TransparencyAttrib.MAlpha)
        self.textObject = OnscreenText(text = 'my text string', pos = (-1.3, 0.8), scale = 0.1,font=self.font,fg=(37/255,108/255,210/255,255/255),align=TextNode.ALeft)

        self.textlocked = OnscreenText(text = 'Panneau de controle', pos = (-1.5, 0.1), scale = 0.1,font=self.font,fg=(37/255,108/255,210/255,255/255),align=TextNode.ALeft)
        self.textlocked2 = OnscreenText(text = 'verrouille', pos = (-1.5, -0.1), scale = 0.1,font=self.font,fg=(37/255,108/255,210/255,255/255),align=TextNode.ALeft)


 
        self.textpower = OnscreenText(text = 'Alimentation défaillante. Controle cablage requis', pos = (-1.5, -0.9), scale = 0.05,font=self.font,fg=(1,0,0,1),align=TextNode.ALeft)

        self.textjump = OnscreenText(text = 'saut:', pos = (0.3, 0.8), scale = 0.07,font=self.font,fg=(37/255,108/255,210/255,255/255),align=TextNode.ALeft)
        self.textjump2 = OnscreenText(text = 'impossible:', pos = (0.7, 0.8), scale = 0.07,font=self.font,fg=(1,0,0,1),align=TextNode.ALeft)
        
        self.countdown= OnscreenText(text = 'Jump in', pos = (0, 0.4), scale = 0.1,font=self.font,fg=(37/255,108/255,210/255,255/255),align=TextNode.ACenter)        
        self.countdownn= OnscreenText(text = '5', pos = (0,-0.4), scale = 0.6,font=self.font,fg=(37/255,108/255,210/255,255/255),align=TextNode.ACenter)

        self.jumpimpossible=OnscreenText(text = 'jump', pos = (0,0.2), scale = 0.2,font=self.font,fg=(1,0,0,1),align=TextNode.ACenter)
        self.jumpimpossible2=OnscreenText(text = 'impossible', pos = (0,-0.2), scale = 0.2,font=self.font,fg=(1,0,0,1),align=TextNode.ACenter)
        
        self.cadre.setBin("onscreenImageBin", 1)
        self.textObject.setBin("onscreenImageBin", 2)
        self.textpower.setBin("onscreenImageBin", 2)
        self.textjump.setBin("onscreenImageBin", 2)
        self.textjump2.setBin("onscreenImageBin", 2)
        
        self.textObject.detachNode()
        self.textlocked.detachNode()
        self.textlocked2.detachNode()
        self.cadre.detachNode()
        self.textjump.detachNode()
        self.textjump2.detachNode()
        self.countdown.detachNode()
        self.countdownn.detachNode()
        self.jumpimpossible.detachNode()
        self.jumpimpossible2.detachNode()
        self.loadPlanets()
        self.rotatePlanets()
        

        #définition des lumières 
        
        alight1 = AmbientLight('alight')
        alight1.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp1 = self.scene1.attachNewNode(alight1)
        self.scene1.setLight(alnp1)


        plight1 = PointLight('plight')
        plight1.setColor(VBase4(1, 0.2, 0.1, 1))

        plight1.setAttenuation(LVector3(0.5, 0, 0))
        self.plnp1 = self.scene1.attachNewNode(plight1)
        self.plnp1.setPos(850.4,-500,134)
        self.scene1.setLight(self.plnp1)
                              



        plight2 = PointLight('plight2')
        plight2.setColor(VBase4(0.8, 0.95, 1, 1))

        plight2.setAttenuation(LVector3(0.5, 0, 0))
        self.plnp2 = self.scene2.attachNewNode(plight2)
        self.plnp2.setPos(62.4,-31,71)
        self.scene2.setLight(self.plnp2)

        plight3 = PointLight('plight2')
        plight3.setColor(VBase4(1, 1, 1, 1))

        plight3.setAttenuation(LVector3(0.5, 0, 0))
        self.plnp3 = self.scene3.attachNewNode(plight3)
        self.plnp3.setPos(62.4,-31,71)
        self.scene3.setLight(self.plnp3)
                              


        self.raydensity = 0
        self.raydecay = 0.97
        self.rayexposure = 0.03
        
        
            
        #chargement de la musique 
        self.musique1=base.loader.loadSfx("mus/music1.ogg")
        self.musique1.setVolume(0.2)
        self.musique2=base.loader.loadSfx("mus/stellardrone2.ogg")
        self.musique2.setVolume(0.2)
        self.musique3=base.loader.loadSfx("mus/stellardrone.ogg")
        self.musique3.setVolume(0.3)
        self.winmusique=base.loader.loadSfx("mus/win.ogg")
        self.winmusique.setVolume(0.6)
        self.lostmusique=base.loader.loadSfx("mus/lost.ogg")
        self.lostmusique.setVolume(0.6)

        self.musiqueend=[False,False]
        self.jumpsound=base.loader.loadSfx("mus/jump3.ogg")
        self.jumpsound.setVolume(1)
        self.mesjump=[[base.loader.loadSfx("mus/mesjumprdyfr.wav"),base.loader.loadSfx("mus/mesjumpinfr.wav"),base.loader.loadSfx("mus/mesjump5fr.wav")],[base.loader.loadSfx("mus/mesjumprdy.wav"),base.loader.loadSfx("mus/mesjumpin.wav"),base.loader.loadSfx("mus/mesjump5.wav")]]


        self.mesjump[0][0].setVolume(1)
        self.mesjump[0][1].setVolume(1)
        self.mesjump[0][2].setVolume(1)
        self.mesjump[1][0].setVolume(1)
        self.mesjump[1][1].setVolume(1)
        self.mesjump[1][2].setVolume(1)
        
        self.jumpimpo=[base.loader.loadSfx("mus/mesjumpimpofr.wav"),base.loader.loadSfx("mus/mesjumpimpo.wav")]
        self.jumpimpo[0].setVolume(1)
        self.jumpimpo[1].setVolume(1)

        self.boutonnon=base.loader.loadSfx("mus/button2.ogg")
        self.boutonnon.setVolume(1)

        self.mescoord=[base.loader.loadSfx("mus/coordofr.wav"),base.loader.loadSfx("mus/coordo.wav")]
        self.mescoord[0].setVolume(1)
        self.mescoord[1].setVolume(1)
        
        
        #filtres effets spéciaux
        
        self.filters = CommonFilters(base.win, base.cam)
        self.filters.setBloom(blend=(0, 0, 0, 1),mintrigger =0.6, desat=-0.5, intensity=3.0, size="medium")


        self.filters.setVolumetricLighting(self.plnp1,numsamples = 32,density = self.raydensity,decay = self.raydecay,exposure = self.rayexposure)

    def loadPlanets(self):
        #chargement des modèles 3d et textures

        self.tex_red=loader.loadTexture("tex/phtex.jpg")

        
        self.sky = loader.loadModel("model/boule3")
        self.sky2 = loader.loadModel("model/boule3")
        self.sky3  = loader.loadModel("model/boule3")
    
        
        self.sky.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.sky.setTexProjector(TextureStage.getDefault(), render, self.sky)
        self.sky.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.sky.setTexScale(TextureStage.getDefault(), 1)
        self.sky.reparentTo(self.scene1)

        self.sky.setLightOff()

        self.sky.setScale(300)
        self.sky.setPos(0,0,0)
        
        self.sky2.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.sky2.setTexProjector(TextureStage.getDefault(), render, self.sky2)
        self.sky2.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.sky2.setTexScale(TextureStage.getDefault(), 1)
        self.sky2.reparentTo(self.scene2)

        self.sky2.setLightOff()

        self.sky2.setScale(300)
        
        self.sky2.setPos(0,0,0)

        self.sky3.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.sky3.setTexProjector(TextureStage.getDefault(), render, self.sky2)
        self.sky3.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.sky3.setTexScale(TextureStage.getDefault(), 1)
        self.sky3.reparentTo(self.scene3)

        self.sky3.setLightOff()

        self.sky3.setScale(300)
        
        self.sky3.setPos(0,0,0)

   
        self.sky_tex = loader.loadCubeMap("tex/skybox/Exploding_Planet_Red/sky_#.png")
        self.sky_texglow = loader.loadCubeMap("tex/skybox/glowExploding_Planet_Red/sky_#.png")

        self.sky2_tex = loader.loadCubeMap(("tex/skybox/Planet_Blue-copie/sky_#.png"))

        self.sky3_tex = loader.loadCubeMap(("tex/skybox/skyboxv1_europe/sky-#.png"))
        #self.sky.blue_texglow = loader.LoadCubeMap(("tex/skybox/Planet_Blue/sky_#.png"))
        #self.sky3_tex  = loader.loadTexture("tex/milky.jpg")
        
        self.sky.setTexture(self.sky_tex , 1)
        self.sky2.setTexture(self.sky2_tex , 1)
        self.sky3.setTexture(self.sky3_tex , 1)



        tsglow = TextureStage('tsglow')
        tsglow.setMode(TextureStage.MGlow)
        #self.sky.setTexture(tsglow, self.sky_texglow)


        self.gas1= loader.loadModel("model/boule5")
        self.orbit_root_gas1=self.scene1.attachNewNode('orbit_root_gas1')
        self.gas1_tex= loader.loadTexture("tex/plan1.png")

        self.gas1.setTexture(self.gas1_tex,1)
        self.gas1.setR(75)
        self.gas1.setScale(40)
        self.gas1.setPos(-520,520,0)
        self.gas1.setAntialias(AntialiasAttrib.MMultisample)
        self.gas1.reparentTo(self.orbit_root_gas1)




        self.ring=loader.loadModel("model/ring.egg")
        self.ringnode=self.scene1.attachNewNode("ring")
        self.ring_tex=loader.loadTexture("tex/ring1.png")
   
        self.ring.setScale(10)
        self.ring.setPos(self.gas1.getPos())

        self.ring.setR(75)
        self.ring.reparentTo(self.ringnode)
        self.ring.setTexture(self.ring_tex,1)
        self.ringnode.setTwoSided(True)

        self.ringnode.setTransparency(TransparencyAttrib.MAlpha)


        

        
        self.ast1_tex=loader.loadTexture("asteroides/ast1C.tga")
        self.ast2_tex=loader.loadTexture("asteroides/ast2C.tga")
        self.ast3_tex=loader.loadTexture("asteroides/ast3C.tga")
        self.ast4_tex=loader.loadTexture("asteroides/ast4C.tga")
        self.ast5_tex=loader.loadTexture("asteroides/ast5.tga")
        self.ast6_tex=loader.loadTexture("asteroides/ast6.tga")
        
        self.ast1_norm=loader.loadTexture("asteroides/ast1N.tga")
        self.ast2_norm=loader.loadTexture("asteroides/ast2N.tga")
        self.ast3_norm=loader.loadTexture("asteroides/ast3N.tga")
        self.ast4_norm=loader.loadTexture("asteroides/ast4N.tga")
        self.ast5_norm=loader.loadTexture("asteroides/ast5N.tga")
        self.ast6_norm=loader.loadTexture("asteroides/ast6N.tga")

        self.ast1=loader.loadModel("asteroides/ast1")
        self.ast2=loader.loadModel("asteroides/ast2")
        self.ast3=loader.loadModel("asteroides/ast3")
        self.ast4=loader.loadModel("asteroides/ast4")
        self.ast5=loader.loadModel("asteroides/ast5")
        self.ast6=loader.loadModel("asteroides/ast6")

        self.orbit_root_ast1=self.scene1.attachNewNode('orbit_root_ast1')
        self.orbit_root_ast2=self.scene1.attachNewNode('orbit_root_ast2')
        self.orbit_root_ast3=self.scene1.attachNewNode('orbit_root_ast3')
        self.orbit_root_ast4=self.scene1.attachNewNode('orbit_root_ast4')
        self.orbit_root_ast5=self.scene1.attachNewNode('orbit_root_ast5')
        self.orbit_root_ast6=self.scene1.attachNewNode('orbit_root_ast6')





        self.ast1.setScale(0.002)
        self.ast2.setScale(0.002)
        self.ast3.setScale(0.002)
        self.ast4.setScale(0.002)
        self.ast5.setScale(0.001)
        self.ast6.setScale(0.001)

        self.ast1.setPos(0,0,0)
        self.ast2.setPos(random.uniform(-10,10),30,0)
        self.ast3.setPos(random.uniform(-10,10),-30,30)
        self.ast4.setPos(random.uniform(-10,10),-30,-30)
        self.ast5.setPos(random.uniform(-10,10),30,-30)
        self.ast6.setPos(random.uniform(-10,10),-30,40)


        self.ast1.setTexture(self.ast1_tex,1)
        self.ast2.setTexture(self.ast2_tex,1)
        self.ast3.setTexture(self.ast3_tex,1)
        self.ast4.setTexture(self.ast4_tex,1)
        self.ast5.setTexture(self.ast5_tex,1)
        self.ast6.setTexture(self.ast6_tex,1)
        


        pos=[100,-730,650]
        pos1=[[79, -756, 681], [104, -715, 646], [111, -754, 678], [117, -747, 687], [107, -698, 651], [131, -712, 661], [88, -705, 668], [107, -706, 642], [128, -713, 644], [94, -762, 640], [122, -715, 621], [69, -758, 676], [89, -766, 617], [129, -739, 627], [140, -710, 625], [125, -713, 669], [127, -766, 654], [90, -745, 659], [134, -764, 657], [136, -709, 644], [102, -765, 650], [66, -754, 680], [108, -709, 661], [76, -704, 644], [118, -714, 632], [102, -738, 625], [71, -769, 647], [103, -717, 657], [125, -723, 645], [133, -746, 631], [94, -752, 629], [64, -719, 646], [88, -700, 658], [112, -758, 645], [83, -768, 654], [110, -700, 674], [84, -754, 643], [91, -740, 642], [127, -761, 643], [83, -761, 689], [139, -729, 646], [69, -749, 658], [138, -768, 671], [131, -740, 622], [114, -694, 667], [135, -767, 665], [128, -751, 653], [62, -760, 670], [76, -721, 648], [122, -767, 659]]
        pos2=[[-28, 27, -50], [-72, -67, -21], [62, -49, -64], [-60, -2, -24], [14, 43, 40], [-36, 39, -20], [-54, -51, -46], [55, -30, 63], [53, -19, -14], [39, -65, 67], [76, -47, -54], [-18, -62, -23], [-43, -16, -10], [-73, -14, 18], [79, -26, -70], [-16, -35, 4], [66, 70, 30], [2, -38, 75], [19, 0, 34], [63, -15, -56], [57, 47, -27], [3, 59, -53], [58, -52, -30], [-49, 30, -59], [-6, 41, -54], [34, 50, -3], [78, -68, -65], [39, -2, -60], [-58, 47, -33], [-36, -65, 80], [41, -33, 72], [-74, 43, 3], [41, -21, 58], [74, -48, -4], [-5, 31, 53], [-69, -52, 20], [48, -78, 62], [38, 19, -13], [2, -18, -42], [-46, -3, 13], [-40, -75, 25], [-36, -67, -70], [-22, 27, 19], [-70, -10, -68], [52, -45, -49], [77, 13, 73], [51, -13, -14], [17, -27, 60], [46, -65, -46], [-51, -34, 43]]
        
        for x in range (0,50):
            if x<30:
                placeholder= self.scene1.attachNewNode("asteroidplaceholder")
                placeholder.setPos(pos1[x][0],pos1[x][1],pos1[x][2])
                placeholder.setScale(random.uniform(0.1,10))
                placeholder.setHpr(random.randint(0,360),random.randint(0,360),random.randint(0,360))
                self.ast3.instanceTo(placeholder)

               
            elif x<40:
                placeholder= self.scene1.attachNewNode("asteroidplaceholder")
                placeholder.setPos(pos1[x][0],pos1[x][1],pos1[x][2])
                placeholder.setScale(random.uniform(0.1,10))
                placeholder.setHpr(random.randint(0,360),random.randint(0,360),random.randint(0,360))
                self.ast4.instanceTo(placeholder)
                
            elif x<45:
                placeholder= self.scene1.attachNewNode("asteroidplaceholder")

                placeholder.setPos(pos1[x][0],pos1[x][1],pos1[x][2])
                placeholder.setScale(random.uniform(0.1,10))
                placeholder.setHpr(random.randint(0,360),random.randint(0,360),random.randint(0,360))
            
                self.ast5.instanceTo(placeholder)
            elif x<50:
                placeholder= self.scene1.attachNewNode("asteroidplaceholder")

                placeholder.setPos(pos1[x][0],pos1[x][1],pos1[x][2])
                placeholder.setScale(random.uniform(0.1,10))
                placeholder.setHpr(random.randint(0,360),random.randint(0,360),random.randint(0,360))
     
                self.ast6.instanceTo(placeholder)
        pos=[0,0,0]            
        for x in range (0,50):
            if x<25:
                placeholder= self.scene2.attachNewNode("asteroidplaceholder")
                placeholder.setPos(pos2[x][0],pos2[x][1],pos2[x][2])
                placeholder.setScale(random.uniform(0.1,3))
                placeholder.setHpr(random.randint(0,360),random.randint(0,360),random.randint(0,360))
                self.ast1.instanceTo(placeholder)

               
            elif x<50:
                placeholder= self.scene2.attachNewNode("asteroidplaceholder")
                placeholder.setPos(pos2[x][0],pos2[x][1],pos2[x][2])
                placeholder.setScale(random.uniform(0.1,3))
                placeholder.setHpr(random.randint(0,360),random.randint(0,360),random.randint(0,360))
                self.ast2.instanceTo(placeholder)
                
               
#nebula, but if was ugly             
##        self.nebu=loader.loadModel("model/nebu.egg")
##        
##        self.nebunode=self.scene1.attachNewNode("nebu")
##        self.nebu_tex=loader.loadTexture("tex/nebu4.png")
##        self.nebu_tex_glow=loader.loadTexture("tex/nebug.png")
##   
##        self.nebu.setScale(200)
##        self.nebu.setPos((-640,-430,-62))
##
##        #self.nebu.setHpr(180)
##        self.nebu.reparentTo(self.nebunode)
##        self.nebu.setTexture(self.nebu_tex,1)
##        #self.nebu.setTexture(tsglow,self.nebu_tex_glow)
##        self.nebunode.setTwoSided(True)
##
##        self.nebunode.setTransparency(TransparencyAttrib.MAlpha)
##        self.nebunode.setLightOff()
   




    def spinCameraTask(self, task):

        #debug textes
        #self.textObject.text = (str(render.getRelativeVector(base.camera, Vec3.forward())))
        #self.textObject.text = (str(self.raydensity)+" "+str(self.raydecay)+" "+str(self.rayexposure))
        #self.textObject.text = (str(base.camera.getHpr()))
        self.camhpr=base.camera.getHpr()
        #self.textObject.text =( "x:" + str(int(round ( self.camhpr[0])))+ " y:"+ str(int(round ( self.camhpr[1])))+" z:"+str(int(round ( self.camhpr[2]))))
        self.textObject.text =( "x:" + str(int(round ( script.h2)))+ " y:"+ str(int(round ( script.p2)))+" z:"+str(int(round ( script.r2))))        
        base.camera.setHpr(base.camera,script.h,script.p,script.r)




        
        return Task.cont


    def mustart(self,mus):
        #start musique
        pause.until(ceil(time.time()+1))
        mus.play()

    def jump(self,num):
        #saut hyperspatial
        self.musique3.setVolume(0.2)
        if script.flag[3]:
            self.countdown.text=("saut dans:")
            self.mesjump[0][1].play()
        else:
            self.countdown.text=("jump in:")
            self.mesjump[1][1].play()
        
        self.countdownn.text=("5")
        
        self.countdown.reparentTo(aspect2d)
        self.countdownn.reparentTo(aspect2d)
        time.sleep(1.5)
        if script.flag[3]:
            self.mesjump[0][2].play()
        else:
            self.mesjump[1][2].play()
        time.sleep(1)
        self.countdownn.text=("4")
        time.sleep(1)
        self.countdownn.text=("3")
        self.jumpsound.play()      
        time.sleep(1)
        self.countdownn.text=("2")
        time.sleep(1)
        self.countdownn.text=("1")
        time.sleep(1)
            
        self.countdown.detachNode()
        self.countdownn.detachNode()  

        
        while self.rayexposure<5:
            self.rayexposure=self.rayexposure+0.04
            self.filters.setVolumetricLighting(self.plnp1,numsamples = 32,density = self.raydensity,decay = self.raydecay+0.01,exposure = self.rayexposure)
            time.sleep(0.02)
        
        if num==1:
                    self.scene1.reparentTo(self.postnode)
                    self.scene2.reparentTo(render)
                    base.camera.setHpr(-69,-82,93)
                    
        if num==2:
                    self.scene2.reparentTo(self.postnode)
                    self.scene1.reparentTo(self.postnode)
                    self.scene3.reparentTo(render)
                    base.camera.setHpr(-70,33,-173)
        while self.rayexposure>0.03:
            self.rayexposure=self.rayexposure-0.04
            self.filters.setVolumetricLighting(self.plnp1,numsamples = 32,density = self.raydensity,decay = self.raydecay+0.01,exposure = self.rayexposure)
            time.sleep(0.02)

        self.sauts[2]=False
        self.musique3.setVolume(0.3)


    def jumpnon(self):
        #saut hyperspatial impossible
        self.boutonnon.play()
        time.sleep(1)
        self.jumpimpossible.fg=(1,0,0,1)
        self.jumpimpossible2.fg=(1,0,0,1)
        if script.flag[3]:
            self.jumpimpossible.text=("saut")
            self.jumpimpossible2.text=("impossible")
            self.jumpimpo[0].play
        else:
            self.jumpimpossible.text=("jump")
            self.jumpimpossible2.text=("impossible")
            self.jumpimpo[1].play
        for i in range(5):      
            self.jumpimpossible.reparentTo(aspect2d)
            self.jumpimpossible2.reparentTo(aspect2d)
            time.sleep(0.5)
            self.jumpimpossible.detachNode()
            self.jumpimpossible2.detachNode()
            time.sleep(0.5)

    def coordonneincorrectes(self):
        self.boutonnon.play()
        time.sleep(1)
        self.jumpimpossible.fg=(1,0,0,1)
        self.jumpimpossible2.fg=(1,0,0,1)
        if script.flag[3]:
            self.jumpimpossible.text=("coordonnees")
            self.jumpimpossible2.text=("incorrectes")
            self.mescoord[0].play
        else:
            self.jumpimpossible.text=("wrong")
            self.jumpimpossible2.text=("coordinates")
            self.mescoord[1].play
        for i in range(5):      
            self.jumpimpossible.reparentTo(aspect2d)
            self.jumpimpossible2.reparentTo(aspect2d)
            time.sleep(0.5)
            self.jumpimpossible.detachNode()
            self.jumpimpossible2.detachNode()
            time.sleep(0.5)

    def jumpessai(self):

        #print ("jumpessai")

        if script.etat[11]==0:
            if script.etat[9]==0:
                threading.Timer(0.01, self.jumpnon).start()
                
            elif int(script.h2)==-45 and int(script.p2)==54 and int(script.r2)==173:
                try:
                    script.etat[11]=1
                    script.server.changeetat(11,1)
                except:
                    print ("erreur com réseau")
            else:
                threading.Timer(0.01, self.coordonneincorrectes).start()

                

        elif script.etat[12]==0:
            if script.etat[10]==0:
                threading.Timer(0.01, self.jumpnon).start()
            elif int(script.h2)==-88 and int(script.p2)==34 and int(script.r2)==-128:
                try:
                    script.etat[12]=1
                    script.server.changeetat(12,1)
                except:
                    print ("erreur com réseau")
            else:
                threading.Timer(0.01, self.coordonneincorrectes).start()
        #self.textObject.text =( "x:" + str(int(round ( self.camhpr[0])))+ " y:"+ str(int(round ( self.camhpr[1])))+" z:"+str(int(round ( self.camhpr[2]))))

    def iotruc(self,task):

            if script.flag[0] :
                #executé si salle en cours
                if self.musique1.status() == self.musique1.READY and script.porte[0] == True and self.current==0:
                    self.current=1
                    threading.Timer(0.01, self.mustart,[self.musique1]).start()

                if self.musique2.status() == self.musique2.READY  and self.musique1.status()== self.musique1.PLAYING and script.porte[0]== False and self.current==1 and  script.etat[5]==1 and script.etat[6]==1 and script.etat[7]==1 and script.etat[8]==1:
                    self.musique1.stop()
                    self.current=2
                    threading.Timer(0.01, self.mustart,[self.musique2]).start()

                if self.musique3.status() == self.musique3.READY  and self.musique2.status()== self.musique2.PLAYING and script.porte[0]== False and script.etat[1]==1 and script.etat[13]==1 and script.etat[3]==1 and self.current==2:
                    self.musique2.stop()
                    self.current=3
                    threading.Timer(0.01, self.mustart,[self.musique3]).start()

                if script.etat[3]==1 : #cable
                    if self.scene0.getParent()==self.prenode:
                        self.cadre.reparentTo(aspect2d)
                        self.textpower.detachNode()
                        self.textlocked.reparentTo(aspect2d)
                        self.textlocked2.reparentTo(aspect2d)
                        self.scene0.reparentTo(render)  
                    
                if script.etat[2]==1 and script.etat[3]==1: #unlock
                    
                    if self.scene1.getParent()==self.prenode:
                        self.textlocked.detachNode()
                        self.textlocked2.detachNode()
                        self.textObject.reparentTo(aspect2d)
                        self.textjump.reparentTo(aspect2d)
                        self.textjump2.reparentTo(aspect2d)
                        self.scene0.reparentTo(self.postnode)
                        self.scene1.reparentTo(render)

                if script.flag[6]:
                    self.textjump2.fg=(0,1,0,1)

                    if script.flag[3]:
                        if self.sauts[3]==False:
                            self.mesjump[0][0].play()
                        self.textjump2.text=("pret")
                        
                        
                    else:
                        self.textjump2.text=("ready")
                        if self.sauts[3]==False:
                            self.mesjump[1][0].play()
                    self.sauts[3]=True

                elif self.sauts[2]:
                    self.textjump2.fg=(0,1,0,1)
                    if script.flag[3]:
                        self.textjump2.text=("en cours")
                    else:
                        self.textjump2.text=("jumping")


                        
                 

                else :
                    self.textjump2.fg=(1,0,0,1)
                    self.sauts[3]=False
                    if script.flag[3]:
                        self.textjump2.text=("impossible")
                    else:
                        self.textjump2.text=("impossible")
                    

            
                    
                
                if script.etat[11]==1 and self.sauts[0]==False: # saut1
                    #print ("tente")
                    if script.flag[7]==False:
                        #print ("tente")
                        if self.scene3.getParent()==self.prenode:
                            #print ("tente2")     
                            threading.Timer(0.01, self.jump,[2]).start()
                            self.sauts[0]=True
                            #self.sauts[1]=True
                            self.sauts[2]=True

                    else:
                
                        if self.scene2.getParent()==self.prenode:
                
                            threading.Timer(0.01, self.jump,[1]).start()
                            self.sauts[0]=True
                            self.sauts[2]=True

    
                if script.etat[12]==1 and self.sauts[1]==False: #saut2
                    if self.scene3.getParent()==self.prenode:
       
                        threading.Timer(0.01, self.jump,[2]).start()
                        self.sauts[1]=True
                        self.sauts[2]=True


                
                else:
                    #executé si étape réussie
                    pass

            elif script.flag[1]==True :
                #executé si salle gagnée

                if script.flag[7]==False:
                    if self.scene3.getParent()==self.prenode and self.sauts[0]==False:
                            #print ("tente2")     
                            threading.Timer(0.01, self.jump,[2]).start()
                            self.sauts[0]=True
                            #self.sauts[1]=True
                            self.sauts[2]=True
                    if script.etat[9]==1 and script.etat[11]==1  and self.sauts[2]==True :
                        
                        if  self.musiqueend[0]==False:
                            self.musique3.stop()
                            self.musique1.stop()
                            self.musique2.stop()
                            threading.Timer(0.01, self.mustart,[self.winmusique]).start()
                            self.musiqueend[0]=True
                    elif script.etat[9]==1 and script.etat[11]==1 and self.sauts[2]==False :
                        
                        self.jumpimpossible.fg=(0,1,0,1)
                        self.jumpimpossible2.fg=(0,1,0,1)
                        if script.flag[3]:
                            self.textjump2.text=("termine")
                            self.jumpimpossible.text=("terre en vue :)")
                            self.jumpimpossible2.text=("temps: "+ time.strftime("%H:%M:%S",time.gmtime(script.temps[0]+script.temps[1])))
                        else:
                            self.textjump2.text=("over")
                            self.jumpimpossible.text=("earth in sight :)")
                            self.jumpimpossible2.text=("time: "+ time.strftime("%H:%M:%S",time.gmtime(script.temps[0]+script.temps[1])))
                        self.jumpimpossible.reparentTo(aspect2d)
                        self.jumpimpossible2.reparentTo(aspect2d)

                else:
                    if script.etat[9]==1 and script.etat[10]==1 and script.etat[11]==1  and script.etat[12]==1 and self.sauts[2]==True :
                        
                        if  self.musiqueend[0]==False:
                            self.musique3.stop()
                            self.musique1.stop()
                            self.musique2.stop()
                            threading.Timer(0.01, self.mustart,[self.winmusique]).start()
                            self.musiqueend[0]=True
                    elif script.etat[9]==1 and script.etat[10]==1 and script.etat[11]==1  and script.etat[12]==1 and self.sauts[2]==False :
                        
                        self.jumpimpossible.fg=(0,1,0,1)
                        self.jumpimpossible2.fg=(0,1,0,1)
                        if script.flag[3]:
                            self.textjump2.text=("termine")
                            self.jumpimpossible.text=("terre en vue :)")
                            self.jumpimpossible2.text=("temps: "+ time.strftime("%H:%M:%S",time.gmtime(script.temps[0]+script.temps[1])))
                        else:
                            self.textjump2.text=("over")
                            self.jumpimpossible.text=("earth in sight :)")
                            self.jumpimpossible2.text=("time: "+ time.strftime("%H:%M:%S",time.gmtime(script.temps[0]+script.temps[1])))
                        self.jumpimpossible.reparentTo(aspect2d)
                        self.jumpimpossible2.reparentTo(aspect2d)


                    
            elif script.flag[2]==True:
                #executé si salle perdue
                
                    
                    self.jumpimpossible.fg=(1,0,0,1)
                    self.jumpimpossible2.fg=(1,0,0,1)
                    if script.flag[3]:
                        #self.textjump2.text=("termine")
                        self.jumpimpossible.text=("temps ecoule!")
                        self.jumpimpossible2.text=("dommage :(")
                    else:
                        #self.textjump2.text=("over")
                        self.jumpimpossible.text=("time out!")
                        self.jumpimpossible2.text=("too bad :(")
                    self.textpower.detachNode()
                    self.jumpimpossible.reparentTo(aspect2d)
                    self.jumpimpossible2.reparentTo(aspect2d)
                    self.textlocked.detachNode()
                    self.textlocked2.detachNode()
                    self.scene0.detachNode()
                    self.scene1.detachNode()
                    self.scene2.detachNode()
                    self.scene3.detachNode()
                    self.musique3.stop()
                    if  self.musiqueend[1]==False:
                        self.musique3.stop()
                        self.musique1.stop()
                        self.musique2.stop()
                        threading.Timer(0.01, self.mustart,[self.lostmusique]).start()
                        self.musiqueend[1]=True

            else:
                #reset
                        self.scene0.reparentTo(self.prenode) 
                        self.scene1.reparentTo(self.prenode)
                        self.scene2.reparentTo(self.prenode)
                        self.scene3.reparentTo(self.prenode)
                        self.musique1.stop()
                        self.musique2.stop()
                        self.musique3.stop()
                        self.current=0
                        self.sauts=[False,False,False,False]
                        self.cadre.detachNode()
                        self.textObject.detachNode()
                        self.textpower.reparentTo(aspect2d)
                        self.textlocked.detachNode()
                        self.textlocked2.detachNode()
                        self.textjump.detachNode()
                        self.textjump2.detachNode()
                        script.h=0
                        script.p=0
                        script.r=0
                        script.h2=0
                        script.p2=0
                        script.r2=0
                        base.camera.setHpr(93,25,98)
                        self.jumpimpossible.detachNode()
                        self.jumpimpossible2.detachNode()
                        self.musiqueend=[False,False]
                        self.winmusique.stop()
                        self.lostmusique.stop()
                        
            #executé toujours
            if script.flag[3]:
                self.textpower.text=("alimentation absente. reconnexion cablage requis")
                self.textlocked.text=("poste de commande")
                self.textlocked2.text=("verrouille")
                self.textjump.text=("saut:")

            else:
                self.textpower.text=("power failure. check cable")
                self.textlocked.text=("command panel")
                self.textlocked2.text=("locked")
                self.textjump.text=("jump:")



        

            return Task.cont

    def rotatePlanets(self):
        #mouvement des planètes

        self.day_period_ast1=self.ast1.hprInterval(30,(360,0,0))
        self.day_period_ast1.loop()

        self.day_period_ast2=self.ast2.hprInterval(30,(360,0,0))
        self.day_period_ast2.loop()

        self.day_period_ast3=self.ast3.hprInterval(60,(360,0,0))
        self.day_period_ast3.loop()

        self.day_period_ast4=self.ast4.hprInterval(80,(360,0,0))
        
        self.day_period_ast4.loop()
        self.day_period_ast5=self.ast5.hprInterval(80,(360,0,0))
        self.day_period_ast5.loop()
        self.day_period_ast6=self.ast6.hprInterval(80,(360,0,0))
        self.day_period_ast6.loop()
        


        taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        taskMgr.add(self.iotruc, "iotruc")

# end class world

# instantiate the class
script=Client()
script.refresh()
script.refreshjoy()
w = World()
base.run()
