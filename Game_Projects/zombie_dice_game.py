import random
import sys
import time
import copy

f = "footsteps"
b = "brains"
s = "shotgun"

GREEN_DICE = (f, f, b, b, b, s)
RED_DICE = (f, f, b, s, s, s)
YELLOW_DICE = (f, f, b, b, s, s)


def fillTheCup():  # Filling the cup with 13 shuffled dice
    cup = []

    for i in range(4):
        toGreenList = list(GREEN_DICE)
        random.shuffle(toGreenList)
        cup.append(toGreenList)

    for i in range(4):
        toRedList = list(RED_DICE)
        random.shuffle(toRedList)
        cup.append(toRedList)

    for i in range(4):
        toYellowList = list(YELLOW_DICE)
        random.shuffle(toYellowList)
        cup.append(toYellowList)

    if random.randint(0, 2) == 0:
        toGreenList = list(GREEN_DICE)
        random.shuffle(toGreenList)
        cup.append(toGreenList)

    elif random.randint(0, 2) == 1:
        toRedList = list(RED_DICE)
        random.shuffle(toRedList)
        cup.append(toRedList)

    else:
        toYellowList = list(YELLOW_DICE)
        random.shuffle(toYellowList)
        cup.append(toYellowList)

    random.shuffle(cup)

    return cup  # Returns a list of 13 shuffled dice


def drawDice(cup, count):  # Draw random dice from a cup
    diceDrawn = []

    if len(cup) < 3:
        count = len(cup)

    for i in range(count):
        diceDrawn.append(cup[i])

    return diceDrawn  # Returns a list of new dice


def whoGoesFirst():  # Decides who's turn is first
    if random.randint(0, 1) == 0:
        return "Computer"
    else:
        return "Player"


def orderDice(
    forRedrawList, redrawnDiceList, diceLeft
):  # Returns a list of new dice and dice with 'footsteps' from the previous draw
    result = [[], [], []]
    n = 0

    for i in range(len(forRedrawList)):
        if i % 2 != 0:
            if forRedrawList[i - 1] != []:
                random.shuffle(forRedrawList[i - 1])
                while forRedrawList[i - 1] in diceLeft:
                    random.shuffle(forRedrawList[i - 1])
                result.insert(forRedrawList[i], forRedrawList[i - 1])
                result.pop(forRedrawList[i] + 1)

            else:
                for k in range(n, len(redrawnDiceList)):
                    result.insert(forRedrawList[i], redrawnDiceList[k])
                    result.pop(forRedrawList[i] + 1)
                    n += 1
                    break

    return result  # Returns a list of 3 Dice


# The game starts
gameIsFinished = False

