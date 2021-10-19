#Module
import random

#Data
dice = [0, 0, 0, 0, 0]

p1 = [-1, -1, -1, -1 ,-1 ,-1 ,-1 ,-1, -1, -1, -1, -1, -1]
p2 = [-1, -1, -1, -1 ,-1 ,-1 ,-1 ,-1, -1, -1, -1, -1, -1]
p3 = [-1, -1, -1, -1 ,-1 ,-1 ,-1 ,-1, -1, -1, -1, -1, -1]
p4 = [-1, -1, -1, -1 ,-1 ,-1 ,-1 ,-1, -1, -1, -1, -1, -1]

#Dice
def rollDice(a = 0):
    if a == 0:
        for i in range(5):
            dice[i] = random.randint(1, 6)
    else:
        dice[a-1] = random.randint(1, 6)
    return dice

#Gameplay

def selectScore(sel, dice, array):
    if sel == 1 and array[0] == -1:
        array[0] = dice.count(1)
        
    elif sel == 2 and array[1] == -1:
        array[1] = 2*dice.count(2)
        
    elif sel == 3 and array[2] == -1:
        array[2] = 3*dice.count(3)
        
    elif sel == 4 and array[3] == -1:
        array[3] = 4*dice.count(4)
        
    elif sel == 5 and array[4] == -1:
        array[4] = 5*dice.count(5)
        
    elif sel == 6 and array[5] == -1:
        array[5] = 6*dice.count(6)
        
    # 3카
    elif sel == 7 and array[6] == -1:
        array[6] = 0
        for item in [1,2,3,4,5,6]:
            if dice.count(item) >= 3:
                array[6] = sum(dice)
                break
            
    #4카
    elif sel == 8 and array[7] == -1:
        array[7] = 0
        for item in [1,2,3,4,5,6]:
            if dice.count(item) >= 4:
                array[7] = sum(dice)
                break
         
    #풀하우스(25)
    elif sel == 9 and array[8] == -1:
        val1 = dice.count(1)
        val2 = dice.count(2)
        val3 = dice.count(3)
        val4 = dice.count(4)
        val5 = dice.count(5)
        val6 = dice.count(6)
        if (val1 == 3 or val2 == 3 or val3 == 3 or val4 == 3 or val5 == 3 or val6 == 3) and (val1 == 2 or val2 == 2 or val3 == 2 or val4 == 2 or val5 == 2 or val6 == 2):
            array[8] = 25
        else:
            array[8] = 0
            
    #스스(30)
    elif sel == 10 and array[9] == -1:
        change_dice_result = list(set(dice))
        change_dice_result = sorted(change_dice_result)
        for i in range(1, 4):
            if (i in change_dice_result) and (i + 1 in change_dice_result) and (i + 2 in change_dice_result) and (i + 3 in change_dice_result):
                array[9] = 30
            elif array[9] != 30:
                array[9] = 0
                
    #라스(40)
    elif sel == 11 and array[10] == -1:
        change_dice_result = list(set(dice))
        change_dice_result = sorted(change_dice_result)
        for i in range(1, 3):
            if (i in change_dice_result) and (i + 1 in change_dice_result) and (i + 2 in change_dice_result) and (i + 3 in change_dice_result) and (i + 4 in change_dice_result):
                array[10] = 40
            elif array[10] != 40:
                array[10] = 0
    #찬스
    elif sel == 12 and array[11] == -1:
        array[11] = sum(dice)

    #야추(50)
    elif sel == 13 and array[12] == -1:
        change_dice_result = set(dice)
        if len(change_dice_result) == 1:
            array[12] = 50
        else:
            array[12] = 0

    return None

#Score
def dataArray(a):
    if a == 1:
        return p1
    elif a == 2:
        return p2
    elif a == 3:
        return p3
    elif a == 4:
        return p4

def scoreCalc(array, opt = 0):
    bonus = array[0] + array[1] + array[2] + array[3] + array[4] + array[5] + array[:6].count((-1))
    total = bonus + array[6] + array[7] + array[8] + array[9]+ array[10] + array[11] + array[12] + array[6:].count((-1))
    if opt == 0:
        if bonus < 63:
            return total
        else:
            return total + 60
    elif opt == 1:
        return bonus
#Reset
def resetDice():
    dice = [0, 0, 0, 0, 0]
    return None

def resetScore():
    for i in range(13):
        p1[i] = -1
    for i in range(13):
        p2[i] = -1
    for i in range(13):
        p3[i] = -1
    for i in range(13):
        p4[i] = -1
    return None
    
