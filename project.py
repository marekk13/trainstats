import os
import curses
from curses import wrapper
import time
from datetime import date
import json
from unidecode import unidecode
import sys
from datetime import date, timedelta
from trainstats import day_punct, mult_day_punct, day_occ, mult_day_occ


def main(stdscr):
    menu(stdscr)


def menu(stdscr):  # main menu
    stdscr.clear()
    curses.curs_set(0)  # turning the visibility of a cursor off
    y, x = window_check(stdscr)

    welcome = "Hello! Here you can check out the statistics regarding delays and occupancies of PKP Intercity trains."
    stdscr.addstr(0, int(x / 2 - len(welcome) / 2), welcome)
    while True:
        stdscr.addstr(3, int(x / 2 - len("Functionalities:") / 2), "Functionalities:")
        stdscr.addstr(5, int(x / 2 - 25 / 2), "1. List of train delays")
        stdscr.addstr(6, int(x / 2 - 25 / 2), "2. List of train occupancies")
        stdscr.addstr(7, int(x / 2 - 25 / 2), "3. Delay statistics")
        stdscr.addstr(8, int(x / 2 - 25 / 2), "4. Occupancy statistics")
        stdscr.addstr(
            y - 1,
            int(x / 2 - len("Print ESC to leave") / 2),
            "Print ESC to leave",
        )
        stdscr.refresh()
        k = stdscr.getkey()
        if choice := validate(k):
            menu1(stdscr, choice)  # go to the second menu
        elif k == "\x1b":  # exit if esc
            sys.exit()
        else:
            stdscr.clear()
            stdscr.addstr(
                0,
                int(x / 2 - len("Incorrect input! Type again") / 2),
                "Incorrect input! Type again.",
            )


def menu1(
    stdscr, choice
):  # the second menu is almost the same for every option, so I opted for conditionals instead of more functions
    y, x = window_check(stdscr)
    stdscr.clear()
    curses.curs_set(0)
    while True:
        stdscr.clear()
        if choice == 1:
            stdscr.addstr(
                0,
                int(x / 2 - len("List of train delays") / 2),
                "List of train delays",
                curses.A_STANDOUT,
            )
        elif choice == 2:
            stdscr.addstr(
                0,
                int(x / 2 - len("List of train occupancies") / 2),
                "List of train occupancies",
                curses.A_STANDOUT,
            )
        elif choice == 3:
            stdscr.addstr(
                0,
                int(x / 2 - len("Delay statistics") / 2),
                "Delay statistics",
                curses.A_STANDOUT,
            )
        elif choice == 4:
            stdscr.addstr(
                0,
                int(x / 2 - len("Occupancy statistics") / 2),
                "Occupancy statistics",
                curses.A_STANDOUT,
            )

        if choice == 1 or choice == 2:
            stdscr.addstr(
                2,
                int(x / 2 - 25 / 2),
                "1. Single-day list",
            )

            stdscr.addstr(
                3,
                int(x / 2 - 25 / 2),
                "2. Multi-day list",
            )

        else:
            stdscr.addstr(
                2,
                int(x / 2 - 25 / 2),
                "1. Single-day statistics",
            )

            stdscr.addstr(
                3,
                int(x / 2 - 25 / 2),
                "2. Multi-day statistics",
            )

        stdscr.addstr(
            y - 1,
            int(x / 2 - len("Print ESC to come back to the main menu") / 2),
            "Print ESC to come back to the main menu",
        )
        stdscr.refresh()
        k = stdscr.getkey()
        if k == "1":
            menu11(stdscr, choice)  # single-day menu
        elif k == "2":
            menu12(stdscr, choice)  # multi-day menu
        elif k == "\x1b":
            menu(stdscr)


