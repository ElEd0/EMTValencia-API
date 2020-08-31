import xml.etree.ElementTree as ET
import requests
import json


EMT_BUS_TIMES_URL = "https://www.emtvalencia.es/EMT/mapfunctions/MapUtilsPetitions.php?sec=getSAE"
EMT_STOPS_IN_EXTENT_URL = "https://www.emtvalencia.es/opentripplanner-api-webapp/ws/metadata/stopsInExtent"

class EMTApiException(Exception):

	def __init__(self, errorCode, message):
		self.errorCode = errorCode
		self.message = message
	
	def __str__(self):
		return self.errorCode + ": " + self.message

class EMTVLC:
	
	#def __init__(self):
	#	pass
	
	def get_from_url(self, url, params):
		
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
			'Accept': '*/*',
			'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
			'Referer': 'https://www.emtvalencia.es',
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
		}
		
		r = requests.get(url, params=params, headers=headers)
		
		if r != None and r.status_code == 200:
			responseText = r.text
			#print(responseText)
			#f = open('response.xml', 'w')
			#f.write(responseText)
			return responseText
		else:
			raise EMTApiException("REQUEST", "API not accessible")
	
	def get_bus_times(self, stop, bus = 0, adaptados = False):
		
		data = {
			'parada': str(stop),
			'adaptados': "true" if adaptados else "false"
		}
		if bus != 0:
			data['linea'] = bus
		
		# call API
		responseText = self.get_from_url(EMT_BUS_TIMES_URL, data)
		root = ET.fromstring(responseText)
		
		if root.tag != "estimacion":
			raise EMTApiException("XML", "Invalid XML body")
		
		results = []
		
		for bus in root[0]:
			#filter out 'info' elements
			if bus.tag == "bus":
			
				# no minutos or horallegada = error
				if len(bus) == 3:
					results.append({
						'error': bus[2].text
					})
					continue
				
				if len(bus) != 5:
					results.append({
						'error': "Invalid bus response"
					})
					continue
				
				linea = bus[0].text
				destino = bus[1].text
				minutos = bus[2].text
				horaLlegada = bus[3].text
				error = bus[4].text
				
				#has error tag
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
						busResult['minutos'] = minutos.replace(" min.", "")
					elif bytes(minutos, "utf-8") == "Próximo":
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

	def get_stops_in_extent(self, lowerLat, lowerLon, upperLat, upperLon):
		
		data = {
			'lowerCornerLat': lowerLat,
			'lowerCornerLon': lowerLon,
			'upperCornerLat': upperLat,
			'upperCornerLon': upperLon,
		}
		
		results = []
		# call API
		responseText = self.get_from_url(EMT_STOPS_IN_EXTENT_URL, data)
		
		if responseText[0] == "{": #is json
			
			responseJson = json.loads(responseText)
			results = responseJson['stop']
			
			for stop in results:
				rtI = stop['routes']['rtI']
				if isinstance(rtI, dict):
					rtI = [rtI]
				stop['routes'] = rtI
		
		else: #is xml (maybe?)
			# the following code is untested
			if root.tag != "stops":
				raise EMTApiException("XML", "Invalid XML body")
			
			for stop in root:
				#filter out elements
				if stop.tag == "stop":
					
					if len(stop) != 6:
						results.append({
							'error': "Invalid stop response"
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
		














	