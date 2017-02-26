# -*- coding: utf-8 -*-
import random
import sys
#list stores all the names of the properties in order
names = ['GO','Medit.', 'Baltic','Chance','Oriental','Vermont',
'Just Visitng', 'States','Virginia','Com. Chest','St.James','New York', 'Free Parking', 'Kentucky',
'Indiana','Chance','Atlantic','Ventnor','JAIL', 'Pacific', 'N Carolina',
'Com. Chest', 'Park Place', 'Boardwalk']
#list of houses owned on each property. index of list = pos of property on board
houses = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#list of player number that owns the property (0 if unowned), index of list = pos of property on board
owned = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#dictionary stores buying price of properties
prices = {'GO':200,'Medit.': 60, 'Baltic':60,'Chance':0,'Oriental':100,'Vermont':110,
'Just Visitng':0, 'States':140,'Virginia':160,'Com. Chest':0,'St.James':190,'New York':200, 'Free Parking':0, 'Kentucky':240,
'Indiana':240,'Chance':0,'Atlantic':280,'Ventnor':300,'JAIL':0, 'Pacific':350, 'N Carolina':360,
'Com. Chest':0, 'Park Place':370, 'Boardwalk':400 }
#dictionary of different chance cards that are used in chancer
chance = {1: "Advance to go. Collect $200.", 2: "Pay poor tax of $15 dollars", 3:"You have been elected Chairman of the Board - Pay the other player $50", 4:"From sale of stock you get $45", 5: "You have won second prize in a beauty contest. Collect $10", 6: "Doctor's fee. Pay $50"}
#p = [character,balance,properties owned, properties mortgaged]
p1 = ["░",1500,0,[],[]]
p2 = ["▓",1500,0,[],[]]
players = [p1,p2]
#the number of turns player one or two has been in jail.
jturns = {1:0,2:0}
#the two die that the players roll. Updates every turn.
d1=0
d2=0
#Takes in the player number and returns the other player number (other_player(1) returns 2 and other_player(2) returns 1)
def other_player(num):
	if num==1:
		return 2
	else:
		return 1
#rent takes in the pos of porperty and returns the price of the rent. If there are houses, the players are charged more for rent.
def rent(pos):
	if names[pos] in players[0][4] or names[pos] in players[1][4]:
		print("This property is currently mortgaged. The rent is $0.")
		return 0
	if houses[pos]!=0:
		return (prices[names[pos]]/10)*(houses[pos]+1)
	else:
		return (prices[names[pos]]/10)
#this function checks whether or not the two randomly selected dice are equal and if they are, the player goes again.
def double(playnum):
	if d1==d2:
		print("Congratulations! You have rolled a double, you may roll again.")
		player(playnum)
#This chooses a random chance or community chest card (one of 6 random cards is chosen) and runs what it does
def chancer(num):
	n = random.choice([1,2,3,4,5,6])
	print(chance[n])
	if n==1:
		players[num-1][2]=0
		players[num-1][1]+=200
		print("$200 was added to your balance. Your current balance is $" + str(players[num-1][1]))
	if n==2:
		players[num-1][1]-=15
		print("$15 was subtracted from your balance. Your current balance is $" + str(players[num-1][1]))
	if n==3:
		players[num-1][1]-=50
		players[other_player(num)-1][1]+=50
		print("You have lost $50 dollars. Player 2 has gained $50 dollars.")
	if n==4:
		players[num-1][1]+=45
		print("$45 was added to your balance. Your current balance is $" + str(players[num-1][1]))
	if n==5:
		players[num-1][1]+=10
		print("$10 was added to your balance. Your current balance is $" + str(players[num-1][1]))
	if n==6:
		players[num-1][1]-=50
		print("$50 was subtracted from your balance. Your current balance is $" + str(players[num-1][1]))
#This allows players to mortgage and adds mortgaged properties to a new list, removing it from the list of properties the player owns
def mortgage(playnum):
	if len(players[playnum-1][3])>0:
		print("Which property would you like to mortgage?")
		print("You currently own these properties: "+ str(players[playnum-1][3]))
		print ("Please type the name of the property exactly as it appears on the gameboard.")
		i = input()
		if i in players[playnum-1][3]:
				players[playnum-1][3].remove(i)
				players[playnum-1][4].append(i)
				players[playnum-1][1]+=prices[i]/2
				print("You successfully mortgaged "+i+". $"+str(prices [i]/2)+" was added to your account.")
				print("Your current balance is $" +str(players[playnum-1][1])+".")
				options(playnum)
		else:
			print ("Invalid property name or You do not own that property.")
			options(playnum)
	else:
		print("You do not own any properties to mortgage.")
		options(playnum)