def menu12(stdscr, choice):  # multi-day menu
    y, x = window_check(stdscr)
    curr_text = ""
    curses.curs_set(0)  # turning the visibility of a cursor off
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    if choice == 1 or choice == 2:
        infotext = "Insert the dates of a train you look for: "
    else:
        infotext = "Insert the date range of statistics: "
    clr1 = curses.color_pair(1)
    l = len("from ")
    while True:
        stdscr.clear()
        if choice == 1:
            stdscr.addstr(
                0,
                int(x / 2 - len("List of train delays") / 2),
                "List of train delays",
                curses.A_STANDOUT,
            )
        elif choice == 2:
            stdscr.addstr(
                0,
                int(x / 2 - len("List of train occupancies") / 2),
                "List of train occupancies",
                curses.A_STANDOUT,
            )
        elif choice == 3:
            stdscr.addstr(
                0,
                int(x / 2 - len("Delay statistics") / 2),
                "Delay statistics",
                curses.A_STANDOUT,
            )
        else:
            stdscr.addstr(
                0,
                int(x / 2 - len("Occupancy statistics") / 2),
                "Occupancy statistics",
                curses.A_STANDOUT,
            )

        stdscr.addstr(3, int(x / 2 - len(infotext) / 2), infotext)
        stdscr.addstr(4, int(x / 2 - (l + 24) / 2), "from ")  # 2*10 +" to " = 24
        stdscr.addstr(
            4,
            int(x / 2 - (l + 24) / 2) + l,
            "YYYY-MM-DD",  # first date
            curses.A_REVERSE,
        )
        stdscr.addstr(
            4,
            int(x / 2 - (l + 24) / 2) + l,
            curr_text.split(" ")[
                0
            ],  # overlapping the first yyyy-mm-dd with a current user input
            curses.A_REVERSE,
        )
        stdscr.addstr(
            4, int(x / 2 - (l + 24) / 2) + 15, " to "
        )  # adding "to" after the first date

        stdscr.addstr(
            4,
            int(x / 2 - (l + 24) / 2) + 19,
            "YYYY-MM-DD",  # second date
            curses.A_REVERSE,
        )

        try:
            stdscr.addstr(
                4,
                int(x / 2 - (l + 24) / 2) + 19,
                curr_text.split(" ")[
                    1
                ],  # overlapping the second yyyy-mm-dd with a current user input
                curses.A_REVERSE,
            )
        except IndexError:
            pass

        stdscr.addstr(
            y - 1,
            int(x / 2 - len("Print ESC to come back") / 2),
            "Print ESC to come back",
        )
        stdscr.refresh()
        flag = 0  # flag==0 - increasing size, flag==1 - decreasing
        if len(curr_text) != 21:
            key = stdscr.getkey()
            if key == "\x08":  # backspace
                if len(curr_text) > 0:
                    curr_text = curr_text[:-1]  # shortening a text
                    if curr_text.endswith("-") or curr_text.endswith(" "):
                        curr_text = curr_text[
                            :-1
                        ]  # if "-" or " " is found in current text delete this char,
                        # so the user doesnt have to handle it
                    flag = 1  # decreasing size flag
            if not flag and (
                len(curr_text) == 4
                or len(curr_text) == 7
                or len(curr_text) == 15
                or len(curr_text) == 18
            ):  # "-" is a day, month,year separator
                curr_text += "-"
            if not flag and len(curr_text) == 10:
                curr_text += " "  # add a space separating two dates
            if key == "\x1b":  # escape
                menu1(stdscr, choice)  # come back to the previous menu
            elif not key.isnumeric():
                continue  # skipping non-numeric chars
            else:
                curr_text += key  # after handling other cases, we can add a char
                flag = 0
        else:  # when len(curr_text) == 21 whole time period is inputted and it can be splitted and validated
            first = curr_text.split(" ")[0]
            last = curr_text.split(" ")[1]
            if validate_date(first) and validate_date(last):
                days = []  # creating a list of days which user is interested in
                start_date = date(
                    int(first.split("-")[0]),
                    int(first.split("-")[1]),
                    int(first.split("-")[2]),
                )
                end_date = date(
                    int(last.split("-")[0]),
                    int(last.split("-")[1]),
                    int(last.split("-")[2]),
                )
                if start_date > end_date:  # handling incorrect input
                    errmsg = "First date is later than the second one"
                    stdscr.addstr(
                        6,
                        int(x / 2 - len(errmsg) / 2),
                        errmsg,
                        clr1,
                    )
                    stdscr.refresh()
                    time.sleep(2)
                    curr_text = ""
                    continue
                delta = timedelta(days=1)
                while start_date <= end_date:
                    days.append(start_date.strftime("%Y-%m-%d"))
                    start_date += delta  # appending every wanted day to the list
                flag = 0
                for day in days:
                    path = (  # looking for files
                        "/Users/Marek/.vscode/trainstats/json/trains_" + day + ".json"
                    )
                    if not os.path.isfile(
                        path
                    ):  # if one day of date range has no json file in a folder, user has to input again
                        errmsg = "No data for some of the days in a data range, try another one"
                        stdscr.addstr(
                            6,
                            int(x / 2 - len(errmsg) / 2),
                            errmsg,
                            clr1,
                        )
                        flag = 1
                        stdscr.refresh()
                        time.sleep(2)
                        curr_text = ""  # clearing the input
                        break
                if flag:  # if one of the files was not found, start again
                    continue
                if len(days) == 1:
                    days = days[0]
                stdscr.clear()
                if choice == 1:  # navigating to the third menu
                    menu111(stdscr, days, choice)
                if choice == 2:
                    menu112(stdscr, days, choice)
                if choice == 3:
                    menu113(stdscr, days, choice)
                if choice == 4:
                    menu114(stdscr, days, choice)
            else:  # erasing the input and printing an error message if the date is invalid
                stdscr.addstr(
                    6,
                    int(
                        x / 2
                        - len("One of the dates is invalid, or a future one, try again")
                        / 2
                    ),
                    "One of the dates is invalid, or a future one, try again",
                    clr1,
                )
                curr_text = ""
                stdscr.refresh()
                time.sleep(2)
                continue


