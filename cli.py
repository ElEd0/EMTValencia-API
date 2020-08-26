import sys
from emtvlc import EMTVLC
import json

argv_len = len(sys.argv)

if argv_len == 1:
	print("\n  Syntax:  cli.py parada [linea] [adaptados]")
	exit()

parada = sys.argv[1]
bus = 0
adaptados = False
if not parada.isdigit():
	print("Invalid value for param 'parada'")
	exit()

if argv_len > 2:
	bus = sys.argv[2]

if argv_len > 3:
	adaptados = sys.argv[3].lower()
	adaptados = (adaptados == "1" or adaptados == "true")


msg = "Parada " + parada
if bus != 0:
	msg += " Linea: " + bus
if adaptados:
	msg += " Adaptados: true"

print(msg)

response = EMTVLC().get_bus_times(parada, bus, adaptados)

for estimation in response:

	if 'error' in estimation:
		print("\t" + estimation['error'])
		continue
		
	timeMsg = ""
	if 'minutos' in estimation:
		timeMsg = estimation['minutos'] + " minutes left"
	elif 'horaLlegada' in estimation:
		timeMsg = estimation['horaLlegada']
		
	print("\t" + estimation['linea'] + " (" + estimation['destino'] + "): " + timeMsg)

#print(response)


#f = open('response.json', 'w')
#f.write(json.dumps(response))
	
