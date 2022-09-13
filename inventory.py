# Import to make tables for viewing shoe objects in multiples.
# I still refer back to the __repr__ for displaying individual search returns.
from tabulate import tabulate


class Shoe(object):

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    # Used __repr__ instead of __str__ as I found it more functional
    # for implementing my string version of object output.
    def __repr__(self):
        return (
            f"Shoe code:                  {self.code}"
            f"\n---------------------------------------------"
            f"\nCountry of origin:          {self.country}\n"
            f"Product Name:               {self.product}\n"
            f"Cost:                       R {self.cost}\n"
            f"Quantity:                   {self.quantity}\n"
            f"Total current value:        R {(self.quantity * self.cost)}\n"
            f"---------------------------------------------\n\n"
            )

# CLASS ENDS HERE
# FUNCTIONS START HERE


# Function for reading the text file and importing the shoe data
# and appending each Shoe object to the shoe_list
def read_shoes_data():
    global shoe_list
    shoe_list = []  # Emptying the list so as to not create duplicates.
    with open('inventory.txt', 'r+') as file:
        next(file)  # Skip for the first line.
        for line in file:
            data = line.split(',')
            data[3], data[4] = int(data[3]), int(data[4])
            new_shoe = Shoe(data[0], data[1], data[2], data[3], data[4])
            shoe_list.append(new_shoe)


# Function to create a new Shoe object.
# accounted for not receiving an integer on the cost, or if input <= 0
# accounted for not receiving an integer on the quantity as well
# After I receive all my inputs, I create the object,
# Append it to the shoe_list, and append it to the text file.
# I also create a printout of the object for viewing,
# an option to create another object,
# or a choice to return to main menu.
def capture_shoes():
    print("\nCapturing a new shoe: \n")
    new_country = input("Please provide a country of origin: ")
    new_code = input("Please provide a shoe code: ")
    new_product = input("Please provide a product name: ")
    while True:
        try:
            new_cost = int(input("Please provide a cost per shoe: "))
            if new_cost <= 0:
                print('\nYou cannot book a shoe with 0 cost\n')
            else:
                break
        except ValueError as ve:
            print("\nThat's not a valid number.\n")
    while True:
        try:
            new_quantity = int(input("Please provide the quantity counted: "))
            if new_quantity <= 0:
                print('\nYou counted 0 shoes to book in? Impressive...\n')
            else:
                break
        except ValueError as ve:
            print("\nThat's not a valid number.\n")
    new_shoe = Shoe(new_country,
                    new_code,
                    new_product,
                    new_cost,
                    new_quantity)
    shoe_list.append(new_shoe)
    # Writing the new object to the text file.
    with open('inventory.txt', 'a+') as file:
        file.write('\n{},{},{},{},{}'.format(new_shoe.country,
                                             new_shoe.code,
                                             new_shoe.product,
                                             new_shoe.cost,
                                             new_shoe.quantity))
    print("\nNew Shoe has been created and added to stock sheet.\n\n"
          f"{shoe_list[-1]}")
    # Choice to input another shoe object
    while True:
        second_choice = input("Press 1 if you'd like to add another shoe\n"
                              "or press menu if you'd like to return to menu:")
        if second_choice == '1':
            capture_shoes()
        # Choice to return to menu
        if second_choice == 'menu':
            print('\n', end='')
            break
        else:
            print("\nYou have selected an invalid option.\n")


# Function to view all the shoes objects in a tabular format.
# provided a counter if you tried to view before importing the text file
def view_all():
    new_list = [['Country', 'Code', 'Product', 'Cost', 'Quantity']]
    # Counter for not importing first
    if len(shoe_list) == 0:
        print("""\nYou haven't imported the list of shoes yet.
returning to main menu...\n""")
        menu()
    for i in shoe_list:
        temp_shoe = [i.country, i.code, i.product, i.cost, i.quantity]
        new_list.append(temp_shoe)
    # Used tabulate import to create view.
    table1 = tabulate(new_list, headers='firstrow', tablefmt='grid')
    print(table1 + '\n')