def menu11(
    stdscr, choice
):  # similar to the previous function, but handling only one day
    y, x = window_check(stdscr)
    curr_text = ""
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    clr1 = curses.color_pair(1)
    if choice == 1 or choice == 2:
        infotext = "Insert the date of a train you look for: "
    else:
        infotext = "Insert the date of statistics: "
    while True:
        stdscr.clear()
        if choice == 1:
            stdscr.addstr(
                0,
                int(x / 2 - len("List of train delays") / 2),
                "List of train delays",
                curses.A_STANDOUT,
            )
        elif choice == 2:
            stdscr.addstr(
                0,
                int(x / 2 - len("List of train occupancies") / 2),
                "List of train occupancies",
                curses.A_STANDOUT,
            )
        elif choice == 3:
            stdscr.addstr(
                0,
                int(x / 2 - len("Delay statistics") / 2),
                "Delay statistics",
                curses.A_STANDOUT,
            )
        else:
            stdscr.addstr(
                0,
                int(x / 2 - len("Occupancy statistics") / 2),
                "Occupancy statistics",
                curses.A_STANDOUT,
            )
        stdscr.addstr(3, int(x / 2 - (len(infotext) + 10) / 2), infotext)
        stdscr.addstr(
            3,
            int(x / 2 - (len(infotext) + 10) / 2) + len(infotext),
            "YYYY-MM-DD",
            curses.A_REVERSE,
        )
        stdscr.addstr(
            3,
            int(x / 2 - (len(infotext) + 10) / 2) + len(infotext),
            curr_text,
            curses.A_REVERSE,
        )
        stdscr.addstr(
            y - 1,
            int(x / 2 - len("Print ESC to come back") / 2),
            "Print ESC to come back",
        )
        stdscr.refresh()
        flag = 0
        if len(curr_text) != 10:
            key = stdscr.getkey()
            if key == "\x08":
                if len(curr_text) > 0:
                    curr_text = curr_text[:-1]
                    if curr_text.endswith("-"):
                        curr_text = curr_text[:-1]
                    flag = 1
            if not flag and (len(curr_text) == 4 or len(curr_text) == 7):
                curr_text += "-"
            if key == "\x1b":  # escape
                menu1(stdscr, choice)
            elif not key.isnumeric():
                continue
            else:
                curr_text += key
                flag = 0
        else:
            if validate_date(curr_text):
                path = (
                    "/Users/Marek/.vscode/trainstats/json/trains_" + curr_text + ".json"
                )
                if not os.path.isfile(path):
                    stdscr.addstr(
                        5,
                        int(x / 2 - len("No data for this day, try another one") / 2),
                        "No data for this day, try another one",
                        clr1,
                    )
                    stdscr.refresh()
                    time.sleep(2)
                    curr_text = ""
                    continue
                stdscr.clear()
                if choice == 1:
                    menu111(stdscr, curr_text, choice)
                if choice == 2:
                    menu112(stdscr, curr_text, choice)
                if choice == 3:
                    menu113(stdscr, curr_text, choice)
                if choice == 4:
                    menu114(stdscr, curr_text, choice)
            else:
                stdscr.addstr(
                    5,
                    int(x / 2 - len("Invalid date, or a future one, try again") / 2),
                    "Invalid date, or a future one, try again",
                    clr1,
                )
                curr_text = ""
                stdscr.refresh()
                time.sleep(2)
                continue


