from UnionBarrie import un_ba
from BarrieUnion import ba_un
from CustomDirections import custom_mode
import requests as r
from inquirer.themes import GreenPassion

def pick_mode():
    print("==================================================================")
    print("\nWelcome to the GO Train Schedule Finder!\n")
    print("1. Barrie to Union\n2. Union to Barrie\n3. Custom Mode\n")
    print("==================================================================\n")

    mode = input("Enter Mode:\t")
    mode = str(mode)

    if mode == '1':
        ba_un()

    if mode == '2':
        un_ba()

    if mode == '3':
        custom_mode()

    elif mode != '1' and mode != '2' and mode != '3':
        print('Invalid Input')
        pick_mode()
pick_mode()
