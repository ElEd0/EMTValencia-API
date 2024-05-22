import pytest
import re
import emtvlcapi


def test_get_bus_times():
    response = emtvlcapi.get_bus_times(508)
    assert isinstance(response, list)
    assert len(response) > 0
    first = response[0]
    assert isinstance(first, dict)
    assert "linea" in first
    assert "destino" in first
    assert "minutos" in first or "horaLlegada" in first
    if "minutos" in first:
        assert re.compile("[0-9]+").match(str(first['minutos']))
    if "horaLlegada" in first:
        assert re.compile("\\d\\d:\\d\\d").match(first['horaLlegada'])


def test_get_stops_in_extent():
    response = emtvlcapi.get_stops_in_extent(39.471964, -0.394641, 39.474714, -0.405906)
    assert isinstance(response, list)
    assert len(response) > 0
    first = response[0]
    assert isinstance(first, dict)
    assert "lat" in first and "lon" in first
    assert "name" in first
    assert re.compile("\\d\\d\\.[0-9]+").match(str(first['lat']))
    assert re.compile("-\\d\\.[0-9]+").match(str(first['lon']))