def menu111(stdscr, date, choice):  # list of train delays menu
    # with filters and sorting included

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    clr1 = curses.color_pair(1)

    y, x = window_check(stdscr)
    maxlines = y - 1 - 4  # 4 lines on top, 1 at the bottom
    curses.curs_set(0)

    stdscr.addstr(
        0,
        int(x / 2 - len("List of train delays") / 2),
        "List of train delays",
        curses.A_STANDOUT,
    )
    stdscr.refresh()

    bottom = curses.newwin(1, x, y - 1, 0)  # nlines, ncols, begin y, begin x
    bottom.addstr("Press ESC to come back, i to scroll up, k to scroll down")
    bottom.refresh()

    top = curses.newwin(
        2, x, 1, 0
    )  # initializing more windows to exclude some text from scrolling
    filtwin = curses.newwin(1, x, 3, 0)

    mainpad = curses.newpad(maxlines, 100)
    mainpad.scrollok(True)  # allowing printing beyong a pad

    if "list" in str(type(date)):
        f1 = (
            []
        )  # if list was passed as argument, it means that data has to be gathered from multiple files
        for day in date:
            with open(f"json/trains_{day}.json", "r") as file:
                temp = json.load(file)
            for train in temp:
                f1.append(train)  # appending json files based on a given date period
    else:  # string - one day
        with open(f"json/trains_{date}.json", "r") as file:
            f1 = json.load(file)

    f1 = [train for train in f1 if not train["delay"] == "n/a"]
    f1og = sorted(f1, key=lambda k: int(k["delay"].split(" ")[0]), reverse=True)
    flag = 1  # main flag - filter, sort by..., quit
    r = 1  # reversed order flag
    filt = -1  # filter flag
    filtcount = 0  # filter count - max 3

    while True:
        filttext = "Applied filters: "
        if not flag:
            if "list" in str(type(date)):
                menu12(stdscr, choice)
            else:
                menu11(stdscr, choice)
        elif flag == 1 and r == 1:
            f1 = sorted(f1, key=lambda k: int(k["delay"].split(" ")[0]), reverse=True)
        elif flag == 1 and r == -1:
            f1 = sorted(f1, key=lambda k: int(k["delay"].split(" ")[0]), reverse=False)
        elif flag == 2 and r == 1:
            f1 = sorted(f1, key=lambda k: int(k["number"]), reverse=True)
        elif flag == 2 and r == -1:
            f1 = sorted(f1, key=lambda k: int(k["number"]), reverse=False)
        elif flag == 3 and r == 1:
            f1 = sorted(f1, key=lambda k: unidecode(k["from"]), reverse=False)
        elif flag == 3 and r == -1:
            f1 = sorted(f1, key=lambda k: unidecode(k["from"]), reverse=True)
        elif flag == 4 and r == 1:
            f1 = sorted(f1, key=lambda k: unidecode(k["to"]), reverse=False)
        elif flag == 4 and r == -1:
            f1 = sorted(f1, key=lambda k: unidecode(k["to"]), reverse=True)
        elif flag == 5 and r == 1:
            f1 = sorted(f1, key=lambda k: unidecode(k["name"]), reverse=False)
        elif flag == 5 and r == -1:
            f1 = sorted(f1, key=lambda k: unidecode(k["name"]), reverse=True)

        if filt == 1:  # filters
            # clear top pad
            r = 1
            while True:
                text = ""
                top.clear()
                text1 = "Filter by: 1. Minimal delay, 2. Maximal delay, 3. Train number"
                text2 = "4. Departure station, 5. Arrival station, 6. Train name, d - delete all filters"
                top.addstr(0, int(x / 2 - len(text1) / 2), text1)
                top.addstr(1, int(x / 2 - len(text2) / 2), text2)
                top.refresh()
                if filtcount:
                    filtwin.addstr(
                        0, int(x / 2 - len(filttext) / 2), filttext.rstrip(", "), clr1
                    )
                    filtwin.refresh()
                f = top.getch()
                if f == 49:  # 1. min delay
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert minimal delay: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":  # enter - end of filter input
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        try:
                            f1 = (
                                [  # updating data depending on a filter before printing
                                    train
                                    for train in f1
                                    if int(train["delay"].split(" ")[0])
                                    >= int(text.split(" ")[0])
                                ]
                            )
                            flag, r, filt = printdel(  # printing delay data
                                mainpad, f1, maxlines, r, x, y, flag, filt
                            )
                            filttext += f"delay >= {text.split(' ')[0]} min, "
                            filtcount += 1
                        except ValueError:
                            text = ""

                elif f == 50:  # 2. max delay
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert maximal delay: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        try:
                            f1 = [
                                train
                                for train in f1
                                if int(train["delay"].split(" ")[0])
                                <= int(text.split(" ")[0])
                            ]
                            flag, r, filt = printdel(
                                mainpad, f1, maxlines, r, x, y, flag, filt
                            )
                            filttext += f"delay <= {text.split(' ')[0]} min, "
                            filtcount += 1
                        except ValueError:
                            text = ""

                elif f == 51:  # 3. train number
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first digits of a train number: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        elif t.isnumeric():
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [train for train in f1 if train["number"].startswith(text)]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"train number: {text}, "
                        filtcount += 1

                elif f == 52:  # 4. departure station
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first letters of a departure station name: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [
                            train
                            for train in f1
                            if train["from"].startswith(text.capitalize())
                        ]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"departure station: {text}, "
                        filtcount += 1
                elif f == 53:  # 5. arrival station
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first letters of a arrival station name: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [
                            train
                            for train in f1
                            if train["to"].startswith(text.capitalize())
                        ]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"arrival station: {text}, "
                        filtcount += 1
                elif f == 54:  # 6. train name
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first letters of a train name: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [
                            train
                            for train in f1
                            if train["name"].startswith(text.upper())
                        ]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"train name: {text}, "
                        filtcount += 1
                elif f == 27:  # quit filters
                    filt = -filt
                    break
                elif f == 100:  # d-delete filters
                    f1 = f1og
                    filtwin.clear()
                    filtwin.refresh()
                    filtcount = 0
                    filttext = "Applied filters: "
                    flag, r, filt = printdel(mainpad, f1, maxlines, r, x, y, flag, filt)

        if filt == -1:
            top.clear()
            text1 = "Press: f - filters, r - reversed order, d - sort by delay, x - sort by train number"
            text2 = "s - sort by departure station, a - sort by arrival station, n - sort by train name"
            top.addstr(0, int(x / 2 - len(text1) / 2), text1)
            top.addstr(1, int(x / 2 - len(text2) / 2), text2)
            top.refresh()

        flag, r, filt = printdel(mainpad, f1, maxlines, r, x, y, flag, filt)


