#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ###############################################################################
# Copyright 2014 OCLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Example of retrieving a token with Client Credentials Grant

import urllib2
from authliboclc import wskey

#
# Authentication Parameters
#

key = '{clientID}'
secret = '{secret}'
authenticating_institution_id = '{institutionId}'
context_institution_id = '{institutionId}'

# Configure the wskey library object
my_wskey = wskey.Wskey(
    key=key,
    secret=secret,
    options={'services': ['WorldCatDiscoveryAPI']})

# Get an access token
access_token = my_wskey.get_access_token_with_client_credentials(
    authenticating_institution_id=authenticating_institution_id,
    context_institution_id=context_institution_id
)

# Describe the token received, or the error produced
print("")
if (access_token.access_token_string == None):
    if (key == '{clientID}'):
        print(
        "**** You must configure the key, secret, authenticating_institution_id and context_institution_id ****")
        print("")
    print("error_code:    " + `access_token.error_code`)
    print("error_message: " + access_token.error_message)
    print("error_url:     " + access_token.error_url)
else:
    print("access token:  " + access_token.access_token_string)
    print("expires_in:    " + `access_token.expires_in`)
    print("expires_at:    " + access_token.expires_at)
    print("type:          " + access_token.type)
    if (access_token.refresh_token != None):
        print("refresh_token: " + access_token.refresh_token)
print("")

# Make a DAPI Request - get a JSON Bib Record back for OCLC #52356689
if (access_token.access_token_string != None):
    request_url = 'https://beta.worldcat.org/discovery/bib/data/52356689'
    authorization = 'Bearer ' + access_token.access_token_string
    print("Making a request to " + request_url)
    print(authorization)

    my_request = urllib2.Request(
        url=request_url,
        data=None,
        headers={'Authorization': authorization, 'Accept': 'application/json'}
    )

    try:
        result = urllib2.urlopen(my_request).read()

    except urllib2.HTTPError, e:
        result = str(e)

    print(result)