# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
import argparse
import os
from dotenv import load_dotenv

#Instrument Analytics service credentials
if 'VCAP_SERVICES' in os.environ:
    vcap_servicesData = json.loads(os.environ['VCAP_SERVICES'])
    # Log the fact that we successfully found some service information.
    print("Got vcap_servicesData\n")
    # Look for the Simulated Instrument Analytics service instance
    access_token=vcap_servicesData['sia'][0]['credentials']['accessToken']
    uri=vcap_servicesData['sia'][0]['credentials']['uri']
    # Log the fact that we successfully found credentials
    print("Got SIA credentials\n")
else:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    uri=os.environ.get("SIA_uri")
    access_token=os.environ.get("SIA_access_token")


def simulate(instrument_ids, analytics=None):
    """
    Retreives the Simulated Instrument Analytics service data, pass the instrument_id
    """
    #print for logging purpose
    print ("Calling Simulated Instrument Analytics")
    
    if not analytics:
        analytics = ['Price','Value']

    payload = {
            "id-list":instrument_ids,
            "analytics":analytics,
        }
    payload = json.dumps(payload)

    #call the url
    BASEURL = uri + '/sia/v2/instrument/simulate' #needs to be adjusted!
    headers = {
        'Content-Type':'application/json',
        'x-ibm-algo-user-key': access_token
        }
    get_data = requests.post(BASEURL, headers=headers, data=payload)
    print("Simulated Instrument Analytics status: " + str(get_data.status_code))

    #return json data
    data = get_data.json()
    return data

