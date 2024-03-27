import aiohttp 
import asyncio 
import my_requests
import PySimpleGUI as ps

def getPoint(str):
  str = str.split(", ")
  lat = float(str[0].split("(")[1])
  lng = float(str[1].split(")")[0])
  return lat, lng

def setButtons(window, locations):
  window["buttons"].update(visible=True)
  for i in range(len(locations)):
    window[str(i)].update(locations[i][0] + " (" + str(locations[i][1]) + ", " + str(locations[i][2]) + ")", visible=True)
    
def invisButtons(window):
  window["buttons"].update(visible=False)
  for i in range(20):
    window[str(i)].update(visible=False)
  
weather_field = ['main', 'description', 'icon', 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity', 'sea_level', 'grnd_level']

def setWeather(window, weather):
  window["weather"].update(visible=True)
  for i in weather_field:
    if (i in weather):
      if (i in ["temp", "feels_like", "temp_min", 'temp_max']):
        s = str(round(weather[i] - 273.15, 2)) + "°C"
      else: 
        s = str(weather[i])
    else:
      s = "N/A"
    window[i].update(i + ": " + s, visible=True)
    
def invisWeather(window):
  window["weather"].update(visible=False)

def setFeatures(window, features):
  window["features"].update(visible=True)
  #window["text"].update(features)

def invisFeatures(window):
  window["features"].update(visible=False)

async def main():
  
  but_layout = []
  for i in range(20):
    but_layout.append([ps.Button("", visible=False, key=str(i))])

  weather_layout = []
  for i in weather_field:
    weather_layout.append([ps.Text(i, visible=False, key=str(i))])

  map_layout = [[ps.Output(visible=True, key="output", size=(100, 100), expand_x=True, expand_y=True)]]

  layout = [
    [ps.Text("Enter a location: "), ps.InputText(key="location")],
    [ps.Button("Submit")],
    [ps.Column(layout=but_layout, visible=False, key="buttons",scrollable=True, vertical_scroll_only=True, expand_y=True, expand_x=True, size=(100, 100)),
     ps.Column(layout=weather_layout, visible=False, key="weather"),
     ps.Column(layout=map_layout, visible=False, key="features", scrollable=True, vertical_scroll_only=True, expand_y=True, expand_x=True, size=(100, 100))],
  ]

  window = ps.Window("Lab 3", layout=layout, size=(1000, 400), resizable=True)
  
  while True:
    event, values = window.read()
    if event == ps.WIN_CLOSED:
      break
    if event == "Submit":
      invisWeather(window=window)
      invisFeatures(window=window)
      task = asyncio.create_task(my_requests.getNameLocations(values["location"]))
      locations = await task
      setButtons(window, locations)
    else:
      invisButtons(window)
      button_text = window[event].get_text()
      lat, lng = getPoint(button_text)
      task_weather = asyncio.create_task(my_requests.getWeather(lat, lng))
      task_map = asyncio.create_task(my_requests.getTripMap(lat, lng))
      weather = await task_weather
      map = await task_map
      descr_tasks = {}
      for i in map:
        descr_tasks[i] = asyncio.create_task(my_requests.getLocationDiscr(map[i]))
      text = ""
      for i in map:
        text += i + "\n"
        descr = await descr_tasks[i]
        if ('wikipedia_extracts' in descr):
          text += str(descr['wikipedia_extracts']['text']) + "\n\n"
        elif ('info' in descr):
          text += str(descr['info']) + "\n\n"
        else:
          text += "Description not found\n\n"
      print(text)
      setWeather(window, weather)
      setFeatures(window, text)
      
asyncio.get_event_loop().run_until_complete(main())