#If you have mortgaged a property, this checks the list of mortgaged properties and allows you to unmortgage your properties for the original price of the property
def unmortgage(playnum):
	if len(players[playnum-1][4])>0:
		print ("Which property would you like to unmortgage?")
		print("You currently have these properties mortgaged: "+ str(players[playnum-1][4]))
		print ("Please type the name of the property exactly as it appears on the gameboard.")
		i = input()
		if players[playnum-1][1]>=prices[i]/2:
			if i in players[playnum-1][4]:
				players[playnum-1][4].remove(i)
				players[playnum-1][3].append(i)
				players[playnum-1][1]-=prices [i]/2
				print(i+" has been unmortgaged. Your current balance is $"+ str(players[playnum-1][1]))
			else:
				print("Invalid property name or Property is not mortgaged.")
				options(playnum)
		else:
			print("You do not have enough money to unmortgage this property.")
			options(playnum)

#This allows you to build houses on properties you own (asking how many houses you want to build and allowing you to build up to four).
def house(playnum):
	if len(players[playnum-1][3])!=0:
		print()
		print("Which property would you like to build house(s) on?")
		print("You currently own these properties: "+ str(players[playnum-1][3]))
		print ("Please type the name of the property exactly as it appears on the gameboard.")
		i = input()
		if i in players[playnum-1][3]:
			print("How many houses would you like to build on "+i+"? (Max 4)")
			print("There are "+str(houses[names.index(i)])+" houses on this property.")
			print("Each house for "+i+" costs $" +str(prices[i]/2)+ ".")
			h= input()
			if (int(h) >= 0 and int(h) <= 4) and ((houses[names.index(i)]+int(h))<=4):
				houses[names.index(i)] +=int(h)
				players[playnum-1][1]-=(prices[i]/2)*int(h)
				print(i+" contains "+str(houses[names.index(i)])+" houses now. Your current balance is $" + str(players[playnum-1][1]))
			else:
				print("Invalid number or number of houses exceeds 4.")
				house(playnum)
		else:
			print("Invalid property name or You do not own that property.")
			house(playnum)
	else:
		print("You do not own any properties.")
		options(playnum)
#This simply checks if a specific property is owned.
def if_owned(pos,n):
	if owned[pos]== 0:
		return False
	else:
		return True
#After a player goes, this checks if they have negative money and if they do, it asks if they would like to mortgage a property in order to have a balance greater or equal to 0. If they choose not to mortgage, the game ends and they lose.
def lose(num):
	if players[num-1][1] < 0:
		if len(players[num-1][3])!=0:
			print("Player "+str(num)+", you currently have a negative balance. If you end you turn, you will lose. Would you like to mortgage any of your property?")
			print("Type Yes (y) or No (n)")
			i =input()
			if i == "yes" or i == "y" or i == "Yes" or i == "Y":
				mortgage(n)
		else:
			print("Player "+str(num)+", you have negative balance and no properties to mortgage. ")
	if players[num-1][1] < 0:
		print("I'm sorry but Player " +str(num)+ " you lose. Player " + str(other_player(num)) + " wins.")
		print("CONGRATULATIONS PLAYER "+str(other_player(num))+"!")
		sys.exit("GAME OVER. Thanks for playing COMMAND PROMPT MONOPOLY with the courtesy of Fatih Ak and Arash Nassirinia.")
#This is a very important chunk of code that is used after a person rolls their dice. It allows a person to choose to mortgage, unmortgage, build a house, or end their turn, calling the function that is associated with each respective option.
def options(n):
	print()
	print("Would you like to Mortgage one of your properties (m), Unmortgage a property(u), Build a house(h), or End your turn(e)?")
	i=input()
	if i == "m" or  i == "mortgage" or i == "M" or i == "Mortgage":
		mortgage(n)
		options(n)
	if i == "u" or i == "U" or i == "unmortgage" or i == "Unmortgage":
		unmortgage(n)
		options(n)
	if i == "h" or i == "H" or i == "House" or i == "house":
		house(n)
		options(n)
	if i == "e" or i == "E" or i == "End" or i == "end":
		double(n)
		lose(n)
		player(other_player(n))
	else:
		print("That is not one of the options. Please try again.")
		options(n)

