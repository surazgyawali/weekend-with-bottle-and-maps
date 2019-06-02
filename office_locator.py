import json

import bottle
import petl

DATA_FILE = "./office_service_locations.csv"
SERVICES_FILE = "./Office_Services.csv"

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='views/static/')

@bottle.route("/")
def home():
    data_table =  petl.fromcsv(SERVICES_FILE)
    data = [("Business & Trade",1),("Life Events",2),("Legal Information & Services",3),("Employment & Jobs",4),("Health & Wellbeing",5)]
    print(data)
    return bottle.template('office_map',data=data)

@bottle.route("/getoffices")
def get_offices():
    serviceID = bottle.request.query.serviceid

    data_table = petl.fromcsv(DATA_FILE)

    if serviceID:
        data = petl.facet(data_table, 'ServiceID')[serviceID]
        data = [item[2:] for item in data]
        headers = data.pop(0)
        return json.dumps({
            "headers":headers,
            "data":data
        })

    return

bottle.run(host="0.0.0.0", port=8000, debug=True,reloader=True)
