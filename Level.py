__author__ = 'neufrin'
import pygame
import Map
import MapLoader
import Screen
import Helper
import Timer
import Clock
import Option

levels = Helper.levels
WHITE = (255, 255, 255)

class Level(Screen.Screen):
    def __init__(self):
        super(Level, self,).__init__("level")
        self.player = pygame.sprite.Group()
        self.box_list = pygame.sprite.Group()
        self.mLoader = MapLoader.MapLoader()
        Helper.actuallevel = 0
        self.timer = Timer.Timer()
        self.load(levels[Helper.actuallevel])
        self.playermoves = 0
        self.clockWatch = pygame.sprite.Group()
        self.clockWatch.empty()
        self.clockWatch.add(Clock.Clock())
        self.options = [Option.Option("Back to main menu", (520, 565),"mainmenu")]

    def load(self, mapname):
        self.map = Map.Map("1",self.mLoader.load(mapname))
        self.map.build(self)
        self.timer.restart()
        self.playermoves =0;

    def loadNext(self):
        Helper.actuallevel+=1
        if(len(levels)<=Helper.actuallevel):
            return
        self.load(levels[Helper.actuallevel])

    def drawMoves(self,screen,font):
        str = "Moves: %d" %self.playermoves
        text = font.render(str, True, WHITE)
        screen.blit(text, [10, 10])

    def addPlayer(self,_player):
        self.player.add(_player)

    def addBox(self,_box):
        self.box_list.add(_box)

    def playerMoveUp(self):
        p = self.player.sprites()[0]
        self.tryMove(p.x,p.y,p.x,p.y-1)
    def playerMoveDown(self):
        p = self.player.sprites()[0]
        self.tryMove(p.x,p.y,p.x,p.y+1)
    def playerMoveLeft(self):
        p = self.player.sprites()[0]
        self.tryMove(p.x,p.y,p.x-1,p.y)
    def playerMoveRight(self):
        p = self.player.sprites()[0]
        self.tryMove(p.x,p.y,p.x+1,p.y)

    def isBoxOnPlace(self, x, y):
        for i in self.box_list.sprites():
            if( i.x==x and i.y==y):
                if(i.type=="$" or i.type=="*"):
                    return True
        return False

    def isWallOnPlace(self, x, y):
        for i in self.map.bl_list.sprites():
            if( i.x==x and i.y==y):
                if(i.type=="#"):
                    return True
        return False

    def isFree(self,x,y):
        if(self.isWallOnPlace(x,y)==False and self.isBoxOnPlace(x,y)==False):
            return True
        else:
            return False

    def tryMove(self,fromX,fromY,toX,toY):
        dX = toX - fromX
        dY = toY - fromY
        if(self.isWallOnPlace(toX, toY)==True):
            return False
        elif(self.isBoxOnPlace(toX, toY)==True):
            if(self.isWallOnPlace(toX + dX, toY + dY)):
                return False
            elif(self.isBoxOnPlace(toX + dX, toY + dY)):
                return False
            else:
                #you can move box there
                #and move yourself on box place
                self.moveBox(toX,toY,dX,dY)
                self.movePlayer(dX,dY)
        else:
            #justmove to place
            self.movePlayer(dX,dY)

        self.isLevelComplited()

    def movePlayer(self,dx,dy):
        p = self.player.sprites()[0]

        if(dx==0 and dy==-1):
            p.moveUp()
        elif(dx==0 and dy==1):
            p.moveDown()
        elif(dx==-1 and dy==0):
            p.moveLeft()
        elif(dx==1 and dy==0):
            p.moveRight()
        self.playermoves +=1

    def moveBox(self,x,y,dx,dy):
         for i in self.box_list.sprites():
            if( i.x==x and i.y==y):
                i.changePositin(x+dx,y+dy)
                if(self.checkIfPlaceIsGoal(x+dx,y+dy)):
                    i.setOn()
                else:
                    i.setOff()

    def checkIfPlaceIsGoal(self,x,y):
        for i in self.map.bl_list.sprites():
            if(i.x==x and i.y==y):
                if(i.type=="."):
                    return True
        return False

    def isLevelComplited(self):
        for i in self.box_list.sprites():
            if(i.type!="*"):
               return False
        print("Done")
        self.levelCompleted()
        return True

    def levelCompleted(self):
        Helper.actualscreen = "finishedlevel"
        Helper.MOVES_IN_LAST_LEVEL = self.playermoves
        Helper.TIME_IN_LAST_LEVEL = self.timer.time
        self.loadNext()

    def update(self,events):
        crashed = False
        for option in self.options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
        for event in events:
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.playerMoveUp()
                elif event.key == pygame.K_DOWN:
                    self.playerMoveDown()
                elif event.key == pygame.K_LEFT:
                    self.playerMoveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.playerMoveRight()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for option in self.options:
                    if option.hovered == True:
                        option.doAction()
        self.timer.update()
        self.clockWatch.sprites()[0].update()
        return crashed

    def draw(self,screen):
        self.map.draw(screen)
        self.box_list.draw(screen)
        self.player.draw(screen)
        self.timer.draw(screen,Helper.Font)
        self.drawMoves(screen,Helper.Font)
        self.clockWatch.draw(screen)
        for option in self.options:
            option.draw(screen)
