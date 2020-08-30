# EMTVLC-API  

Python module that retrieves bus times for a given stop or stops within an extent.

Data from EMT valencia.

# Import

```
from emtvlc import EMTVLC
```

# Usage

All methods return a list containing the results

Get bus times for a given stop id and optionally a bus number:
```
>>> response = EMTVLC().get_bus_times(508)
>>> print(response)
[{'linea': '70', 'destino': 'Alboraia', 'minutos': '13'}, 
{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '15'}, 
{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '29'}, 
{'linea': '70', 'destino': 'Alboraia', 'minutos': '31'}, 
{'linea': 'N4', 'destino': 'Est.del Nord', 'horaLlegada': '22:41'}, 
{'linea': 'N4', 'destino': 'Est.del Nord', 'horaLlegada': '23:32'}]

>>> response = EMTVLC().get_bus_times(508, 93)
>>> print(response)
[{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '14'}, 
{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '28'}]

```

Get stops within the rectangle created by 2 lat-lon points in opposite corners:
```
>>> response = EMTVLC().get_stops_in_extent(39.471964, -0.394641, 39.474714, -0.405906)
>>> print(response)
[{
	'lat': '39.4720832588597', 
	'lon': '-0.40559318566979', 
	'name': "Nou d'Octubre (par) - Democràcia", 
	'routes': [
		{'headSign': 'Tres Creus', 'id_linea': '73', 'LN': 'Tres Creus', 'SN': '73', 'type': 'A'}, 
		{'headSign': 'Hospital General', 'id_linea': '95', 'LN': 'Hospital General', 'SN': '95', 'type': 'A'}, 
		{...}
	], 
	'stopId': '2070', 
	'ubica': 'C NUEVE DE OCTUBRE 8 ACC - VALÈNCIA'
}, {
	...
}]
```


# cli

The repo also includes a python cli with a working example

```
$ python3 cli.py bus_times 508
Parada 508
	70 (Alboraia): 5 minutes left
	93 (Pass. Marítim): 13 minutes left
	70 (Alboraia): 22 minutes left
	93 (Pass. Marítim): 12:34
```

```
$ python3 cli.py stops_in_extent 39.471964 -0.394641 39.474714 -0.405906
Paradas en [ 39.471964 , -0.394641 ; 39.474714 , -0.405906 ] ->

	2070 - Nou d'Octubre (par) - Democràcia
		LatLon: 39.4720832588597, -0.40559318566979
		Lineas:
			73 - Tres Creus
			95 - Hospital General
			98 - Av. del cid
			99 - la Malva-rosa
	
	...
```















