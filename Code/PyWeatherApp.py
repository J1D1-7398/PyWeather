import tkinter as tk
import json, time, requests


try:
    def log(log_text):
        with open("PyWeatherApp.log", "a") as logging:
            logging.write(f"{time.ctime()}: {log_text}\n")
    log("Starting")
    log("Defining functions")
    def close_button_action():
        log("Stopping")
        exit()
    def clock_update():
        clock.config(text=f"It is {time.ctime()}")
        clock.after(1000, clock_update)
    def confiramtion_button_press_ask_for_info():
        log("Checking if all fields are filled out")
        api_key_for_weather_requests = api_key_ask_for_info_entry.get()
        address_ask_for_info_result = address_ask_for_info_entry.get()
        region_ask_for_info_result = region_ask_for_info_entry.get()
        if address_ask_for_info_result != "" and region_ask_for_info_result != "" and api_key_for_weather_requests != "":
            log("All fields are filled out")
            name_ask_for_info_result = name_ask_for_info_entry.get()
            if name_ask_for_info_result == "":
                log("Setting Default name as name was not provided")
                name_ask_for_info_result = "Default"
            data_to_write_ask_for_info = {"name": name_ask_for_info_result, "address": address_ask_for_info_result, "region": region_ask_for_info_result, "api-key": api_key_for_weather_requests}
            global info_content
            info_content = data_to_write_ask_for_info
            log("Writing info to file")
            with open("PyUtilsEssentialInfo.json", "w") as write_info:
                json.dump(data_to_write_ask_for_info, write_info, indent=2)
            ask_for_info_window.destroy()
        else:
            log("Need at least the address, region and the API Key")
            need_at_least_address_region_and_api_error.place(relx=0.5, rely=0.9, anchor="center")
    def region_cheat_sheet():
        log("Checking if required values are met for getting a region list for selected city")
        api_key_for_weather_requests_region_list = api_key_ask_for_info_entry.get()
        address_ask_for_info_result_region_list = address_ask_for_info_entry.get()
        if address_ask_for_info_result_region_list != "" and api_key_for_weather_requests_region_list != "":
            log("Requesting a region list")
            get_available_regions_for_selected_city = requests.get(f"https://freeopenapi.dev/api/v1/weather/geocode?city={address_ask_for_info_result_region_list}", headers={"X-Api-Key": api_key_for_weather_requests_region_list})
            log("Configuring Region Cheat Sheet window")
            region_options_window = tk.Tk()
            region_options_window.title("PyUtils Region Selection")
            region_options_window.geometry(f"{ask_for_info_window.winfo_screenwidth()/3:.0f}x{ask_for_info_window.winfo_screenheight()/1.5:.0f}")
            region_options_window.config(bg="#1f1f1f")
            log("Checking for errors while getting region list")
            if get_available_regions_for_selected_city.json()[next(iter(get_available_regions_for_selected_city.json()))] == "rate_limit_exceeded":
                tk.Label(region_options_window, text="\n    Rate Limit Exceeded!    \n    You have reached your limit of requests today    \n    Limits resets at 00:00 UTC    \n", font=("arial", 15, "bold"), bg="#3a3a3a", fg="#f1f1f1", justify="left", borderwidth = 2, relief = "raised").pack(fill="both")
                log("Region Cheat Sheet: Rate Limit Exceeded!")
            if get_available_regions_for_selected_city.json()[next(iter(get_available_regions_for_selected_city.json()))] == "invalid_api_key":
                log("Region Cheat Sheet: Invalid API Key!")
                tk.Label(region_options_window, text="\n    Invalid API Key!    \n    Please ensure you have entered a valid API Key    \n", font=("arial", 15, "bold"), bg="#3a3a3a", fg="#f1f1f1", justify="left", borderwidth = 2, relief = "raised").pack(fill="both")
            if get_available_regions_for_selected_city.json()[next(iter(get_available_regions_for_selected_city.json()))] == address_ask_for_info_result_region_list:
                available_regions = ""
                log("Listing available Regions")
                for i in get_available_regions_for_selected_city.json()["results"]:
                    available_regions += f"\n   {i["admin1"]}   "
                tk.Label(region_options_window, text=f"\n   {get_available_regions_for_selected_city.json()["query"]}:   \n{available_regions}\n", font = ("arial", 15, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised", justify="left", anchor="nw").pack(fill="both", expand=True)
        else:
            log("Need at least the address and the API Key!")
            need_at_least_address_and_api_error.place(relx=0.5, rely=0.9, anchor="center")
    def get_my_api_key():
        log("Configuring Get My API Key window")
        region_options_window = tk.Tk()
        region_options_window.title("PyUtils get API key")
        region_options_window.geometry(f"{ask_for_info_window.winfo_screenwidth()/3:.0f}x{ask_for_info_window.winfo_screenheight()/3:.0f}")
        region_options_window.config(bg="#1f1f1f")
        log("Defining an extra function")
        def send_API_key_to_email():
            log("Sending email for API Key request")
            confirmation_of_sent_email = requests.post("https://freeopenapi.dev/api/v1/keys", json={"email": str(email_to_send_api_key_to_entry.get())})
            tk.Label(region_options_window, text=f"    {confirmation_of_sent_email.json()["message"].replace(". Click it", ".    \n    Click it").replace("to verify ", "to verify    \n    ")}    ", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.8, anchor="center")
        tk.Label(region_options_window, text="Enter the email you want the API key to be sent to *", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.1, anchor="center")
        log("Generating Get My API Key window content")
        email_to_send_api_key_to_entry = tk.Entry(region_options_window, bg="#5a5a5a", fg="#f1f1f1", borderwidth = 2, relief="sunken", width=40)
        email_to_send_api_key_to_entry.place(relx=0.5, rely=0.3, anchor="center")
        tk.Button(region_options_window, text="Send API key", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised", activebackground="#5a5a5a", activeforeground="#f1f1f1", command=send_API_key_to_email).place(relx=0.5, rely=0.6, anchor="center")
    log("Functions defined")
    log("Creating necessary files")
    with open("PyUtilsEssentialInfo.json", "a") as create_file:
        create_file.write("")
    with open("PyUtilsEssentialInfo.json", "r") as read_info:
        log("Checking if app already has enough info")
        try:
            info_content = json.load(read_info)
            log("App has enough info, starting main window")
        except:
            log("App does not have enough info, starting ask_for_info_window")
            log("Configuring ask for info window appearance")
            ask_for_info_window = tk.Tk()
            ask_for_info_window.title("PyUtils Info Required")
            ask_for_info_window.geometry(f"{ask_for_info_window.winfo_screenwidth()/3:.0f}x{ask_for_info_window.winfo_screenheight()/1.5:.0f}")
            ask_for_info_window.config(bg="#1f1f1f")
            ask_for_info_window.resizable(False, False)
            ask_for_info_window.protocol("WM_DELETE_WINDOW", lambda: None)
            log("Configuring ask for info window content")
            tk.Label(ask_for_info_window, text="Fields marked with * are required", font = ("arial", 15, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.05, anchor="center")
            tk.Label(ask_for_info_window, text="Enter your name (For welcome screen)", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.15, anchor="center")
            name_ask_for_info_entry = tk.Entry(ask_for_info_window, bg="#5a5a5a", fg="#f1f1f1", borderwidth = 2, relief="sunken")
            tk.Label(ask_for_info_window, text="Enter the city to measure the weather from *", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.3, anchor="center")
            address_ask_for_info_entry = tk.Entry(ask_for_info_window, bg="#5a5a5a", fg="#f1f1f1", borderwidth = 2, relief="sunken")
            tk.Label(ask_for_info_window, text="Enter the region of the city *", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.45, anchor="center")
            region_ask_for_info_entry = tk.Entry(ask_for_info_window, bg="#5a5a5a", fg="#f1f1f1", borderwidth = 2, relief="sunken")
            tk.Label(ask_for_info_window, text="Enter your freeopenapi.dev API key *", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised").place(relx=0.5, rely=0.6, anchor="center")
            api_key_ask_for_info_entry = tk.Entry(ask_for_info_window, bg="#5a5a5a", fg="#f1f1f1", borderwidth = 2, relief="sunken")
            tk.Button(ask_for_info_window, text="Confirm", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#4a4a4a", borderwidth = 2, relief= "raised", activebackground="#5a5a5a", activeforeground="#f1f1f1", command=confiramtion_button_press_ask_for_info).place(relx=0.5, rely=0.75, anchor="center")
            need_at_least_address_region_and_api_error = tk.Label(ask_for_info_window, text="Please ensure you have filled out the required entries!", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#5a5a5a", borderwidth = 2, relief= "raised")
            need_at_least_address_and_api_error = tk.Label(ask_for_info_window, text="Please ensure you have filled out API key and City!", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#5a5a5a", borderwidth = 2, relief= "raised")
            tk.Button(ask_for_info_window, text="X", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#5a5a5a", borderwidth = 2, relief= "raised", command=close_button_action).place(relx=0.95, rely=0.05, anchor="center")
            tk.Button(ask_for_info_window, text="?", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#5a5a5a", borderwidth = 2, relief= "raised", command=region_cheat_sheet).place(relx=0.75, rely=0.525, anchor="center")
            tk.Button(ask_for_info_window, text="?", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#5a5a5a", borderwidth = 2, relief= "raised", command=get_my_api_key).place(relx=0.75, rely=0.675, anchor="center")

            name_ask_for_info_entry.place(relx=0.5, rely=0.225, anchor="center")
            address_ask_for_info_entry.place(relx=0.5, rely=0.375, anchor="center")
            region_ask_for_info_entry.place(relx=0.5, rely=0.525, anchor="center")
            api_key_ask_for_info_entry.place(relx=0.5, rely=0.675, anchor="center")

            ask_for_info_window.mainloop()

            info_content = json.load(read_info)
    log("Configuring main window")
    main = tk.Tk()
    main.title("PyUtils")
    main.geometry(f"{main.winfo_screenwidth()/2:.0f}x{main.winfo_screenheight()/1.3:.0f}")
    main.config(bg="#1f1f1f")
    main.protocol("WM_DELETE_WINDOW", lambda: None)

    log("Configuring main window content")
    tk.Label(main, text=f"Welcome {info_content["name"]}!", font=("arial", 30, "bold"), bg="#1f1f1f", fg="#f1f1f1", justify="left").place(relx=0.02, rely=0.06)
    tk.Button(main, text="X", font = ("arial", 10, "bold"), fg="#f1f1f1", bg="#5a5a5a", borderwidth = 2, relief= "raised", command=close_button_action).place(relx=0.95, rely=0.05, anchor="center")
    log("Setting up clock")
    clock = tk.Label(main, text=f"It is {time.ctime()}", font=("arial", 15, "bold"), bg="#1f1f1f", fg="#f1f1f1")
    clock.place(relx=0.02, rely=0.14)
    clock_update()
    log("Getting coords for selected city")
    get_coords_from_city = requests.get(f"https://freeopenapi.dev/api/v1/weather/geocode?city={info_content["address"]}", headers={"X-Api-Key": info_content["api-key"]})
    if get_coords_from_city.json()[next(iter(get_coords_from_city.json()))] == "rate_limit_exceeded":
        log("Rate Limit Exceeded!")
        tk.Label(main, text="\n    Rate Limit Exceeded!    \n    You have reached your limit of requests today    \n    Limits resets at 00:00 UTC    \n", font=("arial", 15, "bold"), bg="#3a3a3a", fg="#f1f1f1", justify="left", borderwidth = 2, relief = "raised").place(relx=0.5, rely=0.1)
    elif get_coords_from_city.json()[next(iter(get_coords_from_city.json()))] == "invalid_api_key":
        log("Invalid API Key!")
        tk.Label(main, text="\n    Invalid API Key!    \n    Please ensure you have entered a valid API Key    \n", font=("arial", 15, "bold"), bg="#3a3a3a", fg="#f1f1f1", justify="left", borderwidth = 2, relief = "raised").place(relx=0.5, rely=0.1)
    else:
        log("Checking for selected region in recieved request")
        for i in get_coords_from_city.json()["results"]:
            if i["admin1"] == info_content["region"]:
                city_specifications = i
        log("Getting weather from selected city coords")
        get_weather_from_coords = requests.get(f"https://freeopenapi.dev/api/v1/weather/current?lat={city_specifications["latitude"]}&lon={city_specifications["longitude"]}", headers={"X-Api-Key": info_content["api-key"]})
        log("Parsing weather codes file")
        with open("PyUtilsWeatherCodes.json", "r") as read_weather_codes:
            weather_codes = json.load(read_weather_codes)
        log("Comparing current weather code with weather code list")
        current_weather_code = weather_codes["weather-codes"][str(get_weather_from_coords.json()["current"]["weatherCode"])]
        del weather_codes
        too_long_code_isTrue = False
        log("Shortening too long weather code")
        if len(current_weather_code) > 30:
            too_long_code_isTrue = True
            too_long_weather_code = ""
            line_for_too_long_weather_code = ""
            for i in current_weather_code.split():
                if len(line_for_too_long_weather_code) < 30:
                    line_for_too_long_weather_code += f"{i} "
                else:
                    too_long_weather_code += f"    {line_for_too_long_weather_code}   \n"
                    line_for_too_long_weather_code = f"{i} "
            too_long_weather_code += f"    {line_for_too_long_weather_code}   \n"
        log("Displaying all info")
        tk.Label(main, text=f"\n    Weather in {city_specifications["name"]}, {city_specifications["country"]}    \n    {city_specifications["admin1"]}    \n    Measures taken {get_weather_from_coords.json()["current"]["timestamp"].replace("T", " at ")}    \n\n    Temperature: {get_weather_from_coords.json()["current"]["temperatureC"]} °C    \n    Temperature feeling: {get_weather_from_coords.json()["current"]["apparentTemperatureC"]} °C    \n    Wind speed: {get_weather_from_coords.json()["current"]["windSpeedKmh"]} km/h    \n    Wind direction: {get_weather_from_coords.json()["current"]["windDirectionDeg"]} degrees    \n    Precipitation: {get_weather_from_coords.json()["current"]["precipitationMm"]} mm    \n    Weather code: {get_weather_from_coords.json()["current"]["weatherCode"]}    \n    ({too_long_weather_code.removesuffix("    \n").removeprefix("    ") if too_long_code_isTrue == True else current_weather_code})    \n\n    It is {"nighttime" if get_weather_from_coords.json()["current"]["isDay"] == False else "daytime"}    \n", font=("arial", 15, "bold"), bg="#3a3a3a", fg="#f1f1f1", justify="left", borderwidth = 2, relief = "raised").place(relx=0.02, rely=0.3)

    main.mainloop()
except Exception as e:
    log(f"General Error: {e}")
    log("Stopping")
    exit()
