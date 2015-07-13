#!/usr/bin/env python
import random
import time
import re

days = ['su', 'm', 'tu', 'w', 'th', 'f', 'sa']

def randomDate(start, end, prop):
    stime = time.mktime(time.strptime(start, "%m/%d/%Y"))
    etime = time.mktime(time.strptime(end, "%m/%d/%Y"))

    ptime = stime + prop * (etime - stime)
    return time.localtime(ptime)

def getDayIndex(day):
    for i in enumerate(days):
        try:
            if re.match(i[1], day):
                return int(i[0])
        except TypeError:
            pass

def printHint(date, hint):
    year = int(time.strftime("%Y", date))
    c = year // 100
    y = year % 100

    anchor = (5 * (c % 4) + days.index('tu')) % 7
    a = y // 12
    b = y % 12
    c = b // 4
    d = a + b + c
    doomsday = (d + anchor) % 7

    print("Anchor day is: ", days[anchor])
    if hint > 0:
        print("Doomsday is: ", days[doomsday])

def promptGuess(dd, hints = 0):
    ddStr = time.strftime('%m/%d/%Y', dd)
    expected = int(time.strftime("%w", dd))

    result = { 'result' : False, 'hints' : hints }

    guess = input("What day of the week is %s: " % ddStr).lower()
    match = re.match("(" + "|".join(days) + "|[0-6]|h)", guess)
    if match:
        if re.match('h', guess):
            printHint(dd, hints)
            result['hints'] = result['hints'] + 1
            return result

        guess = getDayIndex(guess)
        if expected != guess:
            print("Sorry. That is not correct")
            return result

        print("Correct!")
        if hints > 0:
            print("%d hints used" % hints)
        result['result'] = True
        return result
    else:
        print("Not a valid guess (or 'h' for hint)")
        return result

    return result

def playGame():
    dd = randomDate("1/1/1700", "12/31/2500", random.random())
    finished = False
    hints = 0
    answers = 0

    start = time.time()
    while(not finished):
        result = promptGuess(dd, hints)
        answers = answers + 1
        finished = result['result']
        hints = result['hints']
    end = time.time()
    print("You took %d seconds and %d %s to solve" %
            ((end - start), answers, "tries" if answers > 1 else "try"))

def main():
    while(True):
        playGame()
        a = input("\nPlay another game [Y/n]? ")
        if re.match("n", a):
            return False


if __name__ == "__main__":
    main()
