from requests.models import MissingSchema
from requests_html import HTMLSession
import requests
import sys
import json
from datetime import date
from itertools import zip_longest
import re
import os


def datajson():
    td = get_date()
    path = "/Users/Marek/.vscode/trainstats/json/trains_" + td + ".json"
    if not os.path.isfile(path):
        get_data1(td, f"json/trains_{td}.json")
    clear_data(f"json/trains_{td}.json")
    get_delay(f"json/trains_{td}.json", td)


def get_date():  # getting date format needed for the url
    return f"{date.today().year}-{date.today().month:02}-{date.today().day:02}"


def get_data1(date, fname):  # getting data from the website using requests_html
    s = HTMLSession()
    i = 1
    data = []  # initializing a list (which will consist of dicts)
    while (
        True
    ):  # this way we are not dependent on number of pages, after the last one we break out of the loop
        try:
            url = f"https://www.intercity.pl/pl/site/dla-pasazera/informacje/frekwencja.html?location=&date={date}&category%5Beic_premium%5D=eip&category%5Beic%5D=eic&category%5Bic%5D=ic&category%5Btlk%5D=tlk&page={i}"
            r = s.get(url)
            table = r.html.find("table")[0]  # first result for table
            # list comprehension for more compact code, skipping unnecessary data
            data.append(
                [d.text for d in row.find("td")[:5] + row.find("td")[6:]]
                for row in table.find("tr")[1:]
            )
            i += 1
        except IndexError:
            break
        except MissingSchema:
            sys.exit("Invalid URL provided (get_data1)")

    headers = [
        "domestic",
        "number",
        "category",
        "name",
        "from",
        "to",
        "occupancy",
        "delay",
        "date",
    ]

    res = []
    for j in range(i - 1):
        for train in data[
            j
        ]:  # each page from the website is data[j], so we iterate over them
            # appending resulting dicts to the list, adding delay field which will be filled later, default delay==0
            res.append(dict(zip_longest(headers, train, fillvalue="n/a")))

    for train in res:
        train["date"] = date

    with open(fname, "w") as file:
        json.dump(res, file, indent=2)


def get_delay(fname, date):
    # create a set of the stations
    with open(fname) as file:
        f = json.load(file)
    stations = set()
    for train in f:
        stations.add(train["to"])

    s = HTMLSession()

    for station in stations:
        searchstation = convert_station(
            station
        )  # converting names to the needed format
        # first we get a station id
        try:
            url = f"https://infopasazer.intercity.pl/index.php?p=stations&q={searchstation}"
            r = s.get(url)
            id = r.html.search("\"window.location='?{}'\"")[0]
        except TypeError:  # automatically excluding foreign stations - no results
            continue
        except (MissingSchema, requests.exceptions.InvalidSchema):
            print("Invalid URL provided (get_delay)")
            return 0
        except (requests.exceptions.ConnectionError, TimeoutError):
            print(
                f"Unable to load delays - page not responding\nError code: {r.status_code}"
            )
            return 0

        # having obtained the station id, we are now able to get the delay
        try:
            url2 = f"https://infopasazer.intercity.pl/index.php?{id}"
            r1 = s.get(url2)
            table = r1.html.find("table")[0]
            for row in table.find("tr")[1:]:
                if (
                    date == row.find("td")[2].text
                    and row.find("td")[1].text == "PKP Intercity"
                    and station in row.find("td")[3].text
                ):
                    for train in f:
                        if validate(  # look for a train in a json file for which delay info was found
                            train, row.find("td")[0].text, row.find("td")[3].text
                        ):

                            train["delay"] = row.find("td")[5].text
                            break

        except IndexError:
            print("No trains arriving at this station as of now\n\n")
            continue
        except (requests.exceptions.ConnectionError, TimeoutError):
            print(
                f"Unable to load delays - page not responding\nError code: {r1.status_code}"
            )
            return 0
    with open(fname, "w") as file:
        json.dump(f, file, indent=2)