def printdel(mainpad, f1, maxlines, r, x, y, flag, filt):  # printing delay list
    # first, initial printing from a first train to the limit in lines
    mainpad.clear()
    nr = 0  # index of a last element shown on the screen
    while nr < maxlines - 1:
        try:
            if r == 1:
                mainpad.addstr(
                    f"{nr+1}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: {f1[nr]['delay']}\n",
                )
            if r == -1:
                mainpad.addstr(
                    f"{len(f1)-nr}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: {f1[nr]['delay']}\n",
                )
            nr += 1
        except IndexError:
            break
    mainpad.refresh(0, 0, 4, int(x / 2 - 78 / 2), y - 2, int(x / 2 + 96 / 2))
    if filt == 1:  # not allowing scrolling before leaving filter menu
        return (flag, r, filt)
    # obtional scrolling
    while True:
        c = mainpad.getkey()
        # downwards
        if c == "k":
            try:
                if r == 1:
                    mainpad.addstr(
                        f"{nr+1}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: {f1[nr]['delay']}\n",
                    )
                if r == -1:
                    mainpad.addstr(
                        f"{len(f1)-nr}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: {f1[nr]['delay']}\n",
                    )
                nr += 1
                mainpad.refresh(
                    0, 0, 4, int(x / 2 - 78 / 2), y - 2, int(x / 2 + 96 / 2)
                )
            except IndexError:
                pass
        # upwards
        elif c == "i":
            if nr - maxlines >= 0:
                mainpad.clear()
                if r == 1:
                    for i in range(nr - maxlines, nr):
                        mainpad.addstr(
                            f"{i}. {f1[i-1]['category']} {f1[i-1]['number']} {f1[i-1]['name']} {f1[i-1]['date']} {f1[i-1]['from']} - {f1[i-1]['to']}: {f1[i-1]['delay']}\n",
                        )
                if r == -1:
                    for i in range(nr - maxlines, nr):
                        mainpad.addstr(
                            f"{len(f1)-i+1}. {f1[i-1]['category']} {f1[i-1]['number']} {f1[i-1]['name']} {f1[i-1]['date']} {f1[i-1]['from']} - {f1[i-1]['to']}: {f1[i-1]['delay']}\n",
                        )
                nr -= 1
                mainpad.refresh(
                    0, 0, 4, int(x / 2 - 78 / 2), y - 2, int(x / 2 + 96 / 2)
                )
        elif c == "\x1b":  # esc - quit
            flag = 0
            break
        elif c == "r":  # r-reverse order
            r = -r
            break
        elif c == "d":  # d-sort by delay
            flag = 1
            break
        elif c == "x":  # x-sort by train number
            flag = 2
            break
        elif c == "s":  # s-sort by departure station
            flag = 3
            break
        elif c == "a":  # a-sort by arrival station
            flag = 4
            break
        elif c == "n":  # n-sort by train name
            flag = 5
            break
        elif c == "f":  # f-filters
            filt = -filt
            break
    return (flag, r, filt)