# Function to restock the object with the lowest value
# provided a counter if you tried to restock before importing text file.
# used list comprehension generation for finding the lowest quantity
# Then input variable for receiving new quantity to update to.
# I couldn't find a way without os import or regex to update a single line
# So I just used the shoe_list to rewrite the entire file everytime
# a shoe value changes.
# Finally, I used truncate() and tell() to remove the last new line in
# my text file.
# Code is also written in such a format that if you had multiple shoes
# at that lowest value, it would update all of them to new input value.
def re_stock():
    if len(shoe_list) == 0:
        print("""\nYou haven't imported the list of shoes yet.
returning to main menu...\n""")
        menu()
    # used list comprehension generation here to just use 1 line.
    lowest_q = min(x.quantity for x in shoe_list)
    new_q = input("What do you want to update the quantity to: ")
    for i in shoe_list:
        if i.quantity == lowest_q:
            i.quantity = new_q
    with open('inventory.txt', 'w+') as file:
        for item in shoe_list:
            file.write('{},{},{},{},{}\n'.format(item.country,
                                                 item.code,
                                                 item.product,
                                                 item.cost,
                                                 item.quantity))
        # removing the new line from the last item we write to the file.
        # If you don't do this, import creates an issue.
        file.truncate(file.tell()-2)


# Function to search for a shoe by code.
# Counter for not importing first provided.
# Used a boolean check variable to return a different output
# If you entered a non-existent shoe code.
def search_shoe():
    if len(shoe_list) == 0:
        print("""\nYou haven't imported the list of shoes yet.
returning to main menu...\n""")
        menu()
    else:
        while True:
            search_choice = input("Input the code of the shoe you need: ")
            bool_check = False
            for item in shoe_list:
                if item.code == search_choice:
                    bool_check = True
                    print('\n', item)
                    menu()
            # Used bool_check to return output for invalid code.
            if not bool_check:
                print("\nCouldn't find that code. Try again.\n")


# Function to print out the costings of each total shoe object
# Referred back to tabulate form for display.
# Counter for using before import provided.
def value_per_item():
    if len(shoe_list) == 0:
        print("""\nYou haven't imported the list of shoes yet.
returning to main menu...\n""")
        menu()
    else:
        temp_val_list = [['Product', 'Cost per unit',
                          'Quantity', 'Total cost']]
        for i in shoe_list:
            temp_shoe = [i.product, i.cost, i.quantity, (i.cost * i.quantity)]
            temp_val_list.append(temp_shoe)
        table1 = tabulate(temp_val_list, headers='firstrow', tablefmt='grid')
        print(table1 + '\n')


# Function for highest quantity item.
# counter for using before import provided.
# used list comprehension generator again for finding the max object qty
# Also wrote the output in such a way that if you had multiple shoes
# at max value it would display them all.
def highest_qty():
    if len(shoe_list) == 0:
        print("""\nYou haven't imported the list of shoes yet.
returning to main menu...\n""")
        menu()
    else:
        highest_q = max(x.quantity for x in shoe_list)
        for item in shoe_list:
            if item.quantity == highest_q:
                print('\n', item)
                print("This item will be up for sale!")


# Main menu function with exit option and all choices coded from to
# functions
def menu():
    while True:
        user_choice = input("""Welcome, what would you like to do:\n
Import data for shoes             - import
Capture a new shoe                - capture
View all shoes                    - view
Restock the lowest quantity shoe  - restock
Lookup specific shoe              - lookup
View total shoe value             - value
Lookup shoe with highest quantity - highest

Choice:""").lower()

        if user_choice == 'import':
            read_shoes_data()
            print("\nData imported. Returning to Main Menu...\n")

        elif user_choice == 'capture':
            capture_shoes()

        elif user_choice == 'view':
            view_all()

        elif user_choice == 'restock':
            re_stock()

        elif user_choice == 'lookup':
            search_shoe()

        elif user_choice == 'value':
            value_per_item()

        elif user_choice == 'highest':
            highest_qty()

        else:
            print("Incorrect option. Please try again.\n")


shoe_list = []

menu()