def validate(dict, nr, fromto):
    try:
        if (
            nr.endswith(dict["name"])
            and fromto.endswith(dict["to"])
            and fromto.startswith(dict["from"])
        ):
            return True

        elif (
            nr.endswith(dict["name"])
            or (fromto.endswith(dict["to"]) and fromto.startswith(dict["from"]))
        ) and nr.split("/")[0] == dict["number"]:
            return True
        elif (
            nr.startswith(dict["number"])
            and fromto.endswith(dict["to"])
            and nr.endswith(dict["name"])
        ):
            return True

        elif nr.startswith(dict["number"]) and (
            fromto.endswith(dict["to"]) or fromto.startswith(dict["from"])
        ):
            if re.match(
                r"^\d{4,5}/\d(?: \(\d{2,3}\))?$", nr
            ):  # regex to exclude non EIP trains
                return True
        elif (
            dict["domestic"] == "Mi\u0119dzyn."
            and nr.endswith(dict["name"])
            and (re.search(r"\(\d{2,4}\)", nr).group(0))
            .replace("(", "")
            .replace(")", "")
            == dict["number"]
        ):
            return True
        elif nr.startswith(dict["number"][:4]) and nr[:7].endswith(dict["number"][4]):
            return True
        elif nr.startswith(dict["number"][:3]) and nr[:6].endswith(dict["number"][3]):
            return True
        else:
            return False
    except IndexError:
        pass


def convert_station(sstr):
    if sstr.startswith(
        "Łódź"
    ):  # in the case of stations in Łódź for some reason the website only reacts
        # when given the name without diacritical marks
        sstr = sstr.replace("Łódź", "Lodz")
    return sstr.replace(" ", "+")


def clear_data(fname):  # clearing some station names (to search delays easier)
    with open(fname, "r") as file:
        f = json.load(file)

    for train in f:
        if train["from"] == "Kraków Główny Osobowy":
            train["from"] = "Kraków Główny"
        if train["to"] == "Kraków Główny Osobowy":
            train["to"] = "Kraków Główny"

        if train["from"] == "Gdynia Główna Osobowa":
            train["from"] = "Gdynia Główna"
        if train["to"] == "Gdynia Główna Osobowa":
            train["to"] = "Gdynia Główna"

        if train["from"] == "Warszawa Gdańska Osobowa":
            train["from"] = "Warszawa Gdańska"
        if train["to"] == "Warszawa Gdańska Osobowa":
            train["to"] = "Warszawa Gdańska"

        if train["from"] == "Przemyśl":
            train["from"] = "Przemyśl Główny"
        if train["to"] == "Przemyśl":
            train["to"] = "Przemyśl Główny"

        if train["from"] == "Rzeszów":
            train["from"] = "Rzeszów Główny"
        if train["to"] == "Rzeszów":
            train["to"] = "Rzeszów Główny"

        if train["from"] == "Zielona Góra":
            train["from"] = "Zielona Góra Główna"
        if train["to"] == "Zielona Góra":
            train["to"] = "Zielona Góra Główna"

        if train["from"] == "Lublin":
            train["from"] = "Lublin Główny"
        if train["to"] == "Lublin":
            train["to"] = "Lublin Główny"

        if train["from"] == "Bielsko Biała Główna":
            train["from"] = "Bielsko-Biała Główna"
        if train["to"] == "Bielsko Biała Główna":
            train["to"] = "Bielsko-Biała Główna"

        if train["to"] == "Wrocław Gł./Przemyśl":
            train["to"] = "Przemyśl Główny"

        if train["to"] == "Świnoujście/Ustka":
            train["to"] = "Świnoujście"

        if train["to"] == "Krak\u00f3w G\u0142./Hrubiesz\u00f3w M.":
            train["to"] = "Kraków Główny"

        if train["to"] == "Lublin/Hrubiesz\u00f3w Miasto":
            train["to"] = "Lublin Główny"

        if "." in train["name"] or "-" in train["name"]:
            train["name"] = ""

    with open(fname, "w") as file:
        json.dump(f, file, indent=2)


if __name__ == "__main__":
    datajson()
