from dict import *
from art import logo


def check_resources():
	"""Check resources if sufficient"""
	global coffeeChosen
	insufficient_ingredients = False
	while not insufficient_ingredients:
		coffee_ingredients = MENU[prompt]["ingredients"]
		for ingredient in coffee_ingredients:
			if resources[ingredient] > coffee_ingredients[ingredient]:
				continue
			else:
				coffeeChosen = False
				print(f"\nInsufficient \33[31m{ingredient}\33[0m. Please choose another drink.")
				return coffeeChosen
		if not insufficient_ingredients:
			coffeeChosen = True
			return coffeeChosen


def coin_processing():
	"""Process coins"""
	coffee_price = MENU[prompt]["cost"]
	print(f"\33[34m{prompt.capitalize()}\33[0m: \33[32m${coffee_price:.2f}\33[0m\nPlease insert coins.\n")
	
	cent10_inserted = int(input("10c coins: ")) * 0.1
	cent20_inserted = int(input("20c coins: ")) * 0.2
	cent50_inserted = int(input("50c coins: ")) * 0.5
	
	total_amount = cent10_inserted + cent20_inserted + cent50_inserted
	change_amount = total_amount - coffee_price
	
	return total_amount, coffee_price, change_amount


def deduct_ingredient():
	coffee_ingredients = MENU[prompt]["ingredients"]
	for ingredient in coffee_ingredients:
		resources[ingredient] = resources[ingredient] - coffee_ingredients[ingredient]


def restart():
	global off
	another_coffee = input("\nWould you like to purchase another coffee? \33[32mY\33[0m/\33[31mN\33[0m\n")
	if another_coffee == "n":
		print("\n\33[31mTurning coffee machine off...\33[0m")
		off = True
	elif another_coffee == "y":
		return


def menu():
	print("\33[1;4mMenu\33[0m")
	for drink in MENU:
		print(f"{drink.capitalize()}: ${MENU[drink]['cost']:.2f}")


logo()
print("\n\33[32mTurning coffee machine on...\33[0m\n")
menu()
profit = 0
off = False
while not off:
	coffeeChosen = False
	while not coffeeChosen:
		prompt = input("\nWhat would you like? ").lower()
		
		if prompt == "menu":
			menu()
		
		if prompt == "report":
			for key in resources:
				if key == "coffee":
					unit = "g"
				else:
					unit = "ml"
				print(f"{key.capitalize()}: {resources[key]}{unit}")
			print("---")
			print(f"\33[1mProfit:\33[0m \33[1;32m${profit:.2f}\33[0m")
		
		if prompt == "refill":
			resourcesIngredient = input("\nWhat do you want to refill? ").lower()
			refillAmount = int(
				input(f"How much \33[32m{resourcesIngredient}\33[0m do you want to refill? "))
			resources[resourcesIngredient] += refillAmount
		
		if prompt == "off":
			break
		
		for coffee in MENU:
			if prompt != coffee:
				coffeeChosen = False
			elif prompt == coffee:
				coffeeChosen = check_resources()
				break
	
	if prompt != "off":
		totalAmount, coffeePrice, changeAmount = coin_processing()
		if totalAmount >= coffeePrice:
			deduct_ingredient()
			profit += coffeePrice
			print(f"\nYour change is \33[32m${changeAmount:.2f}\33[0m.")
			print(f"Here is your \33[34m{prompt}\33[0m. Enjoy!")
			restart()
		else:
			print("\n\33[31mInsufficient amount. Refunding coins...\33[0m")
			restart()
	elif prompt == "off":
		off = True
		print("\n\33[31mTurning coffee machine off...\33[0m")
