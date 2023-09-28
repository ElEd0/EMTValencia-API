import requests
import json
import xml.etree.ElementTree as ET


EMT_BUS_TIMES_URL = "https://www.emtvalencia.es/EMT/mapfunctions/MapUtilsPetitions.php?sec=getSAE"
EMT_STOPS_IN_EXTENT_URL = "https://www.emtvalencia.es/opentripplanner-api-webapp/ws/metadata/stopsInExtent"


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/98.0',
	'Accept': '*/*',
	'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
	'Referer': 'https://www.emtvalencia.es',
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
}
	
def get_from_url(url, params):
	r = requests.get(url, params=params, headers=headers)
	if r.status_code == 200:
		return r.text
	else:
		raise Exception("Request status code: " + str(r.status_code))



def get_bus_times(stop, bus = 0, adaptados = False):

	data = {
		'parada': str(stop),
		'adaptados': "true" if adaptados else "false"
	}
	if bus != 0:
		data['linea'] = bus

	# call API
	responseText = get_from_url(EMT_BUS_TIMES_URL, data)
	root = ET.fromstring(responseText)

	if root.tag != "estimacion":
		raise Exception("Invalid XML body: No tag 'estimacion' found in root")

	results = []

	for bus in root[0]:
		if bus.tag != "bus":
			continue
			
		# no minutos or horallegada = error
		if len(bus) == 3:
			results.append({
				'error': bus[2].text
			})
			continue

		if len(bus) != 5:
			results.append({
				'error': "Invalid bus response: "+str(len(bus))+" tags found, expected 5"
			})
			continue

		linea = bus[0].text
		destino = bus[1].text
		minutos = bus[2].text
		horaLlegada = bus[3].text
		error = bus[4].text
		
		# fix encoding in destino
		try:
			destino = destino.encode("latin-1").decode("utf-8")
		except Exception:
			pass

		if error != None:
			results.append({
				'error': error
			})
			continue

		busResult = {
			'linea': linea,
			'destino': destino
		}

		# 'minutos' or 'horaLlegada'
		if minutos != None:

			if "min." in minutos:
				busResult['minutos'] = int(minutos.replace(" min.", ""))
			elif minutos[0:2] == "Pr":
				busResult['minutos'] = 1
			else:
				busResult['minutos'] = "error"

		elif horaLlegada != None:

			busResult['horaLlegada'] = horaLlegada

		else:
			results.append({
				'error': 'No time data'
			})
			continue

		results.append(busResult)

	return results



def get_stops_in_extent(lowerLat, lowerLon, upperLat, upperLon):

	data = {
		'lowerCornerLat': lowerLat,
		'lowerCornerLon': lowerLon,
		'upperCornerLat': upperLat,
		'upperCornerLon': upperLon,
	}

	results = []
	
	responseText = get_from_url(EMT_STOPS_IN_EXTENT_URL, data)

	if responseText[0] == "{": #is json

		responseJson = json.loads(responseText)
		if responseJson == None:
			raise Exception("Invalid JSON body")
			
		results = responseJson['stop']

		for stop in results:
			rtI = stop['routes']['rtI']
			if isinstance(rtI, dict):
				rtI = [rtI]
			stop['routes'] = rtI

	else: #is xml (maybe?)
		# the following code is untested
		if root.tag != "stops":
			raise Exception("Invalid XML body: No tag 'stops' found in root")

		for stop in root:
			if stop.tag != "stop":
				continue
				
			if len(stop) != 6:
				results.append({
					'error': "Invalid stop response: "+str(len(stop))+" tags found, expected 5"
				})
				continue

			lat = stop[0].text
			lon = stop[1].text
			name = stop[2].text
			routesTag = stop[3]
			stopId = stop[4].text
			ubication = stop[5].text

			routes = []
			for rtI in routesTag:
				if rtI.tag == "rtI":
					routes.append({
						'headSign': rtI[0].text,
						'lineaId': rtI[1].text,
						'lineaName': rtI[2].text,
						'lineaNumber': rtI[3].text,
						'type': rtI[4].text
					})

			results.append({
				'lat': lat,
				'lon': lon,
				'name': name,
				'routes': routes,
				'stopId': stopId,
				'ubication': ubication
			})

	return results
		

	