#This cehcks where a person is on the board. If they own it, it tells them and nothing happens. If the other player owns it, they are charged rent. If you are on go, you get $200.If it's unowned, it gives the option to buy the property.
def move(pos, n):
	if pos==0 or pos==24:
		players[n-1][1]+= 200
		print("$200 was added to your bank. Your current balance is $" + str(players[n-1][1]))
		options(n)
	if pos==3 or pos==9 or pos==15 or pos==21:
		chancer(n)
		options(n)
	if pos==6 or pos==12:
		print("Nothing happens.")
		options(n)
	if pos==1 or pos==2 or pos==4 or pos==5 or pos==7 or pos==8 or pos==10 or pos==11 or pos==13 or pos==14 or pos==16 or pos==17 or pos==19 or pos==20 or pos==22 or pos==23:
		if if_owned(pos,n) == True:
			if owned[pos]==n:
				print("You own this property. Nothing happens.")
				options(n)
			else: 
				print("Your opponent owns this property. You will pay rent of $" +str(rent(pos))+".")
				players[n-1][1]-=rent(pos)
				print("Your current balance is $" +str(players[n-1][1])+".")
				options(n)
		else:
			if players[n-1][1]>=prices[names[pos]]:
				print("This property is unowned, would you like to buy it for $"+str(prices[names[pos]])+"? Type Yes(y) or No(n).")
				i = input()
				if i == "yes" or i == "y" or i == "Yes" or i == "Y" or i == "YES":
					owned[pos]=n
					players[n-1][1]-=prices[names[pos]]
					players[n-1][3].append(str(names[pos]))
					print("You have bought "+names[pos]+". Your current balance is now $" +str(players[n-1][1])+"." )
					options(n)
				elif i == "no" or i == "N" or i == "No" or i == "n":
					options(n)
				else:
					print("That was not one of the options.")
					options(n)
	if pos==18:
		print("You have landed on Jail and you will be inactive for 4 turns unless you pay $50 in your next turn.")
		player(other_player(n))
#This keeps a person in jail for three turns. if they are in jail, it gives them the option to get out of jail for $50. If they roll doubles in three turns, they can leave for free and if it is their fourth turn there, they are automatically charged $5o and leave.
def jail(num):
	if players[num-1][2] == 18:
		jturns[num] += 1
		if jturns[num] <=3:
			if d1==d2:
				print ("Congratulations. You rolled a double and you are now out of jail.")
				jturns[num] = 0
			else:
				print ("You are still in jail. You have been in jail for " +str(jturns[num])+ " turns.")
				print ("Would you like to pay $50 to leave jail? Yes (y) or no (n)")
				i = input()
				if i == "no" or i == "N" or i == "No" or i == "n":
					player(other_player(num))
				if i == "y" or i == "Y" or i == "yes" or i == "Yes":
					players[num-1][1]-=50
					print ("You are now out of jail and you have been charged $50. Your balance is now $" +str(players[num-1][1])+ ".")
					jturns[num] = 0
				else:
					print ("That is not one of the options. Try again.")
					jail(pos,num)
		else:
			print("You have been in jail for 3 turns.")
			players[num-1][1]-=50
			print ("You are now out of jail and you have been charged $50. Your balance is now $" +str(players[num-1][1])+ ".")
			jturns[num] = 0
#This puts everything together. It takes in which player's turn it is and first pritns the board. Then it tells the player to roll, showing the dice and the number they roll.
#It also calls jail which checks whether or not they are in jail and runs the jail program. It also checks if they pass go and adds $200 to their balance if they do.
#Finally, this function uses recursion by calling the other player in the end and keeps calling itself until one player loses.
def player(num):
	global d1
	global d2
	print_board()
	print("Player "+str(num)+", your balance is $"+str(players[num-1][1])+". You are currently at "+str(names[players[num-1][2]])+".")
	print("You currently own these properties: "+ str(players[num-1][3]))
	print("What would you like to do? Roll Dice (r)?")
	i=input()
	while i!= "Roll" and i != "roll" and i != "r" and i != "Roll Dice":
		print ("That is not one of the options. Try again.")
		i =input()
	d1 = roll_dice()
	d2 = roll_dice()
	print_dice(d1,d2)
	jail(num)
	n3=(d1+d2)
	if n3+players[num-1][2] >=24:
		players[num-1][1]+=200
		print("Player "+str(num)+", you passed go and recieved $200. Your current balance is $"+str(players[num-1][1]))
	players[num-1][2]=(players[num-1][2]+n3)%24
	print("You are currently at "+str(names[players[num-1][2]])+".")
	move(players[num-1][2],num)
	
