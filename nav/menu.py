#! /usr/bin/env python3
# coding: utf-8


class Menu:
    """
    Menu management
    """
    def __init__(self):
        self.menu_choice = self.menu_choice()

    def menu_choice(self):
        """
        Main menu of the application
        """
        print(">> Welcome !")
        print(">> What do you want to do ?\n")
        print("1 | Find a substitute")
        print("2 | Consult my substitutes history\n")

        menu_choice = 0

        while True:
            try:
                while (menu_choice < 1) or (menu_choice > 2):
                    menu_choice = int(input(">> Type your choice and press ENTER : \n"))
                break
            except ValueError:
                print(">> Please, type in a number.")

        return menu_choice

    def back_to_menu_or_exit(self):
        """
        Saves the saving choice of user (yes or no)
        """
        while True:
            self.menu_choice = input("\n>> Type M to go back to main menu, "
                                     "or Q to leave the application, and the press ENTER : \n").strip().upper()
            if self.menu_choice == "M":
                break
            elif self.menu_choice == "Q":
                print("See you next time !")
                exit()
            else:
                continue