while not gameIsFinished:
    print("Welcome to the game!")
    turn = whoGoesFirst()
    playerPoints = 0
    computerPoints = 0

    while True:
        if gameIsFinished:
            if playerPoints >= 13 and computerPoints >= 13 and playerPoints == computerPoints:
                print(f"It's a tie! Player got {playerPoints} brains eaten against computer's {computerPoints}")
            elif playerPoints > computerPoints:
                print(f"Player wins with {playerPoints} brains eaten against computer's {computerPoints}")
            elif computerPoints > playerPoints:
                print(f"Computer wins with {computerPoints} brains eaten against your {playerPoints}")
            break

        if playerPoints >= 13:
            turn = "Computer"
            gameIsFinished = True
            print("That would be the last turn for the computer")
        elif computerPoints >= 13:
            turn = "Player"
            gameIsFinished = True
            print("That would be the last turn for the player")
        else:
            print(f"It's {turn}'s turn!")

        cup = fillTheCup()

        if turn == "Player":
            # Player's turn
            playerTurnPoints = 0
            print("Are you ready to draw 3 dice?")
            answer = input()
            if answer.lower().startswith("y") or len(answer) == 0:
                playerDice = drawDice(cup, 3)
                playerSides = []
                for i in range(len(playerDice)):
                    playerSides.append(playerDice[i][0])
                print(f"You got: {playerSides}")

                # We create a copy of given cup to modify it
                diceLeft = copy.copy(cup)

                while len(diceLeft) >= 0:
                    # While the cup is not empty

                    if (
                        len(playerSides) == 3
                        and playerSides[0] == "shotgun"
                        and playerSides[1] == "shotgun"
                        and playerSides[2] == "shotgun"
                    ):
                        turn = "Computer"
                        playerTurnPoints = 0
                        print("You got 3 shotguns, so no points were added to the total after the turn.")
                        input("Press Enter to continue")
                        print()
                        break

                    elif "brains" or "footsteps" in playerSides:
                        playerBrainsCount = 0
                        for i in playerSides:
                            if i == "brains":
                                playerBrainsCount += 1
                        playerTurnPoints += playerBrainsCount

                        playerStepsCount = 0
                        forPlayerRedraw = []
                        for i in range(len(playerSides)):
                            # We count how many footsteps we got after the draw and prepare list for orderDice func
                            if playerSides[i] == "footsteps":
                                playerStepsCount += 1
                                forPlayerRedraw += [playerDice[i], i]
                            else:
                                forPlayerRedraw += [[], i]

                        # After the draw, we remove the dice that got us 'brains' or 'shotguns' from the cup
                        for i in range(len(playerDice)):
                            try:
                                if playerDice[i] in diceLeft:
                                    diceLeft.remove(playerDice[i])
                                else:
                                    continue
                            except:
                                break

                        if len(diceLeft) < (3 - playerStepsCount):
                            # If it's not enough dice in the cup to redraw, we finish the turn
                            turn = "Computer"
                            playerPoints += playerTurnPoints
                            print("Now it's not enough dice in the cup to rerall!")
                            print(f"You've finished the turn with {playerPoints} points in total")
                            print()
                            time.sleep(2)
                            break

                        print(
                            f"After this draw you could add {playerTurnPoints} point(s) to your total score or keep rolling the dice."
                        )
                        print(f"There are {len(diceLeft)} dice left in the cup. Would you like to rerall your dice?")
                        playerRedraw = input()

                        if playerRedraw.lower().startswith("y") or len(playerRedraw) == 0:
                            # If player decides to rerall dice
                            print(
                                f"You got {playerStepsCount} footsteps, so you are taking {3 - playerStepsCount} dice from the cup to rerall. Press Enter if you are ready"
                            )
                            input()

                            # Now we create a list of 3 dice for redraw. We shuffle dice that gave us footsteps and add new dice if requred
                            newdrawnPlayerDice = drawDice(diceLeft, (3 - playerStepsCount))
                            redrawnPlayerDice = orderDice(forPlayerRedraw, newdrawnPlayerDice, diceLeft)
                            redrawnPlayerSides = []

                            for i in range(len(redrawnPlayerDice)):
                                try:
                                    redrawnPlayerSides.append(redrawnPlayerDice[i][0])
                                except:
                                    break

                            print(f"Rerall got you: {redrawnPlayerSides}")
                            playerSides = redrawnPlayerSides
                            playerDice = redrawnPlayerDice

                        else:
                            # If the player decides not to rerall dice
                            turn = "Computer"
                            playerPoints += playerTurnPoints
                            print(f"You've finished the turn with {playerPoints} points in total")
                            print()
                            break

            else:
                # Quit from the game
                print("Would you like to quit?")
                toQuit = input()
                if toQuit.lower().startswith("y"):
                    sys.exit()

        else:
            # Computer's turn
            computerRerallCount = 0
            computerTurnPoints = 0
            computerDice = drawDice(cup, 3)
            computerSides = []
            for i in range(len(computerDice)):
                computerSides.append(computerDice[i][0])

            # We create a copy of given cup to modify it
            diceLeft = copy.copy(cup)

            while len(diceLeft) >= 0:
                # While the cup is not empty

                if (
                    len(computerSides) == 3
                    and computerSides[0] == "shotgun"
                    and computerSides[1] == "shotgun"
                    and computerSides[2] == "shotgun"
                ):
                    turn = "Player"
                    computerTurnPoints = 0
                    print(f"Computer got 3 shotguns, so no points were added to the total after the turn.")
                    input("Press Enter to continue")
                    print()
                    break

                elif "brains" or "footsteps" in computerSides:
                    computerBrainsCount = 0
                    for i in computerSides:
                        if i == "brains":
                            computerBrainsCount += 1
                    computerTurnPoints += computerBrainsCount

                    computerStepsCount = 0
                    forComputerRedraw = []
                    for i in range(len(computerSides)):
                        # We count how many footsteps computer got after the draw and prepare list for orderDice func
                        if computerSides[i] == "footsteps":
                            computerStepsCount += 1
                            forComputerRedraw += [computerDice[i], i]
                        else:
                            forComputerRedraw += [[], i]

                    # After the draw, we remove the dice that got us 'brains' or 'shotguns' from the cup
                    for i in range(len(computerDice)):
                        try:
                            if computerDice[i] in diceLeft:
                                diceLeft.remove(computerDice[i])
                            else:
                                continue
                        except:
                            break

                    if len(diceLeft) < (3 - computerStepsCount):
                        # If it's not enough dice in the cup to redraw, computer finishes the turn
                        turn = "Player"
                        computerPoints += computerTurnPoints
                        print(f"After {computerRerallCount} reralls, computer is out of dice!")
                        print(f"Computer finished the turn with {computerPoints} points in total")
                        print()
                        time.sleep(2)
                        break

                    while True:
                        # Crazy computer will rerall the dice while there is still dice left in the cup
                        computerRerallCount += 1

                        # Now we create a list of 3 dice for redraw. We shuffle dice that gave us footsteps and add new dice if requred
                        newdrawnComputerDice = drawDice(diceLeft, (3 - computerStepsCount))
                        redrawnComputerDice = orderDice(forComputerRedraw, newdrawnComputerDice, diceLeft)
                        redrawnComputerSides = []

                        for i in range(len(redrawnComputerDice)):
                            try:
                                redrawnComputerSides.append(redrawnComputerDice[i][0])
                            except:
                                break

                        computerSides = redrawnComputerSides
                        computerDice = redrawnComputerDice
                        break

    print("Would you like to play again?")
    playAgain = input()
    if playAgain.lower().startswith("y"):
        gameIsFinished = False
        continue
    else:
        sys.exit()
