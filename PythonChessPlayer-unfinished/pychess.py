"""EXTRA NOTES FROM DEVELOPER"""
#Due to how messy the source code is (and the fact that I havent touched this project for a while, which results to me forgetting how almost everything works here), a remake of this Chess Program will be made soon
#-sidharta310312 on github.com


import pygame
import time
import sys
import os
import getpass
import webbrowser
 
pygame.init()
 
#init screen
 
screensize = (600,600)
screen = pygame.display.set_mode((screensize[0] + 300, screensize[1]))

#init font
default_font = pygame.font.SysFont("Consolas", 40)

#init colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
blacktile = (118,150,86)
gray = (128,128,128)
yellow = (255,255,0)

#initialize pieces map
pcName = getpass.getuser()
loadImage = pygame.image.load
PieceMap = loadImage(os.path.dirname(os.path.realpath(__file__)) + r"\assets\PiecesMap.png")

#PieceIDs :
#-2 = En Passant Tile
#-1 = empty slot
#0 = white king
#1 = white queen
#2 = white bishop
#3 = white knight
#4 = white rook
#5 = white pawn
#6 = black king
#7 = black queen
#8 = black bishop
#9 = black knight
#10 - black rook
#11 - black pawn

tileOccup = (
    [10,9,8,7,6,8,9,10],
    [11,11,11,11,11,11,11,11],
    [-1,-1,-1,-1,-1,-1,-1,-1],
    [5,-1,-1,4,-1,-1,2,-1],
    [-1,-1,8,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1],
    [5,5,5,5,5,5,5,5],
    [4,3,2,1,0,2,3,4]
)

EnPassantPossible = (
    [True] * 8, #BlackPawns
    [True] * 8 #WhitePawns
)

EnPassantData = []

TileSize = int(screensize[0]/8)
SelectedTile, SelectedPieceID = 0, 0
SelectedData = [-1,-1,[-1], "White", 0] #selected tile (piece position), selected piece id, Legal target points data, selected turn, Moves Made
MovesHistory = []
#AlreadySelect = False
cursor = pygame.Rect(10,10,10,10)

githublinkHitbox = pygame.Rect(0,0,0,0)

#left = top                  right = bottom

def MakeText(position, text, size, color, corner=False, thicc=False):
    newText = pygame.font.SysFont("Consolas", size, bold=thicc).render(text, True, color)
    newText_rect = newText.get_rect()
    if not corner:
        newText_rect.center = position
    else:
        newText_rect.topleft = position
    screen.blit(newText,newText_rect)

    return newText_rect

def UnpackTileOccup():
    unpacked = []
    for i in range(0, len(tileOccup)):
        unpacked.extend(tileOccup[i])

    return unpacked

