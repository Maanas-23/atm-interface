import csv
import random
from getpass import getpass
import hashlib, uuid


def get_csv_content():
    with open('users.csv') as f:
        csv_r = csv.reader(f)
        l = list()
        for i in csv_r:
            l.append(i)
        return l


def update_balance(card, amount):
    l = get_csv_content()
    code = 0
    with open('users.csv', 'w') as f:
        csv_w = csv.writer(f)
        for i in l:
            if i[2] == card:

                if int(i[-1]) + amount < 0:
                    code = 2
                    print("INSUFFICIENT FUNDS")
                else:
                    i[-1] = str(int(i[-1]) + amount)
                    code = 1

            csv_w.writerow(i)

    return code


def hashed_pin(pin):
    salt = uuid.uuid4().bytes
    hashed_password = hashlib.sha512(pin + salt).digest()
    return hashed_password


class Atm:
    def __init__(self):
        self.logged_in = False
        self.details = list()

    def prompt(self):
        divider = ''
        for i in range(30): divider += '-'

        print(divider)

        if not self.logged_in:
            print("1. Log in\n2. Sign up")
        else:
            print("1. Transfer to account\n2. Deposit\n3. Withdraw\n4. Show balance")
        print("0. Exit")

        x = int(input())
        print(divider, divider, sep='\n')
        return x

    def signup(self):
        l = get_csv_content()
        name = input("Enter your name : ")

        pin = ''
        while len(pin) != 4:
            pin = input("Enter a 4 digit pin : ")

        while 1:
            ac_no = random.randint(10 ** 7, 10 ** 8 - 1)
            is_valid = True
            for i in l:
                if i[1] == ac_no:
                    print("invalid ac number")
                    is_valid = False
            if is_valid:
                break

        while 1:
            card_no = random.randint(10 ** 15, 10 ** 16 - 1)
            is_valid = True
            for i in l:
                if i[2] == card_no:
                    print("invalid card number")
                    is_valid = False
            if is_valid:
                break

        with open('users.csv', 'a', newline='\n') as f:
            csv_w = csv.writer(f)
            csv_w.writerow([name, ac_no, card_no, pin, 0])

        card = str()
        for i in range(4, 15, 4):
            card += str(card_no)[i - 4:i] + '-'
        card += str(card_no)[-4:]
        print(f"Your account has been created with account number : {ac_no}\nand card number : {card}")
        self.details = [name, str(ac_no), str(card_no), str(pin), 0]
        self.details[-1] = 0
        print("Successfully logged in")
        self.logged_in = True

    def login(self):
        card_no = input("Enter card number : ")
        card_no = card_no.replace(' ', '')
        card_no = card_no.replace('-', '')

        pin = input("Pin : ")

        l = get_csv_content()

        for i in l:
            if i[2] == card_no:
                if i[3] == pin:
                    self.details = i
                    self.details[-1] = int(i[-1])
                    print("Successfully logged in")
                    self.logged_in = True
                else:
                    print("incorrect pin")
                return 1
        print("Card not found")
        return 0

    def main(self):
        x = self.prompt()

        while x:
            if not self.logged_in:  # Not logged in case

                if x == 1:  # Login
                    self.login()

                elif x == 2:  # Sign up
                    self.signup()

            else:  # Logged in case

                if x == 1:  # Account transfer
                    amount = int(input("Enter amount to transfer : "))
                    card_no = input("Enter card number to transfer to :")
                    transferred = update_balance(card_no, amount)
                    if transferred == 1:
                        t = update_balance(card=self.details[2], amount=-amount)
                        if t == 2:
                            update_balance(card_no, -amount)
                        else:
                            self.details[-1] -= amount

                    else:
                        print("Card not found. Transfer failed.")

                if x == 2:  # Deposit
                    amount = int(input("Enter amount to deposit : "))
                    update_balance(card=self.details[2], amount=amount)
                    self.details[-1] += amount
                    print(f"Successfully deposited Rs. {amount}")

                if x == 3:  # Withdraw
                    amount = int(input("Enter amount to withdraw : "))
                    transfer = update_balance(card=self.details[2], amount=-amount)
                    if transfer != 2:
                        self.details[-1] -= amount
                        print(f"Successfully withdrew Rs. {amount}")
                    else:
                        print("WITHDRAWAL FAILED")

                if x == 4:  # Show Balance
                    print(f"Your balance is {self.details[-1]}")

            x = self.prompt()


if __name__ == '__main__':
    atm = Atm()
    atm.main()