def menu112(stdscr, days, choice):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    clr1 = curses.color_pair(1)

    y, x = window_check(stdscr)
    maxlines = y - 1 - 4  # 4 lines on top, 1 at the bottom
    curses.curs_set(0)

    stdscr.addstr(
        0,
        int(x / 2 - len("List of train occupancies") / 2),
        "List of train occupancies",
        curses.A_STANDOUT,
    )
    stdscr.refresh()

    bottom = curses.newwin(1, x, y - 1, 0)  # nlines, ncols, begin y, begin x
    bottom.addstr("Press ESC to come back, i to scroll up, k to scroll down")
    bottom.refresh()

    top = curses.newwin(2, x, 1, 0)
    filtwin = curses.newwin(1, x, 3, 0)

    mainpad = curses.newpad(maxlines, 110)
    mainpad.scrollok(True)

    if "list" in str(type(days)):
        f1 = []
        for day in days:
            with open(f"json/trains_{day}.json", "r") as file:
                temp = json.load(file)
            for train in temp:
                f1.append(train)
    else:
        with open(f"json/trains_{days}.json", "r") as file:
            f1 = json.load(file)

    for train in f1:
        if "poniżej" in train["occupancy"]:  # poniżej means "below"
            train["occupancy"] = "below 50%"
        elif "50%-80%" in train["occupancy"]:
            train["occupancy"] = "between 50% and 80%"
        else:
            train["occupancy"] = "over 80%"
    f1og = sorted(f1, key=lambda k: k["occupancy"], reverse=True)
    flag = 1  # main flag - filter, sort by..., quit
    r = 1  # reversed order flag
    filt = -1  # filter flag
    filtcount = 0  # filter count

    while True:
        filttext = "Applied filters: "
        if not flag:
            if "list" in str(type(days)):
                menu12(stdscr, choice)
            else:
                menu11(stdscr, choice)
        elif flag == 1 and r == 1:
            f1 = sorted(f1, key=lambda k: k["occupancy"], reverse=True)
        elif flag == 1 and r == -1:
            f1 = sorted(f1, key=lambda k: k["occupancy"], reverse=False)
        elif flag == 2 and r == 1:
            f1 = sorted(f1, key=lambda k: int(k["number"]), reverse=True)
        elif flag == 2 and r == -1:
            f1 = sorted(f1, key=lambda k: int(k["number"]), reverse=False)
        elif flag == 3 and r == 1:
            f1 = sorted(f1, key=lambda k: unidecode(k["from"]), reverse=False)
        elif flag == 3 and r == -1:
            f1 = sorted(f1, key=lambda k: unidecode(k["from"]), reverse=True)
        elif flag == 4 and r == 1:
            f1 = sorted(f1, key=lambda k: unidecode(k["to"]), reverse=False)
        elif flag == 4 and r == -1:
            f1 = sorted(f1, key=lambda k: unidecode(k["to"]), reverse=True)
        elif flag == 5 and r == 1:
            f1 = sorted(f1, key=lambda k: unidecode(k["name"]), reverse=False)
        elif flag == 5 and r == -1:
            f1 = sorted(f1, key=lambda k: unidecode(k["name"]), reverse=True)

        if filt == 1:  # filters
            # clear top pad
            r = 1
            while True:
                text = ""
                top.clear()
                text1 = "Filter by: 1. Train number, 2. Departure station"
                text2 = "3. Arrival station, 4. Train name, d - delete all filters"
                top.addstr(0, int(x / 2 - len(text1) / 2), text1)
                top.addstr(1, int(x / 2 - len(text2) / 2), text2)
                top.refresh()
                if filtcount:
                    filtwin.addstr(
                        0, int(x / 2 - len(filttext) / 2), filttext.rstrip(", "), clr1
                    )
                    filtwin.refresh()
                f = top.getch()
                if f == 49:  # 1. train number
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first digits of a train number: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        elif t.isnumeric():
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [train for train in f1 if train["number"].startswith(text)]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"train number: {text}, "
                        filtcount += 1

                elif f == 50:  # 2. departure station
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first letters of a departure station name: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [
                            train
                            for train in f1
                            if train["from"].startswith(text.capitalize())
                        ]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"departure station: {text}, "
                        filtcount += 1
                elif f == 51:  # 3. arrival station
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first letters of a arrival station name: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [
                            train
                            for train in f1
                            if train["to"].startswith(text.capitalize())
                        ]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"arrival station: {text}, "
                        filtcount += 1
                elif f == 52:  # 4. train name
                    top.clear()
                    while True:
                        top.clear()
                        fstr = "Insert first letters of a train name: "
                        top.addstr(1, int(x / 2 - 70 / 2), fstr)
                        top.addstr(1, int(x / 2 - 70 / 2) + len(fstr), text)
                        top.refresh()
                        t = top.getkey()
                        if t == "\n":
                            break
                        elif t == "\x08" and len(text) > 0:  # backspace
                            text = text[:-1]
                        elif t == "\x1b":
                            text = ""
                            break
                        else:
                            text += t
                            top.addstr(text)
                    if text and filtcount < 3:
                        f1 = [
                            train
                            for train in f1
                            if train["name"].startswith(text.upper())
                        ]
                        flag, r, filt = printdel(
                            mainpad, f1, maxlines, r, x, y, flag, filt
                        )
                        filttext += f"train name: {text}, "
                        filtcount += 1
                elif f == 27:  # quit filters
                    filt = -filt
                    break
                elif f == 100:  # d-delete filters
                    f1 = f1og
                    filtwin.clear()
                    filtwin.refresh()
                    filtcount = 0
                    filttext = "Applied filters: "
                    flag, r, filt = printdel(mainpad, f1, maxlines, r, x, y, flag, filt)

        if filt == -1:
            top.clear()
            text1 = "Press: f - filters, r - reversed order, o - sort by occupancy, x - sort by train number"
            text2 = "d - sort by departure station, a - sort by arrival station, n - sort by train name"
            top.addstr(0, int(x / 2 - len(text1) / 2), text1)
            top.addstr(1, int(x / 2 - len(text2) / 2), text2)
            top.refresh()

        flag, r, filt = printocc(mainpad, f1, maxlines, r, x, y, flag, filt)


