import os
import decimal

DrinkOptions = {
    "Espresso":{"Ingredients":{"Water":50,"Milk":0,"Coffee":18},"Cost":"1.5"},
    "Latte":{"Ingredients":{"Water":200,"Milk":150,"Coffee":24},"Cost":"2.5"},
    "Cappuccino":{"Ingredients":{"Water":250,"Milk":100,"Coffee":24},"Cost":"3"}
}

Resources = {
    "Water":1000,
    "Milk":500,
    "Coffee":100,
    "Money":{
            "$0.05":10,
            "$0.10":10,
            "$0.20":10,
            "$0.50":10,
            "$1.00":10,
            "$2.00":10,
            "Card":0,
            }}

Currency = {
    "$0.05":decimal.Decimal('0.05'),
    "$0.10":decimal.Decimal('0.10'),
    "$0.20":decimal.Decimal('0.20'),
    "$0.50":decimal.Decimal('0.50'),
    "$1.00":decimal.Decimal('1.00'),
    "$2.00":decimal.Decimal('2.00'),
    "Card":decimal.Decimal('1.00')
    }

def CreateOptionList():
    OptionList = list(DrinkOptions)
    OptionList.append("Report")
    OptionList.append("Turn Machine Off")
    return OptionList

def UserOptions(OptionList:list):
    def CreateAndProvideAvailableList():
        def CheckIsAvailableForOrder(index):
            Water = Resources["Water"] >= DrinkOptions[OptionList[index]]["Ingredients"]["Water"]
            Milk =  Resources["Milk"] >= DrinkOptions[OptionList[index]]["Ingredients"]["Milk"]
            Coffee = Resources["Coffee"] >= DrinkOptions[OptionList[index]]["Ingredients"]["Coffee"]
            return (Water == True and Milk == True and Coffee == True)

        AvailableOptions = []
        for index in range(0,len(OptionList)):
            try:
                if  CheckIsAvailableForOrder(index):
                    print(f"{index+1}. {OptionList[index]}")
                    AvailableOptions.append(index+1)
            except:
                print(f"{index+1}. {OptionList[index]}")
                AvailableOptions.append(index+1)

        return AvailableOptions
    
    print("\nPlease see machine controls below")
    return CreateAndProvideAvailableList()

def UserInput(OptionList:list,ValidOptions:list):
    OptionSelect = None
    while ValidOptions.count(OptionSelect) == 0:
        try:
            OptionSelect = int(input("\nPlease select an option from above using the number associated: "))
        except:
            print(f"{OptionSelect}, is not an option\nPlease input a valid option")
        if ValidOptions.count(OptionSelect) == 0:
            print(f"{OptionSelect}, is not an option\nPlease input a valid option")
    print()
    return OptionList[OptionSelect-1]

def PrintReport():
    Cash = 0
    Card = 0
    ClearScreen()
    print("Current stock and revenue:")
    for Resource in Resources:
        if Resource == "Money":
            for value in Resources[Resource]:
                if value != "Card":
                    Cash += Resources[Resource][value]*Currency[value]
                else:
                    Card += Resources[Resource][value]
        else:
            print(f"{Resource}:{Resources[Resource]}")
    print(f"Cash Payments:${Cash}\nCard Payments:${'{:.2f}'.format(Card)}\nTotal Payments:${(float(Cash)+Card)}")

def Change(PaymentRequired,PaymentProvided,DenominationsPaidIn:dict):    
    ChangeDue = decimal.Decimal(PaymentProvided) - decimal.Decimal(PaymentRequired)
    if ChangeDue < 0:
        print("WTF Error")
        
    ChangeValueProvided = 0
    ChangeProvided = {}
    StartingTill = Resources["Money"].copy()

    for Denomination in StartingTill:
        StartingTill[Denomination] = StartingTill[Denomination] + DenominationsPaidIn.get(Denomination,0)

    for Denomination in sorted(Currency.keys(),reverse=True)[1:]:
        while decimal.Decimal(ChangeDue) >= Currency[Denomination] and StartingTill[Denomination] > 0:
            ChangeDue -= Currency[Denomination]
            ChangeValueProvided += Currency[Denomination]
            ChangeProvided[Denomination] = ChangeProvided.get(Denomination,0) + 1
            StartingTill[Denomination] -=1

    if ChangeDue > 0:
        print("Not enough money to provide change")
        TransactionSuccessful= False
    else:
        for Denomination in StartingTill:
            Resources["Money"][Denomination] = StartingTill[Denomination]
        TransactionSuccessful = True

    return ChangeValueProvided, TransactionSuccessful

def ClearScreen():
    os.system("cls")

def CloseProgram():
    ClearScreen()
    exit()

def GetPayment(Cost:str):
    ClearScreen()
    IsCash = input("Will you be paying with Card?\n1. Yes\n2. No ") == "2"
    Paid = 0
    if IsCash:
        CashRecieved = {}
        while decimal.Decimal(Cost) > Paid:
            for Denominator in sorted(Currency.keys(),reverse=True)[1:]:
                if decimal.Decimal(Paid) < decimal.Decimal(Cost):
                    ClearScreen()
                    print(f"Your total payment remaining is {'{:.2f}'.format(decimal.Decimal(Cost)-Paid)}")
                    try:
                        Recieved = int(input(f"\nHow many {Denominator} are you paying with? "))
                    except:
                        Recieved = 0
                    CashRecieved[Denominator] = CashRecieved.get(Denominator,0) + Recieved
                    Paid += decimal.Decimal(CashRecieved[Denominator] * Currency[Denominator])
            if (decimal.Decimal(Cost) > Paid):
                ClearScreen()
                print(f"\nYou have paid {Paid}, though require {Cost}")
                Continue = input("Would you like to continue inserting coins?\n1. Yes\n2. No ") == "1"
                if Continue == False:
                    CashRecieved = {}
                    return decimal.Decimal("0"), CashRecieved, Cost
        return Paid, CashRecieved, Cost
    else:
        CashRecieved = {"Card":float(decimal.Decimal(Cost))}
        Paid = Cost
        return Paid, CashRecieved, Cost

def ProduceDrink(SuccessfulTransaction:bool,Input:str):
    
    if SuccessfulTransaction:
        print(Resources)
        for ingredient in DrinkOptions[Input]["Ingredients"]:
            Resources[ingredient] -= DrinkOptions[Input]["Ingredients"][ingredient]
        print(Resources)
        print("Thank you, come again")
    else:
        print("Applogies, please come again")

def PrintReciept(Paid,Cost,ChangeProvided,Input):
    ClearScreen()
    print(f'''
Order Complete, have a wonderful day!
Order:{Input}
Total:${'{:.2f}'.format(decimal.Decimal(Cost))}
Paid:${'{:.2f}'.format(decimal.Decimal(Paid))}
Change:${'{:.2f}'.format(decimal.Decimal(ChangeProvided))}
          ''')

def Main():
    OptionList = CreateOptionList()
    while True:
        Input = UserInput(OptionList,UserOptions(OptionList))
        if Input == "Report":
            PrintReport()
        elif Input == "Turn Machine Off":
            CloseProgram()    
        else:
            print(Input)
            Paid, CashRecieved, Cost = GetPayment(DrinkOptions[Input]["Cost"])
            if float(Paid)>= float(Cost):
                ChangeProvided, SuccessfulTransaction = Change(Cost,Paid,CashRecieved)
                ProduceDrink(SuccessfulTransaction, Input)
                PrintReciept(Paid,Cost,ChangeProvided,Input)
            else:
                print("Payment refunded")

Main()