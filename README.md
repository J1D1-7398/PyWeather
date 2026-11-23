# PyWeather
A simple weather app implemented in python

## Requirements:

- Python (For running source code)
- Python libraries:

  - json
  - time
  - requests
  - tkinter

For installation of python refer to https://github.com/J1D1-7398/Python-Installation-Tutorial

Any library, except for tkinter (which must be installed at the same time with python), can be installed with

```
pip install library-name
```

Where library-name is the library you are trying to install

## How to use:

Clone this github repo with
```
git clone https://github.com/J1D1-7398/PyWeather.git
```
Or download the zip file by clicking the green "<> Code" button and pressing "Download ZIP"

If you have downloaded the .zip file, extract it.

To run the program, just enter into the "Code" folder in the terminal and execute:
```
python PyWeatherApp.py
```
Or, on Windows, you can just double click the .py file IF you have it run in python automatically, you can select "Open With" and select python

In Windows if you have downloaded it from releases, double click the executable


When it is opened, it should be pretty easy to understand how it works

First window, will ask you:
- Your name (No need to enter one, it is just for the greeter)
- The city you want to measure the weather from (Ex: Paris, London, New York)
- The region of the city (There are lots of cities with the same name, Ex: Paris is in: France, Kentucky, Illinois...)
  - You will see a ? button, press it and it will reveal all the options (You will need a valid API Key and the city name) (You can't copy paste for the moment, sorry)
- Your API Key (For Weather API)
  - You will see a ? button, press it and it will ask you for an email, enter your email and it should send you the API key to your inbox, (It could be in spam, so check)

When you have filled in all the info, press Confirm and it will write down all info on a json

It will then open the main window with the current weather for that city

When you open it again, it should remember your info and directly display the weather

If you have any questions, feel free to send me an e-mail or post an issue on this repo!

J1D1.7398@gmail.com