def menu113(stdscr, date, choice):
    y, x = window_check(stdscr)
    curses.curs_set(0)

    bottom = curses.newwin(1, x, y - 1, 0)  # nlines, ncols, begin y, begin x
    bottom.addstr("Press ESC to come back, i to scroll up, k to scroll down")
    bottom.refresh()

    if "list" in str(type(date)):
        punctdata = mult_day_punct(date)
    else:
        punctdata = day_punct(date)

    stdscr.addstr(
        0,
        int(x / 2 - len("Delay statistics") / 2),
        "Delay statistics",
        curses.A_STANDOUT,
    )

    if "list" in str(type(date)):
        text1 = f"{punctdata[1]['nodelay']} of trains arrived on time between {date[0]} and {date[-1]}"
    else:
        text1 = f"{punctdata[1]['nodelay']} of trains arrived on time on {date}"

    stdscr.addstr(
        2,
        int(x / 2 - len(text1) / 2),
        text1,
    )

    if "list" in str(type(date)):
        text2 = f"{punctdata[1]['m10']} of trains arrived with delay from 1 to 9 minutes between {date[0]} and {date[-1]}"
    else:
        text2 = f"{punctdata[1]['m10']} of trains arrived with delay from 1 to 9 minutes on {date}"
    stdscr.addstr(
        3,
        int(x / 2 - len(text2) / 2),
        text2,
    )

    if "list" in str(type(date)):
        text3 = f"{punctdata[1]['m30']} of trains arrived with delay from 10 to 29 minutes between {date[0]} and {date[-1]}"
    else:
        text3 = f"{punctdata[1]['m30']} of trains arrived with delay from 10 to 29 minutes on {date}"
    stdscr.addstr(
        4,
        int(x / 2 - len(text3) / 2),
        text3,
    )

    if "list" in str(type(date)):
        text4 = f"{punctdata[1]['m60']} of trains arrived with delay from 30 to 59 minutes between {date[0]} and {date[-1]}"
    else:
        text4 = f"{punctdata[1]['m60']} of trains arrived with delay from 30 to 59 minutes on {date}"
    stdscr.addstr(
        5,
        int(x / 2 - len(text4) / 2),
        text4,
    )

    if "list" in str(type(date)):
        text5 = f"{punctdata[1]['m180']} of trains arrived with delay from 60 to 179 minutes between {date[0]} and {date[-1]}"
    else:
        text5 = f"{punctdata[1]['m180']} of trains arrived with delay from 60 to 179 minutes on {date}"
    stdscr.addstr(
        6,
        int(x / 2 - len(text5) / 2),
        text5,
    )

    if "list" in str(type(date)):
        text6 = f"{punctdata[1]['m180p']} of trains arrived with delay exceeding 179 minutes between {date[0]} and {date[-1]}"
    else:
        text6 = f"{punctdata[1]['m180p']} of trains arrived with delay exceeding 179 minutes on {date}"
    stdscr.addstr(
        7,
        int(x / 2 - len(text6) / 2),
        text6,
    )

    text7 = f"There are {punctdata[0]['withdata']} trains with delay extracted from the PKP Intercity website"
    stdscr.addstr(
        9,
        int(x / 2 - len(text7) / 2),
        text7,
    )
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == "\x1b":  # escape
            menu12(stdscr, choice)


def menu114(stdscr, date, choice):
    y, x = window_check(stdscr)
    curses.curs_set(0)

    bottom = curses.newwin(1, x, y - 1, 0)  # nlines, ncols, begin y, begin x
    bottom.addstr("Press ESC to come back, i to scroll up, k to scroll down")
    bottom.refresh()

    if "list" in str(type(date)):
        occdata = mult_day_occ(date)
    else:
        occdata = day_occ(date)

    stdscr.addstr(
        0,
        int(x / 2 - len("Occupancy statistics") / 2),
        "Occupancy statistics",
        curses.A_STANDOUT,
    )

    if "list" in str(type(date)):
        text1 = f"{occdata[1]['<50']} of trains were occupied at below 50% capacity between {date[0]} and {date[-1]}"
    else:
        text1 = f"{occdata[1]['<50']} of trains were occupied at below 50% capacity on {date}"

    stdscr.addstr(
        2,
        int(x / 2 - len(text1) / 2),
        text1,
    )

    stdscr.addstr(
        y - 1,
        int(x / 2 - len("Print ESC to come back") / 2),
        "Print ESC to come back",
    )

    if "list" in str(type(date)):
        text2 = f"{occdata[1]['50-80']} of trains were occupied at between 50% and 80% capacity between {date[0]} and {date[-1]}"
    else:
        text2 = f"{occdata[1]['50-80']} of trains were occupied at between 50% and 80% capacity on {date}"
    stdscr.addstr(
        3,
        int(x / 2 - len(text2) / 2),
        text2,
    )

    if "list" in str(type(date)):
        text3 = f"{occdata[1]['>80']} of trains were occupied at over 80% capacity between {date[0]} and {date[-1]}"
    else:
        text3 = f"{occdata[1]['>80']} of trains were occupied at over 80% capacity on {date}"
    stdscr.addstr(
        4,
        int(x / 2 - len(text3) / 2),
        text3,
    )

    stdscr.addstr(
        y - 1,
        int(x / 2 - len("Print ESC to come back") / 2),
        "Print ESC to come back",
    )
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == "\x1b":  # escape
            if "list" in str(type(date)):
                menu12(stdscr, choice)
            else:
                menu11(stdscr, choice)


