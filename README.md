# trainstats
> A terminal application displaying data about delays of trains run by the Polish main railroad carrier - PKP Intercity.
> Data sources are JSON files created by an automatically run script that scrapes the intercity.pl website.


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)


## General Information
- I undertook the project to finish CS50p and to make practical use of the knowledge gained during the course.

- Detailed data about past delays of the trains isn't shared with the public in Poland and some railway enthusiasts might be interested in it. What's more, public companies (such as PKP Intercity) should be monitored and I believe that checking delay statistics might be a way to assess its efficiency. The purpose of my project is to address these issues.

- One of the files, getdata.py is responsible for scraping the data from the intercity.pl website using requests-HTML,
clearing it, and storing it in a JSON file. One JSON file represents information from one day.

- On the intercity.pl website, information about delays is hidden after a train terminates.
If the scraping script is run frequently, for example, every 5 or 10 minutes all day, it allows us to get data about the final delay of every PKP Intercity train during
the day.

- A dictionary in a resulting JSON file represents one train on a given day and consists of information on whether
a train is domestic or international, its number, category, name, departure and arrival stations, projected occupancy, delay, and date.

## Technologies Used
- python - version 3.6


## Features

- One of the features lets you see a list of train delays for a day or a multi-day period. By default, it sorts a list by the biggest delay.
<img width="958" alt="sc1" src="https://user-images.githubusercontent.com/109167046/212196180-aca42040-ea8d-4b5c-af08-0e366c0dbe8c.png">
<img width="958" alt="sc2" src="https://user-images.githubusercontent.com/109167046/212196190-3345bb1b-82b0-425b-b635-f575e764130b.png">

- The application handles sorting and filtering a list with a limit of 3 filters. Reversed order is also implemented.
<img width="959" alt="sc3" src="https://user-images.githubusercontent.com/109167046/212196199-64c414e7-56cb-4ac0-9f2f-174f98346e8d.png">

- There is a similar menu regarding occupancies.
<img width="959" alt="sc4" src="https://user-images.githubusercontent.com/109167046/212196206-674b397c-1b9c-4d21-bd52-3a3f0f9c2b5a.png">
<img width="959" alt="sc5" src="https://user-images.githubusercontent.com/109167046/212196211-03021dcc-2e5b-4300-9501-0666a264ed89.png">

- Moreover, you can check out delay and occupancy statistics.
<img width="960" alt="sc6" src="https://user-images.githubusercontent.com/109167046/212196221-26be8533-df5c-4e44-9a3f-229078abaaa8.png">

- If there is no file for a day or one of the days inputted by a user, the fitting message is printed out and the user is prompted for the input again.
<img width="955" alt="sc7" src="https://user-images.githubusercontent.com/109167046/212196231-573a7e07-1f6f-48e4-a796-79ddc0474cf9.png">


## Project Status
The project is no longer being worked on since I need to focus more on university classes. In the future, I'd like to make improvements as detailed below.


## Room for Improvement
In my view, the execution time of getdata.py needs to be shortened significantly. I'd like to achieve this using asynchronous programming.
The biggest obstacle I encountered while developing a project was executing getdata.py 24/7. I remained unsuccessful despite trying multiple ways, such as Windows Task Scheduler,
pythonanywhere.com, and using a Linux account on my university's student server. It makes the resulting JSON files much less credible
because the task set on Task Scheduler is launched only with my laptop being on. Therefore, there is a possibility that a delay had been scraped and later Windows Task Scheduler failed to launch a task and didn't update it. This would mean that delay in a JSON file isn't a final one, what was intended.

#### To–dos:
- Creating an asynchronous version of getdata.py
- Finding a way to execute getdata.py non-stop


## Acknowledgements
Making this project wouldn't be possible without the knowledge gained during CS50p classes.
Moreover, videos by [@John Watson Rooney](https://www.youtube.com/@JohnWatsonRooney) helped me immensely
with getting my head around web scraping.
[@Tech With Tim](https://www.youtube.com/@TechWithTim) series on Curses library introducted me to it.
