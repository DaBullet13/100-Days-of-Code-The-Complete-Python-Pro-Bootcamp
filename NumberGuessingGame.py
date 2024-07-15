import random
import os

def SetValue():
    MaxValue = "BLANK"
    while MaxValue == "BLANK":
        try:
            MaxValue = int(input("Whats the max potential number that could be guessed? "))
            Goal = random.randrange(1,MaxValue)
        except:
            print("please only enter numbers and greater than 1")
            MaxValue = "BLANK"
    return Goal, MaxValue

def Guess(Goal:int,Lives:int,MaxValue:int):
    Guess = "BLANK"
    while Guess == "BLANK":
        try:
            Guess = int(input(f"Guess a number between 1 and {MaxValue}\n"))
        except:
            Guess = "BLANK"
            print("You must enter only numbers, try again")
    os.system("cls")
    if Guess > Goal:
        print(f"{Guess} is too high!")
        return Lives-1, False
    elif Guess < Goal:
        print(f"{Guess} is too low!")
        return Lives-1, False
    elif Guess == Goal:
        print(f"{Guess} is right!")
        return Lives, True

def SetDifficulty():
    Choice = 0
    DifficultyLives = {1:["Easy",15],2:["Moderate",10],3:["Hard",5],4:["Impossible",1]}
    while Choice ==0:
        try:
            Choice = int(input("1.Easy - 15 lives\n2.Moderate - 10 lives\n3.Hard - 5 lives\n4.Impossible - 1 life\nWhat difficulty would you like to play? "))
        except:
            print("Please enter only 1,2,3,4")
    if Choice > 4 or Choice < 1:
        print("You didn't select a valid options, your difficulty has been choosen at random.... good luck!")
        Choice = random.randrange(1,4)
        print(f"You have been given {DifficultyLives[Choice][0]}")
    return DifficultyLives[Choice][1]

def GameOver(Lives:int,Win):
    if Win == True and Lives > 0:
        return input("Well done! would you like to play again y/n? ").lower() == "y"
    elif Win != True and Lives > 0:
        print(f"{Lives} Lives remaining")
        return False
    else:
        return input("That was rough! would you like to play again y/n? ").lower() == "y"

def GuessingGame():
    Replay = input("Would you like to play a guessing game y/n? ").lower() == "y"
    while Replay == True:
        Goal, MaxValue = SetValue()
        Lives = SetDifficulty()
        Win = False    
        while Lives>0 and Win != True:
            Lives, Win = Guess(Goal,Lives,MaxValue)
            Replay = GameOver(Lives,Win)
        os.system("cls")

GuessingGame()

