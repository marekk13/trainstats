import json


def day_punct(
    day,
):  # returns a dict consisting of percentages regardning punctuality for a given day
    with open(f"json/trains_{day}.json", "r") as file:
        f = json.load(file)
    delint = {
        "withdata": 0,  # number of trains with delay data assigned
        "nodelay": 0,
        "m10": 0,
        "m30": 0,
        "m60": 0,
        "m180": 0,
        "m180p": 0,
    }
    for train in f:
        if not "n/a" in train["delay"]:
            delint["withdata"] += 1
            if train["delay"].split(" ")[0] == "0":
                delint["nodelay"] += 1
            elif int(train["delay"].split(" ")[0]) < 10:
                delint["m10"] += 1
            elif int(train["delay"].split(" ")[0]) < 30:
                delint["m30"] += 1
            elif int(train["delay"].split(" ")[0]) < 60:
                delint["m60"] += 1
            elif int(train["delay"].split(" ")[0]) < 180:
                delint["m180"] += 1
            else:
                delint["m180p"] += 1
    return (
        delint,
        {
            "nodelay": f"{round(100*(delint['nodelay']/delint['withdata']))}%",  # percentage of trains with 0min delay
            "m10": f"{round(100*(delint['m10']/delint['withdata']))}%",  # percentage of trains with 1-9min delay
            "m30": f"{round(100*(delint['m30']/delint['withdata']))}%",  # percentage of trains with 10-29min delay
            "m60": f"{round(100*(delint['m60']/delint['withdata']))}%",  # percentage of trains with 30-59min delay
            "m180": f"{round(100*(delint['m180']/delint['withdata']))}%",  # percentage of trains with 60-179min delay
            "m180p": f"{round(100*(delint['m180p']/delint['withdata']))}%",  # percentage of trains with >179min delay
        },
    )


def day_occ(day):
    with open(f"json/trains_{day}.json", "r") as file:
        f = json.load(file)
    occint = {"all": 0, "<50": 0, "50-80": 0, ">80": 0}
    for train in f:
        occint["all"] += 1
        if "poniżej" in train["occupancy"]:
            occint["<50"] += 1
        elif "50%-80%" in train["occupancy"]:
            occint["50-80"] += 1
        else:
            occint[">80"] += 1
    return (
        occint,
        {
            "<50": f"{round(100*(occint['<50']/occint['all']))}%",
            "50-80": f"{round(100*(occint['50-80']/occint['all']))}%",
            ">80": f"{round(100*(occint['>80']/occint['all']))}%",
        },
    )


def mult_day_punct(l):
    flist = []
    for day in l:
        with open(f"json/trains_{day}.json", "r") as file:
            flist.append(json.load(file))
    delint = {
        "withdata": 0,  # number of trains with delay data assigned
        "nodelay": 0,
        "m10": 0,
        "m30": 0,
        "m60": 0,
        "m180": 0,
        "m180p": 0,
    }
    for f in flist:
        for train in f:
            if not "n/a" in train["delay"]:
                delint["withdata"] += 1
                if train["delay"].split(" ")[0] == "0":
                    delint["nodelay"] += 1
                elif int(train["delay"].split(" ")[0]) < 10:
                    delint["m10"] += 1
                elif int(train["delay"].split(" ")[0]) < 30:
                    delint["m30"] += 1
                elif int(train["delay"].split(" ")[0]) < 60:
                    delint["m60"] += 1
                elif int(train["delay"].split(" ")[0]) < 180:
                    delint["m180"] += 1
                else:
                    delint["m180p"] += 1
    return (
        delint,
        {
            "nodelay": f"{round(100*(delint['nodelay']/delint['withdata']))}%",  # percentage of trains with 0min delay
            "m10": f"{round(100*(delint['m10']/delint['withdata']))}%",  # percentage of trains with 1-9min delay
            "m30": f"{round(100*(delint['m30']/delint['withdata']))}%",  # percentage of trains with 10-29min delay
            "m60": f"{round(100*(delint['m60']/delint['withdata']))}%",  # percentage of trains with 30-59min delay
            "m180": f"{round(100*(delint['m180']/delint['withdata']))}%",  # percentage of trains with 60-179min delay
            "m180p": f"{round(100*(delint['m180p']/delint['withdata']))}%",  # percentage of trains with >179min delay
        },
    )


def mult_day_occ(l):
    flist = []
    for day in l:
        with open(f"json/trains_{day}.json", "r") as file:
            flist.append(json.load(file))
    occint = {"all": 0, "<50": 0, "50-80": 0, ">80": 0}
    for f in flist:
        for train in f:
            occint["all"] += 1
            if "poniżej" in train["occupancy"]:
                occint["<50"] += 1
            elif "50%-80%" in train["occupancy"]:
                occint["50-80"] += 1
            else:
                occint[">80"] += 1
    return (
        occint,
        {
            "<50": f"{round(100*(occint['<50']/occint['all']))}%",
            "50-80": f"{round(100*(occint['50-80']/occint['all']))}%",
            ">80": f"{round(100*(occint['>80']/occint['all']))}%",
        },
    )
