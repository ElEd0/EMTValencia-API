# EMTVLC-API  

Python module that retrieves bus times for a given stop and stops within an extent.

Data from EMT valencia.

# pip

Module is available at [PyPI](https://pypi.org/project/emtvlcapi/) and can be installed via pip:

```
pip install emtvlcapi
```

# Usage

All methods return a list containing the results

Get bus times for a given stop id and optionally a bus number:
```
import emtvlcapi

# get bus times for stop 508
response = emtvlcapi.get_bus_times(508)
print(response)

# get bus times for stop 508 and line 93
response = emtvlcapi.get_bus_times(508, 93)
print(response)
```
Output:
```
[{'linea': '70', 'destino': 'Alboraia', 'minutos': '13'}, 
{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '15'}, 
{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '29'}, 
{'linea': '70', 'destino': 'Alboraia', 'minutos': '31'}, 
{'linea': 'N4', 'destino': 'Est.del Nord', 'horaLlegada': '22:41'}, 
{'linea': 'N4', 'destino': 'Est.del Nord', 'horaLlegada': '23:32'}]


[{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '14'}, 
{'linea': '93', 'destino': 'Pass. Marítim', 'minutos': '28'}]

```

Get stops within the rectangle created by 2 lat-lon points in opposite corners:
```
import emtvlcapi

response = emtvlcapi.get_stops_in_extent(39.471964, -0.394641, 39.474714, -0.405906)
print(response)
```
Output:
```
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
$ python -m emtvlcapi bus_times 508
Parada 508
	70 (Alboraia): 5 minutes left
	93 (Pass. Marítim): 13 minutes left
	70 (Alboraia): 22 minutes left
	93 (Pass. Marítim): 12:34
```

```
$ python -m emtvlcapi stops_in_extent 39.471964 -0.394641 39.474714 -0.405906
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


