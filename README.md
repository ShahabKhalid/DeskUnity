# DeskUnity v1.0
-----------------------------------

## About
DeskUnity is a mouse, keyboard and other resource sharing app between multiple computers connected through 
WAN or LAN both. DeskUnity prefer LAN connection over WAN in case it find both. 

## Current Features

- Mouse Sharing
- Keyboard Sharing
- ClipBoard Sharing

## Current Limits / Cons

- Only Windows system can act as server ( Computer that can sharing resources )
- Only two computers is supported right now ( 1 Server and 1 Client )
- Computer with multiple screens is not supported yet
- You can positions your computer ( Server computer is always positioned left and other at right )

## Bugs

- NIL

## Instructions

- Clone the repository 
- Install requirements `pip install -r requirenments.txt`
- Install pyHook, Recommended pyHook3 ( With Some major fixes for Python3 ) https://github.com/ShahabKhalid/pyHook3    
- Run the main.py `python main.py`
- **Note** : Computer in which DeskUnity is run first with start as Server and other will connect to it automatically.


**Please let me know about any bugs you face and also any suggestions you want to see in next versions.**

## Next Version Plans (Priority from top to bottom)

- Lock Sync
- Client will be to share resources too
- Multiple Computers support
- Multiples Screens support
- Others 