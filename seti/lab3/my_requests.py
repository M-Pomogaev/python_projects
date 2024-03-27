import aiohttp 
import asyncio 

key = "1220a472-7909-4c28-9ea3-246f3742c083"
weather_key = "679415e2c86c5e279482ed2736284bf8"
trip_map_key = "5ae2e3f221c38a28845f05b634fda430964076a19d647023895f726a"
async def getResponseJson(session, url):
    async with session.get(url) as response:
        return await response.json()

async def getNameLocations(location):
    async with aiohttp.ClientSession() as session:
        url = f'https://graphhopper.com/api/1/geocode?q={location}&limit=20&key={key}'
        data = await getResponseJson(session, url)
        return [[hit['name'], hit['point']['lat'], hit['point']['lng']] for hit in data['hits']]

async def getWeather(lat, lng):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={weather_key}'
        data = await getResponseJson(session, url)
        return dict(list(data['weather'][0].items()) + list(data['main'].items()))
    
async def getTripMap(lat, lng):
    async with aiohttp.ClientSession() as session:
        url = f'http://api.opentripmap.com/0.1/en/places/radius?lang=en&radius=1000&lon={lng}&lat={lat}&apikey={trip_map_key}'
        data = await getResponseJson(session, url)
        places = data['features']
        dictionary = {}
        for place in places:
            dictionary[place['properties']['name']] = place['id']
        dictionary.pop("", "")
        return dictionary
    
    
async def getLocationDiscr(xid):
    async with aiohttp.ClientSession() as session:
        url = f'http://api.opentripmap.com/0.1/ru/places/xid/{xid}?xid={xid}&apikey={trip_map_key}'
        data = await getResponseJson(session, url)
        return data

async def main():
    global num
    task = asyncio.create_task(getNameLocations('Berlin'))
    return [hit['name'] for hit in await task]