def printocc(
    mainpad, f1, maxlines, r, x, y, flag, filt
):  # similar to printdel, but with occcupancies instead
    # initial printing from a first train to the limit in lines
    mainpad.clear()
    nr = 0  # index of a last element shown on the screen
    while nr < maxlines - 1:
        try:
            if r == 1:
                mainpad.addstr(
                    f"{nr+1}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: occupancy {f1[nr]['occupancy']}\n",
                )
            if r == -1:
                mainpad.addstr(
                    f"{len(f1)-nr}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: occupancy {f1[nr]['occupancy']}\n",
                )
            nr += 1
        except IndexError:
            break
    mainpad.refresh(0, 0, 4, int(x / 2 - 90 / 2), y - 2, int(x / 2 + 108 / 2))
    if filt == 1:
        return (flag, r, filt)
    # obtional scrolling
    while True:
        c = mainpad.getkey()
        # downwards
        if c == "k":
            try:
                if r == 1:
                    mainpad.addstr(
                        f"{nr+1}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: occupancy {f1[nr]['occupancy']}\n",
                    )
                if r == -1:
                    mainpad.addstr(
                        f"{len(f1)-nr}. {f1[nr]['category']} {f1[nr]['number']} {f1[nr]['name']} {f1[nr]['date']} {f1[nr]['from']} - {f1[nr]['to']}: occupancy {f1[nr]['occupancy']}\n",
                    )
                nr += 1
                mainpad.refresh(
                    0, 0, 4, int(x / 2 - 90 / 2), y - 2, int(x / 2 + 108 / 2)
                )
            except IndexError:
                pass
        # upwards
        elif c == "i":
            if nr - maxlines >= 0:
                mainpad.clear()
                if r == 1:
                    for i in range(nr - maxlines, nr):  # range(0,18) od 1 do 19
                        mainpad.addstr(
                            f"{i}. {f1[i-1]['category']} {f1[i-1]['number']} {f1[i-1]['name']} {f1[i-1]['date']} {f1[i-1]['from']} - {f1[i-1]['to']}: occupancy {f1[i-1]['occupancy']}\n",
                        )
                if r == -1:
                    for i in range(nr - maxlines, nr):  # range(0,18) od 1 do 19
                        mainpad.addstr(
                            f"{len(f1)-i+1}. {f1[i-1]['category']} {f1[i-1]['number']} {f1[i-1]['name']} {f1[i-1]['date']} {f1[i-1]['from']} - {f1[i-1]['to']}: occupancy {f1[i-1]['occupancy']}\n",
                        )
                nr -= 1
                mainpad.refresh(
                    0, 0, 4, int(x / 2 - 90 / 2), y - 2, int(x / 2 + 108 / 2)
                )
        elif c == "\x1b":  # esc - quit
            flag = 0
            break
        elif c == "r":  # r-reverse order
            r = -r
            break
        elif c == "o":  # o-sort by occupancy
            flag = 1
            break
        elif c == "x":  # x-sort by train number
            flag = 2
            break
        elif c == "d":  # d-sort by departure station
            flag = 3
            break
        elif c == "a":  # a-sort by arrival station
            flag = 4
            break
        elif c == "n":  # n-sort by train name
            flag = 5
            break
        elif c == "f":  # f-filters
            filt = -filt
            break
    return (flag, r, filt)


def validate(str):
    try:
        return int(str[:1]) if int(str[:1]) < 5 else 0
    except ValueError:
        return 0


def validate_date(str):  # check the date, reject a future one
    yy, mm, dd = str.split("-")
    td = date.today()
    try:
        dt = date(int(yy), int(mm), int(dd))
        if dt > td:
            return False
        else:
            return True
    except ValueError:
        return False


def window_check(scr):
    y, x = scr.getmaxyx()
    if x < 96 or y < 8:
        scr.addstr("The window is too small and content cannot be printed")
        scr.refresh()
        time.sleep(5)
        sys.exit()
    else:
        return y, x


if __name__ == "__main__":
    wrapper(main)
