import tkinter as tk

import requests

API_KEY = "a27efb97ebb297ba41e8b21dc9eac996"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather():
    city = city_entry.get()

    if city == "":
        result_label.config(text="Please enter a city name")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            condition = data["weather"][0]["description"]

            result = (
                f"City: {city}\n"
                f"Temperature: {temp} °C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind} m/s\n"
                f"Condition: {condition.capitalize()}"
            )
            result_label.config(text=result)

        else:
            result_label.config(text="City not found")

    except:
        result_label.config(text="Error fetching data")

app = tk.Tk()
app.title("Weather App")
app.geometry("350x350")

tk.Label(app, text="Weather App", font=("Arial", 16, "bold")).pack(pady=10)

city_entry = tk.Entry(app, width=25)
city_entry.pack(pady=5)

tk.Button(app, text="Get Weather", command=fetch_weather).pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 10), justify="left")
result_label.pack(pady=10)

app.mainloop()
