# PythonChessPlayer-unfinished
An unfinished source code on my attempt on trying to recreate chess using Python

The only programmed movable pieces are Pawns, Knights, and Rooks. Other pieces don't have a moving ability because they aren't programmed yet (PS : The rook piece is a bit buggy, so expect glitches when interacting with the rook)

## Required third-party library dependencies
- pygame (Run ```pip install pygame-ce``` in command prompt to install, pip required for installation process)
- Nothing else

##Source code config explanation
- line 54 : The ```tileOccup``` 2D array stores every piece position on-board (each piece is represented as an ID ranging from -2 to 11)
- line 36 : Contains directory of PiecesMap.png, this file is heavily required for rendering the chess pieces during run-time
- line 175 : The ```CalculateTargetPoints()``` function is required to find out the legal positions of the currently-selected chess piece
- line 102 : The ```RenderTargetPoints(TilePos, RectObj)``` function is required to render the possible legal positions of the currently-selected chess piece. The first parameter ```TilePos``` is an int value containing the position of the currently-selected chess piece on ```tileOccup```, and ```RectObj``` is a Rect() object from the pygame library that acts like the cursor hitbox of the currently-selected chess piece

##Extra notes from dev
_"Due to how messy the source code is (and the fact that I havent touched this project for a while, which results to me forgetting how almost everything works here), a remake of this Chess Program will be made soon" -sidharta310312_
