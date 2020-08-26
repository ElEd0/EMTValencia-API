import xml.etree.ElementTree as ET
import requests


EMT_BUS_TIMES_URL = "https://www.emtvalencia.es/EMT/mapfunctions/MapUtilsPetitions.php?sec=getSAE"


class ApiException(Exception):

    def __init__(self, errorCode, message):
        self.errorCode = errorCode
        self.message = message
		

class EMTVLC:
	
    #def __init__(self):
	#	pass
	
	def get_bus_times(self, stop, bus = 0, adaptados = False):
		
		data = {
			'parada': str(stop),
			'adaptados': "true" if adaptados else "false"
		}
		if bus != 0:
			data['linea'] = bus
			
		print(data)
		
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
			'Accept': '*/*',
			'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
			'Referer': 'https://www.emtvalencia.es',
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
		}
		
		r = requests.get(EMT_BUS_TIMES_URL, params=data, headers=headers)
		
		if r != None and r.status_code == 200:
			responseText = r.text
			#print(responseText)
			return self.parse_xml(responseText)
		else:
			raise ApiException("REQUEST", "API not accessible")

	
	def parse_xml(self, xmlString):
		root = ET.fromstring(xmlString)
		
		if root.tag != "estimacion":
			raise ApiException("XML", "Invalid XML body")
		
		results = []
		
		for bus in root[0]:
			#filter out info elements
			if bus.tag == "bus":
			
				#has error tag
				if bus[4].text != None:
					results.append({
						'error': bus[4].text
					})
					continue
				
				busResult = {
					'bus': bus[0].text,
					'destination': bus[1].text.decode("utf-8")
				}
				
				# 'minutos' or 'horaLlegada'
				if bus[2].text != None:
				
					minutos = bus[2].text
					if "min." in minutos:
						busResult['time'] = minutos.replace(" min.", "")
					elif bytes(minutos, "utf-8") == "Próximo":
						busResult['time'] = 1
					else:
						busResult['time'] = "error"
					busResult['time_type'] = "minutes_left"
					
				elif bus[3].text != None:
				
					busResult['time'] = bus[3].text
					busResult['time_type'] = "time"
					
				else:
					results.append({
						'error': 'No time data'
					})
					continue
				
				results.append(busResult)
		
		return results
		


















	