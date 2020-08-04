# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 19:39:37 2018

@author: Admin
"""

import random
import cv2
import numpy as np
import math


def num():
    cap = cv2.VideoCapture(1)
    while (cap.isOpened()):
        # read image
        ret, img = cap.read()

        # get hand data from the rectangle sub window on the screen
        cv2.rectangle(img, (300, 300), (100, 100), (0, 255, 0), 0)
        crop_img = img[100:300, 100:300]

        # convert to grayscale
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # applying gaussian blur
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)

        # thresholdin: Otsu's Binarization method
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # show thresholded image
        cv2.imshow('Thresholded', thresh1)

        # check OpenCV version to avoid unpacking error
        (version, _, _) = cv2.__version__.split('.')

        if version == '3':
            image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                                                          cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif version == '2':
            contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                                                   cv2.CHAIN_APPROX_NONE)

        # find contour with max area
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        # create bounding rectangle around the contour (can skip below two lines)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt)

        # drawing contours
        drawing = np.zeros(crop_img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt, returnPoints=False)

        # finding convexity defects
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

        # applying Cosine Rule to find angle for all defects (between fingers)
        # with angle > 90 degrees and ignore defects
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            # apply cosine rule here
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

            # ignore angles > 90 and highlight rest with red dots
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            # dist = cv2.pointPolygonTest(cnt,far,True)

            # draw a line from start to end i.e. the convex points (finger tips)
            # (can skip this part)
            cv2.line(crop_img, start, end, [0, 255, 0], 2)
            # cv2.circle(crop_img,far,5,[0,0,255],-1)

        # define actions required
        if count_defects == 1:
            cv2.putText(img, "2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        elif count_defects == 2:
            str = "3"
            cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        elif count_defects == 3:
            cv2.putText(img, "4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(img, "5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        else:

            cv2.putText(img, "1", (50, 50), \
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        # show appropriate images in windows
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return count_defects + 1


user_score = 0
computer_score = 0
overs = 0
balls = 1
user_duck = True
computer_duck = True
user_out = False
computer_out = False
toss = ['1', '2']
bat_or_bowl = ["Bat", "Bowl"]
print("Toss time!")
choice = input("Head/Tails?\n1.Heads\n2.Tails\nEnter your choice: ")
if choice == '1' or choice == '2':
    who = random.choice(toss)
    # User won the toss!
    if who == choice:

        print("Hurray you won the toss!")
        option = input("What do you wish to do?\n1.Bat\n2.Bowl\nEnter the option: ")
        if option == '1' or option == '2':

            # User choses to bat
            if option == '1':
                print("You chose to bat!")
                print("Let's begin!")
                user_input = num()

                computer_input = random.randint(1, 5)
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                if user_input == computer_input:
                    computer_out = True

                elif user_input != computer_input:
                    user_score += user_input
                    print("Current score:", user_score)

                if user_input <= 0 or user_input > 5:

                    print("Invalid input!")
                    user_score = 0
                    balls = 0
                
                    print()
                    print("Your input is: ", user_input, " and computer input is: ", computer_input)
                    print()
                    print("Current score:", user_score)
                    print("Overs:", overs, ".", balls)
                    print()
                    print()
                while user_input != computer_input:
                    user_duck = False
                    user_input = num()
                    if user_input <= 0 or user_input > 5:
                        print("Invalid input!")
                        continue
                    computer_input = random.randint(1, 5)
                    if computer_input == user_input:
                        break
                    user_score += user_input
                    balls += 1
                    if balls % 6 == 0:
                        overs += 1
                    if balls == 6:
                        balls = 0

                    print()
                    print("Your input is", user_input, " and computer input is ", computer_input)
                    print()
                    print("Current score:", user_score)
                    print("Overs:", overs, ".", balls)
                    print()
                print("Out!!!")
                if user_duck:
                    user_score = 0
                if user_score == 0:
                    print("Duck!!!")
                else:
                    if overs <= 1:
                        print("You scored ", user_score, " from ", overs, " over and", balls, " balls.")
                    else:
                        print("You scored ", user_score, " from ", overs, " overs and", balls, " balls.")

                # User's turn to bowl
                balls = 1
                overs = 0
                print("Now your turn to bowl\n\nNever allow the opponent to cross your score\nAll the best!")
                user_input = num()
                computer_input = random.randint(1, 5)
                print("Your input is: ", user_input, " and computer input is: ", computer_input)

                if user_input != computer_input:
                    computer_score += computer_input
                    computer_duck = False
                else:
                    computer_score = 0
                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    computer_score = 0
                    balls = 0
                
                    print("Your input is: ", user_input, " and computer input is: ", computer_input)
                    print("Current score:", computer_score)
                    print("Overs:", overs, ".", balls)
                while computer_score < user_score:
                    user_input = num()
                    if user_input <= 0 or user_input > 5:
                        print("Invalid input!")
                        continue
                    computer_input = random.randint(1, 5)
                    if user_input == computer_input:
                        break
                    computer_score += computer_input
                    balls += 1
                    if balls % 6 == 0:
                        overs += 1
                    if balls == 6:
                        balls = 0
                    print()
                    print("Your input is", user_input, " and computer input is ", computer_input)
                    print("Current score:", computer_score)
                    print("Overs:", overs, ".", balls)
                    print()
                if computer_out:
                    print("Out!!!")
                if computer_duck:
                    computer_score = 0
                if overs <= 0:
                    print("Computer scored ", computer_score, " from ", overs, " over and", balls + 1, " balls")
                else:
                    print("Computer scored ", computer_score, " from ", overs, " overs and", balls + 1, " balls")
                if user_score > computer_score:
                    print("You won!")
                    print("Scores:\nYou:", user_score, "\nComputer:", computer_score)
                else:
                    print("Computer won!!!\nBetter luck next time")
                    print("Scores:\nComputer:", computer_score, "\nYou:", user_score)

            # User choses to bowl
            else:

                print("You chose to bowl!")
                user_input = num()
                computer_input = random.randint(1, 5)
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                
                
                if user_input != computer_input:
                    

                    computer_score += computer_input
                    computer_duck = False

                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    computer_score = 0
                    balls = 0
                
                    print()
                    print("Your input is: ", user_input, " and computer input is: ", computer_input)
                    print("Current score:", computer_score)
                    print("Overs:", overs, ".", balls)
                    print()
                while computer_input != user_input:
                    user_input = num()
                    if user_input <= 0 or user_input > 5:
                        print("Invalid input!")
                        continue
                    computer_input = random.randint(1, 5)
                    if computer_input == user_input:
                        break
                    computer_score += computer_input
                    balls += 1
                    if balls % 6 == 0:
                        overs += 1
                    if balls == 6:
                        balls = 0
                    print()
                    print("Your input is", user_input, " and computer input is ", computer_input)
                    print("Current score:", computer_score)
                    print("Overs:", overs, ".", balls)
                    print()
                print("Out!!!")
                if computer_duck:
                    computer_score = 0
                if computer_duck:
                    print("Duck!!!")
                else:
                    if overs <= 0:
                        print("Computer scored ", computer_score, " from ", overs, " over and", balls + 1, " balls")
                    else:
                        print("Computer scored ", computer_score, " from ", overs, " overs and", balls + 1, " balls")

                        # User's turn to bat
                overs = 0
                balls = 1
                print("Now it's your turn to bat\nTry to defeat the oppponent\nAll the best!")
                print("Let's begin!")
                user_input = num()
                computer_input = random.randint(1, 5)
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                if user_input != computer_input:
                    user_score += user_input
                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    user_score = 0
                    balls = 0
                
                    print()
                    print("Your input is: ", user_input, " and computer input is: ", computer_input)
                    print()
                    print("Current score:", user_score)
                    print("Overs:", overs, ".", balls)
                    print()
                    print()
                while user_score < computer_score:
                    user_duck = False
                    user_input = num()
                    if user_input <= 0 or user_input > 5:
                        print("Invalid input!")
                        continue
                    computer_input = random.randint(1, 5)
                    if user_input == computer_input:
                        user_out = True
                        break
                    user_score += user_input
                    balls += 1
                    if balls % 6 == 0:
                        overs += 1
                    if balls == 6:
                        balls = 0
                    print()
                    print("Your input is", user_input, " and computer input is ", computer_input)
                    print()
                    print("Current score:", user_score)
                    print("Overs:", overs, ".", balls)
                    print()
                if user_out:
                    print("Out!!!")
                if user_duck:
                    user_score = 0
                if overs <= 0:
                    print("You scored ", user_score, " from ", overs, " over and", balls + 1, " balls")
                else:
                    print("You scored ", user_score, " from ", overs, " overs and", balls + 1, " balls")
                if user_score > computer_score:
                    print("You won!")
                    print("Scores:\nYou:", user_score, "\nComputer:", computer_score)
                elif computer_score > user_score:
                    print("Computer won!!!\nBetter luck next time")
                    print("Scores:\nComputer:", computer_score, "\nYou:", user_score)
                else:
                    print("Tie!!!")
                    print("No one gives up!")
        else:
            print("Invalid option begin given!")

    # Computer won the toss!
    else:
        computer_option = random.choice(bat_or_bowl)
        print("Bad luck! computer won the toss and chose to ", computer_option)
        print("Let the battle begin!!!")

        # If computer choses batting
        if computer_option == "Bat":

            print("Computer bats!")
            user_input = num()
            computer_input = random.randint(1, 5)
            print("Your input is: ", user_input, " and computer input is: ", computer_input)
            computer_score += computer_input
            if computer_input != user_input:
                computer_duck = False

            if user_input <= 0 or user_input > 5:
                print("Invalid input!")
                computer_score = 0
                balls = 0
            
                print()
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                print("Current score:", computer_score)
                print("Overs:", overs, ".", balls)
                print()
            while computer_input != user_input:
                user_input = num()
                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    continue
                computer_input = random.randint(1, 5)
                if computer_input == user_input:
                    break
                computer_score += computer_input
                balls += 1
                if balls % 6 == 0:
                    overs += 1
                if balls == 6:
                    balls = 0
                print()
                print("Your input is", user_input, " and computer input is ", computer_input)
                print("Current score:", computer_score)
                print("Overs:", overs, ".", balls)
                print()
            print("Out!!!")
            if computer_duck:
                print("Duck!!!")
                computer_score = 0
            else:
                if overs <= 0:
                    print("Computer scored ", computer_score, " from ", overs, " over and", balls + 1, " balls")
                else:
                    print("Computer scored ", computer_score, " from ", overs, " overs and", balls + 1, " balls")

                    # Computer's turn to bowl

            overs = 0
            balls = 1
            print("Computer bowls!")
            user_input = num()
            computer_input = random.randint(1, 5)
            print("Your input is: ", user_input, " and computer input is: ", computer_input)
            if user_input != computer_input:
                user_score += user_input
            if user_input <= 0 or user_input > 5:
                print("Invalid input!")
                user_score = 0
                balls = 0
            
                print()
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                print()
                print("Current score:", user_score)
                print("Overs:", overs, ".", balls)
                print()
                print()
            while user_score <= computer_score:
                user_duck = False
                user_input = num()
                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    continue
                computer_input = random.randint(1, 5)
                if user_input == computer_input:
                    user_out = True
                    break
                user_score += user_input
                balls += 1
                if balls % 6 == 0:
                    overs += 1
                if balls == 6:
                    balls = 0
                print()
                print("Your input is", user_input, " and computer input is ", computer_input)
                print()
                print("Current score:", user_score)
                print("Overs:", overs, ".", balls)
                print()
            if user_out:
                print("Out!!!")
            if user_duck:
                user_score = 0
            if overs <= 0:
                print("You scored ", user_score, " from ", overs, " over and", balls + 1, " balls")
            else:
                print("You scored ", user_score, " from ", overs, " overs and", balls + 1, " balls")

                # Announcing the winner

            if user_score > computer_score:
                print("You won!")
                print("Scores:\nYou:", user_score, "\nComputer:", computer_score)
            elif computer_score > user_score:
                print("Computer won!!!\nBetter luck next time")
                print("Scores:\nComputer:", computer_score, "\nYou:", user_score)
            else:
                print("Tie!!!")
            





        # If computer choses to bowl
        else:

            print("Computer bowls!")
            user_input = num()
            computer_input = random.randint(1, 5)
            print("Your input is: ", user_input, " and computer input is: ", computer_input)
            if user_input != computer_input:
                user_score += user_input
            if user_input <= 0 or user_input > 5:
                print("Invalid input!")
                user_score = 0
                balls = 0
            
                print()
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                print()
                print("Current score:", user_score)
                print("Overs:", overs, ".", balls)
                print()
                print()
            while user_input != computer_input:
                user_duck = False
                user_input = num()
                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    continue
                computer_input = random.randint(1, 5)
                if user_input == computer_input:
                    user_out = True
                    break
                user_score += user_input
                balls += 1
                if balls % 6 == 0:
                    overs += 1
                if balls == 6:
                    balls = 0
                print()
                print("Your input is", user_input, " and computer input is ", computer_input)
                print()
                print("Current score:", user_score)
                print("Overs:", overs, ".", balls)
                print()
            if user_out:
                print("Out!!!")
            if user_duck:
                user_score = 0
            if overs <= 0:
                print("You scored ", user_score, " from ", overs, " over and", balls + 1, " balls")
            else:
                print("You scored ", user_score, " from ", overs, " overs and", balls + 1, " balls")

                # Computer's turn to bat

            overs = 0
            balls = 1
            print("Computer bats!")
            user_input = num()
            computer_input = random.randint(1, 5)
            print("Your input is: ", user_input, " and computer input is: ", computer_input)
            
            if computer_input != user_input:
                computer_score += computer_input
                computer_duck = False
            else:
                computer_score = 0
            if user_input <= 0 or user_input > 5:
                print("Invalid input!")
                computer_score = 0
                balls = 0
            
                print()
                print("Your input is: ", user_input, " and computer input is: ", computer_input)
                print("Current score:", computer_score)
                print("Overs:", overs, ".", balls)
                print()
            while computer_score <= user_score:
                computer_duck = False
                user_input = num()
                if user_input <= 0 or user_input > 5:
                    print("Invalid input!")
                    continue
                computer_input = random.randint(1, 5)
                if computer_input == user_input:
                    computer_out = True
                    break
                computer_score += computer_input
                balls += 1
                if balls % 6 == 0:
                    overs += 1
                if balls == 6:
                    balls = 0
                print()
                print("Your input is", user_input, " and computer input is ", computer_input)
                print("Current score:", computer_score)
                print("Overs:", overs, ".", balls)
                print()
            if computer_out:
                print("Out!!!")
            if computer_duck:
                print("Duck!!!")
                computer_score = 0
            else:
                if overs <= 0:
                    print("Computer scored ", computer_score, " from ", overs, " over and", balls + 1, " balls")
                else:
                    print("Computer scored ", computer_score, " from ", overs, " overs and", balls + 1, " balls")

                    # Announcing the winner

            if user_score > computer_score:
                print("You won!")
                print("Scores:\nYou:", user_score, "\nComputer:", computer_score)
            elif computer_score > user_score:
                print("Computer won!!!\nBetter luck next time")
                print("Scores:\nComputer:", computer_score, "\nYou:", user_score)
            else:
                print("Tie!!!")
                


else:
    print("Invalid option given!")


