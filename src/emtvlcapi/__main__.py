import sys
import emtvlcapi
import json


def main():
	argv_len = len(sys.argv)

	if argv_len < 3:
		print("\n\tSyntax:  cli.py bus_times parada [linea] [adaptados]\n"
		"\tSyntax:  cli.py stops_in_extent lowerLat lowerLon upperLat upperLon\n")
		exit()

	method = sys.argv[1].lower()

	if method == "bus_times":

		parada = sys.argv[2]
		bus = 0
		adaptados = False
		if not parada.isdigit():
			print("Invalid value for param 'parada'")
			exit()

		if argv_len > 3:
			bus = sys.argv[3]

		if argv_len > 4:
			adaptados = sys.argv[4].lower()
			adaptados = (adaptados == "1" or adaptados == "true")


		msg = "Parada " + parada
		if bus != 0:
			msg += " Linea: " + bus
		if adaptados:
			msg += " Adaptados: true"

		print(msg)

		try:

			response = emtvlcapi.get_bus_times(parada, bus, adaptados)

		except Exception as e:
			print(e)
			exit()

		for estimation in response:

			if 'error' in estimation:
				print("\tError: " + estimation['error'])
				continue

			timeMsg = ""
			if 'minutos' in estimation:
				timeMsg = str(estimation['minutos']) + " minutes left"
			elif 'horaLlegada' in estimation:
				timeMsg = estimation['horaLlegada']

			print("\t" + estimation['linea'] + " (" + estimation['destino'] + "): " + timeMsg)


	elif method == "stops_in_extent":

		if argv_len < 6:
			print("Invalid number of arguments")
			exit()

		lLat = sys.argv[2]
		lLon = sys.argv[3]
		uLat = sys.argv[4]
		uLon = sys.argv[5]

		try:

			response = emtvlcapi.get_stops_in_extent(lLat, lLon, uLat, uLon)

		except Exception as e:
			print(e)
			exit()


		print("\nParadas en [", lLat, ",", lLon, ";", uLat, ",", uLon,"] ->")

		for stop in response:
			print("\n")
			print("\t" + stop['stopId'] + " - " + stop['name'])
			print("\t\tLatLon: " + stop['lat'] + ", " + stop['lon'])
			print("\t\tLineas: ")
			for linea in stop['routes']:
				print("\t\t\t" + linea['SN'] + " - " + linea['LN'])


	else:
		print("'" + method + "' is not a valid command")
		exit()

if __name__ == "__main__":
    main()