def RenderTargetPoints(TilePos, RectObj):
    NextPosY, NextPosX = divmod(TilePos, 8)
    
    newpoint = pygame.Rect(0,0,TileSize-40, TileSize-40)
    newpoint.center = RectObj.center
    if tileOccup[NextPosY][NextPosX] == -1:
        pygame.draw.rect(screen,yellow,newpoint)
    else:
        pygame.draw.rect(screen,red,newpoint)
    #detect if target points get clicked
    if pygame.mouse.get_pressed()[0] and cursor.colliderect(newpoint):
        PieceToMove = SelectedData[1]
        print("Target point click detected! Piece ID : " , str(PieceToMove))
        print("En passant status : " , str(EnPassantPossible))
        PrevPosY, PrevPosX = divmod(SelectedData[0], 8)

        if PieceToMove == 5: #EnPassant Condition Checker (WHITE PAWNS)
            testTable = [PieceToMove == 5, PrevPosY - 2 == NextPosY, EnPassantPossible[0][PrevPosX]]
            testTable2 = [PieceToMove == 5, tileOccup[PrevPosY + 1][PrevPosX] == -2]
            print("TestTable (En Passant conditions)" , testTable)
            print("TestTable2 (En Passant Removal conditions)" , testTable2)
            if tileOccup[PrevPosY + 1][PrevPosX] == -2: #Remove enpassant effect
                tileOccup[PrevPosY + 1][PrevPosX] = -1
            elif PrevPosY - 2 == NextPosY and EnPassantPossible[0][PrevPosX]: #Add new enpassant tile
                EnPassantPossible[0][PrevPosX] = False
                tileOccup[NextPosY + 1][NextPosX] = -2
                EnPassantData.append([NextPosY + 1, NextPosX, SelectedData[4]])
            elif tileOccup[NextPosY][NextPosX] == -2: #Remove black pawn after en passant
                tileOccup[NextPosY + 1][NextPosX] = -1
                for data in EnPassantData:
                    if data[0] == NextPosY and data[1] == NextPosX:
                        EnPassantData.remove(data)
                #EnPassantData.remove((NextPosY, NextPosX))

        if PieceToMove == 11: #EnPassant Condition Checker (BLACK PAWNS)
            if tileOccup[PrevPosY - 1][PrevPosX] == -2: #Remove enpassant effect
                tileOccup[PrevPosY - 1][PrevPosX] = -1
            elif PrevPosY + 2 == NextPosY and EnPassantPossible[1][PrevPosX]: #Add new enpassant tile
                EnPassantPossible[0][PrevPosX] = False
                tileOccup[NextPosY - 1][NextPosX] = -2
                EnPassantData.append([NextPosY - 1, NextPosX, SelectedData[4]])
            elif tileOccup[NextPosY][NextPosX] == -2: #Remove white pawn after en passant
                tileOccup[NextPosY - 1][NextPosX] = -1
                for data in EnPassantData:
                    if data[0] == NextPosY and data[1] == NextPosX:
                        EnPassantData.remove(data)
                #EnPassantData.remove((NextPosY, NextPosX))

        

        #Move piece to next position
        tileOccup[PrevPosY][PrevPosX] = -1
        tileOccup[NextPosY][NextPosX] = SelectedData[1]
        Turn = SelectedData[3]

        #Remove outdated en passant tiles
        for index,Enpass in enumerate(EnPassantData):
            if Enpass[2] == SelectedData[4] - 1:
                tileOccup[Enpass[0]][Enpass[1]] = -1
                EnPassantData.remove(Enpass)
                #Formatting = (Y, X, MovesPlaced)


        #reset Selected Data table
        if Turn == "White":
            SelectedData[0], SelectedData[1], SelectedData[2], SelectedData[3] = -1,-1,[-1], "Black"
            #SelectedData[4] += 1 
        else:
            SelectedData[0], SelectedData[1], SelectedData[2], SelectedData[3] = -1,-1,[-1], "White"
            SelectedData[4] += 1   
              
              

