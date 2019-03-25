#Question 3:
#Witcher inventory

#Assumptions:
#There is at least 2 of each item in stock, so your extra piece can be
#the same as a piece you already have.

#You have copied the contents of "Witcher Inventory.pdf" into a text file
#called witcher_inv.txt, which is saved in the same folder as witcher_proj.py

#This class is used to store data from each item from the shop
class Armor(object):
    def __init__(self, atype, name, price, av):
        self.t = str(atype),     #atype = armor type
        self.n = str(name),
        self.p  = price
        self.av = av

    def get_type(self):
        return str(self.t)[2:-3]

    def get_name(self):
        return str(self.n)[2:-3]

    def get_price(self):
        return self.p

    def get_av(self):
        return self.av

class Witcher(object):
    def __init__(self):

        #The "nude" armor has -1 armor val to avoid a div by zero error
        self.helm = None
        self.chest = None
        self.leg = None
        self.boot = None
        self.extra = None
        self.wallet = 300

    def get_helmet(self):
        return self.helm.get_name()

    def get_chest(self):
        return self.chest.get_name()

    def get_leggings(self):
        return self.leg.get_name()

    def get_boots(self):
        return self.boot.get_name()

    def get_extra(self):
        return self.extra.get_name()

    def get_av(self):
        return self.helm.get_av() \
               + self.chest.get_av() \
               + self.leg.get_av() \
               + self.boot.get_av() \
               + self.extra.get_av()\


    def get_wallet(self):
        return self.wallet

#Causes Geralt to buy new armor if its value > current armor
#or if he doesn't have any armor on.
    
    def sort(self, oldArmor, armor):

        if oldArmor == None:
            oldArmor = armor
            self.wallet -= int(armor.get_price())
            
        else:
            #Price to armor val ratio of current armor
            newRate = int(armor.get_price())/int(armor.get_av())
            #Price to armor val ratio of prospective new armor
            oldRate = int(oldArmor.get_price())/int(oldArmor.get_av())

            #if the new armor's ratio is narrower than the current armor's, swap.
            if newRate < oldRate:
                self.wallet += oldArmor.get_price()
                
                oldArmor = armor
                self.wallet -= armor.get_price()
        return oldArmor

    

    
            
        

##### STOCKING SECTION ############
### Fills shop list with items ####

#This list will be filled with all armor items.
shop = []

#Iterate through the inventory document,
#recording data of item on each line.
file = open("witcher_inv.txt", "r")

for line in file:

    #as a list of words, the line is easier to read.
    words = line.split()

    atype = words[0]

    name = ""
    for x in words[1:-2]:
        name = name + x + " "

        
    price = int(words[-2])
    
    av = int(words[-1])

#Create the new item and append to the shop list.
    shop.append(Armor(atype, name, price, av))

file.close()
###### END STOCKING SECTION #########


#Now, we create a Witcher object and take him shopping
Geralt = Witcher()

for item in shop:

    #every time he sees an item with a better
    #price/av ratio than his current item, he replaces
    #his current item.
    if item.get_type() == "Helmet":
        Geralt.helm = Geralt.sort(Geralt.helm, item)

    if item.get_type() == "Chest":
        Geralt.chest = Geralt.sort(Geralt.chest, item)

    if item.get_type() == "Leggings":
        Geralt.leg = Geralt.sort(Geralt.leg, item)

    if item.get_type() == "Boots":
        Geralt.boot = Geralt.sort(Geralt.boot, item)
        
#Here, Geralt buys the best quality armor he can afford.

#Starts off with armor where av=0. Helps with comparing
#current armor to new armor.
shopping_cart = Armor("N/A", "Empty cart", 0, 0)

for item in shop:
    #Here, Geralt selects the best armor he can afford...
    if int(item.get_price()) <= int(Geralt.get_wallet()):
        
        if item.get_av() > shopping_cart.get_av():
            
            shopping_cart = item
            
#...and then buys it here.
Geralt.extra = Geralt.sort(Geralt.extra, shopping_cart)

print("Geralt's Helmet:\t" + Geralt.get_helmet())
print("Geralt's Chest:\t\t" + Geralt.get_chest())
print("Geralt's Leggings:\t" + Geralt.get_leggings())
print("Geralt's Boots:\t\t"+ Geralt.get_boots())
print("Geralt's Extra item:\t" + Geralt.get_extra())

print("\nGeralt's Armor Val:\t\t" + str(Geralt.get_av()))
print("Geralt's leftover funds:\t" + str(Geralt.get_wallet()))

dummy_input = input("\nEnter any input to close the program! ")

#About this program:
#To implement the solution, I first came with a sort of list of "tools" I would need to make.
#Conceptually, I broke the project down into objects. You can see below where I partially
#typed out my thought process.

#Then I came up with the algorithm to get the highest armor.
#After some paper-and-pencil testing,#I decided that, for this inventory, it would be
#sufficient for Geralt to just first focus on buying the most cost-effective boots,
#chestpiece, helmet, and leggings, and then splurge on the extra item since he could
#blow all his coin on the item with the highest armor value.
#For the first four armor pieces, he just bought the first items he saw, and then
#traded those items back in to buy a different one every time he saw an item with a
#better price-to-armor-value ratio. For the "extra" item, I gave him a "shopping cart"
#so he didn't have to spend any crowns until he found the item he knew he wanted.
#He simply scanned through the shop, placing the item with the highest av in his budget
#in the cart. After he scanned the whole shop, he bought the item.

#This may not work for other inventories, though; for example, if this inventory included
#a chest piece worth 1 crown and an armor value of 1, Geralt would have bought that chest armor,
#and even if he spent his remaining crowns on the "extra" item with the highest armor val,
#he would have a lower total AV than if he'd just bought the Chestpiece of Vachon twice. 
#I might be able to protect against this if I made sure Geralt only bought items within
#1 standard deviation below the average item's armor value. However, given the inventory
#selection you gave me, that would be overkill.


#Step 1: Create...
#   inventory -- Object
#       Has chest, leggings, helmet, boots, wildcard

#   Shop
#       List of items


#   Item
#       Has
#           Name
#           Type
#               Chest, leggings, helmet, boots
#           Price
#           armor value

#   wallet

#Step 2: Evaluate price
# How do you determine best combination?
# Avg 60c per item,
# Maximize AV/Price or minimize Price/AV

##Chest Armor de Jandro 67 22
##Chest Chestpiece of Vachon 64 23     This is objectively better. Good reference for testing.

    

        


        







        