#This picks random numbers for the dice
def roll_dice():
	return random.choice([1,2,3,4,5,6])
#This uses the roll_dice function to store and then display the faces of the dice on the command prompt.
def print_dice(num1, num2):
	print("You rolled: "+str(num1)+ ", " +str(num2)+".")
	dice_pos = {"1":[" "," "," ","O"," "," ", " "],"2":["O"," "," "," "," "," ", "O"],"3":[" ","O"," ","O"," ","O", " "],"4":["O","O"," "," "," ","O", "O"],"5":["O","O"," ","O"," ","O", "O"],"6":["O","O","O"," ","O","O", "O"],}
	d1 = dice_pos[str(num1)]
	d2 = dice_pos[str(num2)]
	print("┌───────┐ ┌───────┐") 
	print("│ "+d1[0]+"   "+d1[1]+" │ │ "+d2[0]+"   "+d2[1]+" │")
	print("│ "+d1[2]+" "+d1[3]+" "+d1[4]+" │ │ "+d2[2]+" "+d2[3]+" "+d2[4]+" │")
	print("│ "+d1[5]+"   "+d1[6]+" │ │ "+d2[5]+"   "+d2[6]+" │")
	print("└───────┘ └───────┘")
#Used for monopoly board to space the property names out and make it all look correct on the game board.
def spacer(word):
	while len(word)<10:
		word = " "+word
		if len(word)<10:
			word =word +" "
	return word
#This takes in the players money and adds 0s in the beginning to display it correctly on the game board.
def print_money(num):
	if len(num)==4:
		return num
	if len(num)==3:
		return "0"+str(num)
	if len(num)==2:
		return "00"+str(num)
	if len(num)==1:
		return "000"+str(num)
	if len(num)==0:
		return "0000"
#This uses the two characters (▓ ░) and checks if a player is at a specific position and if they are, it displays the mark of the player at the position they are at. 
def print_pos(pos):
	if players[0][2]==pos and players[1][2]==pos:
		return "▓ ░"
	if players[1][2]==pos:
		return " ░ "
	if players[0][2]==pos:
		return " ▓ "
	else:
		return "   "
#Displays a X on the board if no one owns a property and a 1 or 2 if either player owns the property.
def print_own(pos):
	if owned[pos] == 1 or owned[pos]==2:
		return str(owned[pos])
	else:
		return "X"
#Prints the number of houses owned on a property. Takes in pos of property and returns 0H,1H,2H,3H, or 4H.
def print_house(pos):
	return str(houses[pos])+"H"