def CalculateTargetPoints(): #Calculate legal moves
    WhitePieceIDs = [0,1,2,3,4,5]
    BlackPieceIDs = [6,7,8,9,10,11]
    currentPieceID = SelectedData[1]
    
    def CheckKnightMoves(C_pos, Color):
        #BLACK EQUALS BAD
        
        
        try:
            if Color == "White":
                return not UnpackTileOccup()[C_pos] in WhitePieceIDs
            else:
                return not UnpackTileOccup()[C_pos] in BlackPieceIDs
        except:
            #print(C_coords[0] + Delta_Coords[0], C_coords[1] + Delta_Coords[1])
            return False
        
        

        
    
    SelectedRow, SelectedColumn = divmod(SelectedData[0], 8)
    SelectedData[2] = []
    if currentPieceID == 3 or SelectedData[1] == 9: #White Knight and Black Knight
        c_pos = SelectedData[0]
        KnightWarna = SelectedData[3]
        movementData = ((SelectedColumn > 0, c_pos - 17, c_pos + 15),
                        (SelectedColumn > 1, c_pos - 10, c_pos + 6),
                        (SelectedColumn < 6, c_pos - 6, c_pos + 10),
                        (SelectedColumn < 7, c_pos - 15, c_pos + 17))
        
        for i, data in enumerate(movementData):
            if data[0]:
                for legal_moves in data[1:]:
                    if CheckKnightMoves(legal_moves, KnightWarna):
                        SelectedData[2].append(legal_moves)

        #if SelectedColumn > 0:
        #    legal_moves = (c_pos - 17, c_pos + 15)
        #    for i in legal_moves:
        #        if CheckKnightMoves(i, KnightWarna):
        #            SelectedData[2].append(i)
        #if SelectedColumn > 1:
        #    legal_moves = (c_pos - 10, c_pos + 6)
        #    for i in legal_moves:
        #        if CheckKnightMoves(i, KnightWarna):
        #            SelectedData[2].append(i)
        #if SelectedColumn < 6:
        #    legal_moves = (c_pos - 6, c_pos + 10)
        #    for i in legal_moves:
        #        if CheckKnightMoves(i, KnightWarna):
        #            SelectedData[2].append(i)
        
        #if SelectedColumn < 7:
        #    legal_moves = (c_pos - 15, c_pos + 17)
        #    for i in legal_moves:
        #        if CheckKnightMoves(i, KnightWarna):
        #            SelectedData[2].append(i)
           
    elif currentPieceID == 4: #White Rook
        c_pos = SelectedData[0]
        Ypos, Xpos = divmod(c_pos, 8)
        verticalPieces = []

        for i in range(0,len(tileOccup),1):
            verticalPieces.append(tileOccup[i][Xpos])

        HorizontalMovementData = ((tileOccup[Ypos][Xpos + 1:], 1), (list(reversed(tileOccup[Ypos][:Xpos])), -1)) #(Right movement, Left movement)
        VerticalMovementData = ((list(reversed(verticalPieces[Ypos + 1:])), 1, 1), (verticalPieces[:Ypos], -1, 0)) #(Down movement, Up movement)

        #print(tileOccup[Ypos][Xpos + 1:], c_pos)
        #for i in range(c_pos, len(tileOccup[Ypos][Xpos + 1:]), increment):
        #    print(c_pos + i)

        for data in HorizontalMovementData: #Horizontal movement
            for i, pieceOccup in enumerate(data[0]):
                if pieceOccup in WhitePieceIDs:
                    break
                elif pieceOccup in BlackPieceIDs:
                    SelectedData[2].append(c_pos + (i * data[1]) + data[1])
                    break
                else:
                    SelectedData[2].append(c_pos + (i * data[1]) + data[1])
        


        for data in VerticalMovementData:
            length = 0
            for index, pieces in enumerate(data[0]):
                if pieces in WhitePieceIDs and pieces != -1:
                    length = len(data[0][:i - data[2]])
                    break
            
            for i in range(1, length + 1, 1):
                SelectedData[2].append(c_pos + (i * 8 * data[1]))
            

        for pos in SelectedData[2]:
            if pos == c_pos:
                SelectedData[2].remove(pos)

        
    elif currentPieceID == 5: #White Pawn
        leftEnpass = SelectedColumn > 0 and tileOccup[SelectedRow][SelectedColumn-1] == 11 and tileOccup[SelectedRow - 1][SelectedColumn - 1] == -2
        rightEnpass = SelectedColumn < 7 and tileOccup[SelectedRow][SelectedColumn+1] == 11 and tileOccup[SelectedRow - 1][SelectedColumn + 1] == -2

        if tileOccup[SelectedRow - 1][SelectedColumn] == -1:
            SelectedData[2].append(SelectedData[0] - 8)            
            if SelectedRow == 6 and tileOccup[SelectedRow - 2][SelectedColumn] == -1:
                SelectedData[2].append(SelectedData[0] - 16)

        if (tileOccup[SelectedRow - 1][SelectedColumn - 1] in BlackPieceIDs) or leftEnpass:
            SelectedData[2].append(SelectedData[0] - 9)
        if (SelectedColumn != 7 and tileOccup[SelectedRow - 1][SelectedColumn + 1] in BlackPieceIDs) or rightEnpass:
            SelectedData[2].append(SelectedData[0] - 7)
    elif currentPieceID == 11: #Black Pawn
        EndOfBoard = SelectedRow >= 7
        
        if not EndOfBoard:
            rightEnpass = SelectedColumn > 0 and tileOccup[SelectedRow][SelectedColumn-1] == 5 and tileOccup[SelectedRow + 1][SelectedColumn - 1] == -2
            leftEnpass = SelectedColumn < 7 and tileOccup[SelectedRow][SelectedColumn+1] == 5 and tileOccup[SelectedRow + 1][SelectedColumn+1] == -2

            if tileOccup[SelectedRow + 1][SelectedColumn] == -1:
                SelectedData[2].append(SelectedData[0] + 8)
                if SelectedRow == 1 and tileOccup[SelectedRow + 2][SelectedColumn] == -1:
                    SelectedData[2].append(SelectedData[0]+16)      
            if (tileOccup[SelectedRow + 1][SelectedColumn - 1] in WhitePieceIDs) or rightEnpass:
                SelectedData[2].append(SelectedData[0] + 7)
            if (SelectedColumn != 7 and tileOccup[SelectedRow + 1][SelectedColumn + 1] in WhitePieceIDs) or leftEnpass:
                SelectedData[2].append(SelectedData[0] + 9)
       
    

