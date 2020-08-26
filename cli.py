from emtvlc import EMTVLC
import json


response = EMTVLC().get_bus_times(508, 0)

print(response)


f = open('response.json', 'w')
f.write(json.dumps(response))
	