#Puts everything together and displays the board on the command prompt.
def print_board():
	print("╔══════════╦══════════╦══════════╦══════════╦══════════╦══════════╦══════════╗")
	print("║   Free   ║"+spacer(names[13])+"║"+spacer(names[14])+"║"+spacer(names[15])+"║"+spacer(names[16])+"║"+spacer(names[17])+"║          ║")
	print("║  Parking ║   $240   ║    $240  ║          ║   $280   ║   $300   ║   JAIL   ║")
	print("║   "+print_pos(12)+"    ║ "+print_own(13)+" "+print_pos(13)+" "+print_house(13)+" ║ "+print_own(14)+" "+print_pos(14)+" "+print_house(14)+" ║   "+print_pos(15)+"    ║ "+print_own(16)+" "+print_pos(16)+" "+print_house(16)+" ║ "+print_own(17)+" "+print_pos(17)+" "+print_house(17)+" ║   "+print_pos(18)+"    ║")
	print("╠══════════╬══════════╩══════════╩══════════╩══════════╩══════════╬══════════╣")
	print("║"+spacer(names[11])+"║  ┌────────────────┐              ┌────────────────┐  ║"+spacer(names[19])+"║")
	print("║   $200   ║  │ P1 Money:$"+str(print_money(str(int(p1[1]))))+" │              │ P2 Money:$"+str(print_money(str(int(p2[1]))))+" │  ║   $350   ║")
	print("║ "+print_own(11)+" "+print_pos(11)+" "+print_house(11)+" ║  └────────────────┘              └────────────────┘  ║ "+print_own(19)+" "+print_pos(19)+" "+print_house(19)+" ║")
	print("╠══════════╣                                                      ╠══════════╣")
	print("║"+spacer(names[10])+"║                                                      ║"+spacer(names[20])+"║")
	print("║   $190   ║                                                      ║   $360   ║")
	print("║ "+print_own(10)+" "+print_pos(10)+" "+print_house(10)+" ║                       WELCOME TO                     ║ "+print_own(20)+" "+print_pos(20)+" "+print_house(20)+" ║")
	print("╠══════════╣                                                      ╠══════════╣")
	print("║"+spacer(names[9])+"║           ░░ ░░ ░░░ ░  ░ ░░░ ░░░ ░░░ ░ ░   ░         ║"+spacer(names[21])+"║")
	print("║   "+print_pos(9)+"    ║           ░░░░░ ░ ░ ░░ ░ ░ ░ ░ ░ ░ ░ ░  ░ ░          ║   "+print_pos(21)+"    ║")
	print("╠══════════╣           ░ ░ ░ ░ ░ ░ ░░ ░ ░ ░░░ ░ ░ ░   ░           ╠══════════╣")
	print("║"+spacer(names[8])+"║           ░   ░ ░░░ ░  ░ ░░░ ░   ░░░ ░░░ ░           ║"+spacer(names[22])+"║")
	print("║   $160   ║           BY Fatih Ak and Arash Nassirinia           ║   $370   ║")
	print("║ "+print_own(8)+" "+print_pos(8)+" "+print_house(8)+" ║                                                      ║ "+print_own(22)+" "+print_pos(22)+" "+print_house(22)+" ║")
	print("╠══════════╣                                                      ╠══════════╣")
	print("║"+spacer(names[7])+"║                                                      ║"+spacer(names[23])+"║")
	print("║   $140   ║                                                      ║   $400   ║")
	print("║ "+print_own(7)+" "+print_pos(7)+" "+print_house(7)+" ║                                                      ║ "+print_own(23)+" "+print_pos(23)+" "+print_house(23)+" ║")
	print("╠══════════╬══════════╦══════════╦══════════╦══════════╦══════════╬══════════╣")
	print("║   Just   ║"+spacer(names[5])+"║"+spacer(names[4])+"║"+spacer(names[3])+"║"+spacer(names[2])+"║"+spacer(names[1])+"║    GO    ║")
	print("║  Visitng ║   $110   ║   $100   ║          ║   $60    ║   $60    ║ Get $200 ║")
	print("║   "+print_pos(6)+"    ║ "+print_own(5)+" "+print_pos(5)+" "+print_house(5)+" ║ "+print_own(4)+" "+print_pos(4)+" "+print_house(4)+" ║   "+print_pos(3)+"    ║ "+print_own(2)+" "+print_pos(2)+" "+print_house(2)+" ║ "+print_own(1)+" "+print_pos(1)+" "+print_house(1)+" ║   "+print_pos(0)+"    ║")
	print("╚══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╝")
print_board()
print("Welcome to MONOPOLY!")
print("Player 1 is ░. Player 2 is ▓")
#asks and prints instructions if player wants to see them.
print("Would you like to read the instructions? Type yes or no.")
i = input() 
if i == "yes" or i == "y" or i == "Yes" or i == "Y":
	print("Instructions:")
	print("This game is played with two players. Every player starts with $1500 at 'GO'")
	print("In every turn, players roll two dice and move that number of positions on the")
	print("board. If the property is unowned, the player can buy that property. If owned,")
	print("the player pays rent to the owner. Players can build up to four houses on")
	print("their properties, which increases the rent by 2 times. Players can also mortgage")
	print("properties at 1/2 of the original price and unmortgage them at half price.") 
	print("The game ends if one player has no more money and properties to mortgage when")
	print("they end their turn.If a player lands on JAIL, they become inactive for 3 turns")
	print("unless they choose to pay $50 or roll a double. Players who roll a double roll")
	print("of their turn again at the end.")
	print("╠══════════╣")
	print("║"+spacer(names[7])+"║")
	print("║   $140   ║")
	print("║ "+print_own(7)+" "+print_pos(7)+" "+print_house(7)+" ║")
	print("╠══════════╬")
	print("")
	print("The board shows the property names and prices along with each player's position")
	print("and it indicates which player owns each property with an X if it is unowned and")
	print("the Player number if it is owned. Each property also shows number of houses owned")
	print("on that property with 0H, 1H, 2H, 3H, or 4H for the number of houses.")
print("Player 1 starts first. Good luck!")
print()
#starts the game with player 1.
player(1)