def renderPieces(pieceID, x, y):
    if pieceID > -1:
        cropSize = 330
        cropX, cropY = pieceID*cropSize, 0
        
        if pieceID >= 6:
            cropX, cropY = cropX - (6*cropSize), cropSize
        crop_area = pygame.Rect(cropX, cropY, cropSize,cropSize)

        try:
            cropped = PieceMap.subsurface(crop_area)
            resized = pygame.transform.scale(cropped,(TileSize - 20, TileSize - 20))
            screen.blit(resized, (x,y))
            piecehitbox = resized.get_rect()
        except ValueError as e:
            print("[Error] Attempt to crop PiecesMap, pieceID = " , pieceID)
            print(e)
    elif pieceID == -2:
        #Enpassant testing
        TestRect = pygame.Rect(x,y,TileSize-30, TileSize-30)
        pygame.draw.rect(screen, red, TestRect)
        MakeText(TestRect.center, "ENPASS.",10,black)
            

def renderboard():
    x,y = 0,0
    isWhite = True
    
    luasboard = screensize[0] * screensize[1]
    for i in range(0,luasboard, TileSize*TileSize):
        Turn = SelectedData[3]
        #i/TileSize/TileSize = piece position on tileOccup
        #get piece id
        Column = tileOccup[int(y/TileSize)]
        ID = Column[int(x/TileSize)]
        
        newtile = pygame.Rect(x,y,TileSize,TileSize)

        #Make white and black tiles
        if isWhite:
            pygame.draw.rect(screen, white, newtile)
            renderPieces(ID,x,y)
        else:
            pygame.draw.rect(screen, blacktile, newtile)
            renderPieces(ID,x,y)
        isWhite = not isWhite

        for v in SelectedData[2]:
            if v == int(i/TileSize/TileSize) and v != SelectedData[0]:
                RenderTargetPoints(int(i/TileSize/TileSize), newtile)
                
        
        #Detect if piece has been clicked
        if newtile.colliderect(cursor):
            #print(selectedPiece)
            IDlimits = "placeholder"
            
            
            if Turn == "White":
                IDlimits = (0,5)
            else:
                IDlimits = (6,11)
            
            if pygame.mouse.get_pressed()[0] and IDlimits[0] <= ID and IDlimits[1] >= ID:
                #AlreadySelect = True
                SelectedData[0] = int(i/TileSize/TileSize)
                SelectedData[1] = ID
                #selected tile, selected piece id
                print("Selected Piece ID = " , str(SelectedData[1])) 
                print("Selected Tile :" , str(SelectedData[0]))
                print("Game History :" , str(MovesHistory))
                CalculateTargetPoints()
        
        x += TileSize
        if x >= screensize[1]:
            x = 0
            y += TileSize
            isWhite = not isWhite


menuBG = pygame.Rect((screensize), (300,screensize[1]))

loop = True
 
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                print("Selected Data : " , SelectedData)
                print("En Passant Data : " , EnPassantData)
                print("\n")
        if event.type == pygame.MOUSEBUTTONDOWN and cursor.colliderect(githublinkHitbox):
            webbrowser.open("https://github.com/sidharta310312")
    
    screen.fill(white)
    
    renderboard()

    if SelectedData != [-1, -1]:
        CalculateTargetPoints()
    
    cursor.center = pygame.mouse.get_pos()
    pygame.draw.rect(screen, red, cursor)

    #Create the menu
    pygame.draw.rect(screen, gray, menuBG)

    Turn = SelectedData[3]
    MakeText((screensize[0] + 150, 40),f"{Turn} to move", 40, black)
    MakeText((screensize[0] + 150, 70),f"Moves made : {SelectedData[4]}", 10, black)

    if SelectedData[1] > 0:
        pieceNames = ("King", "Queen", "Bishop", "Knight", "Rook", "Pawn")
        currentPiece = pieceNames[SelectedData[1] % len(pieceNames)]
        if SelectedData[1] >= 6: #Black pieces
            currentPiece = "Black " + currentPiece
        else:
            currentPiece = "White " + currentPiece

        tuhRect = MakeText((0,0), f"Selecting : " + currentPiece, 20, red)
        tuhRect.x, tuhRect.y = cursor.center

    MakeText((screensize[0], screensize[1] - 80),f"PythonChessPlayer-unfinished\nMade by sidharta310312 on GitHub", 15, black, corner=True)
    githublinkHitbox = MakeText((screensize[0], screensize[1] - 35),f"Open Github Profile", 20, (201, 81, 12) if not cursor.colliderect(githublinkHitbox) else (255, 165, 0), corner=True, thicc=True)
    if cursor.colliderect(githublinkHitbox):
        pygame.draw.rect(screen, (255, 165, 0), ((githublinkHitbox.bottomleft[0], githublinkHitbox.bottomleft[1] - 7), (githublinkHitbox.width, 3)))
    
    pygame.display.flip()
 
 
pygame.quit()
sys.exit()
