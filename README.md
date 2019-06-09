# vcoclient.py 

A simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the Linux methodology and to have one VCO client that can be used within a complex workflow under Linux.

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 login --username=super@velocloud.net --password=VeloCloud123
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get

                                                         Branch1                                   Branch2                                   Branch3                                   Branch4
activationKey                                HS7S-QKPA-ZZCC-PG74                       LHH3-8B4R-7XVJ-6J3V                       JTWH-EHNW-7LUG-YQ9T                       YZ8U-CKTY-8MTL-FP4R
activationKeyExpires                    2019-05-28T11:53:33.000Z                  2019-05-19T16:58:53.000Z                  2019-06-01T10:32:39.000Z                  2019-06-01T16:10:54.000Z
activationState                                        ACTIVATED                                 ACTIVATED                                 ACTIVATED                                 ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z                  2019-04-19T17:17:51.000Z                  2019-05-02T10:55:10.000Z                  2019-05-02T19:18:20.000Z
alertsEnabled                                                  1                                         1                                         1                                         1
buildNumber                                     R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA
created                                 2019-04-19T15:48:50.000Z                  2019-04-19T16:58:53.000Z                  2019-05-02T10:32:39.000Z                  2019-05-02T16:10:54.000Z
...                                     ...                                       ...                                       ...                                       ...

[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 logout
```

It uses argparse and it is functional hooks. Each functional hook, is a mini method to accomplish something. 

## Supported

On Mac OS and Linux

## Installation

TODO

## Useage
### Global Program Options

```sh
[iddoc@homeserver:/scripts] vcoclient.py --help
usage: vcoclient.py [-h] --vco HOSTNAME [--output {pandas,json, csv}]
                    {login,logout,edges_get,sysprop_set} ...

A simple VeloCloud Orchestrator (VCO) client via Python

positional arguments:
  {login,logout,edges_get,sysprop_set}

optional arguments:
  -h, --help            show this help message and exit
  --vco HOSTNAME        Hostname/IP of VCO
  --output {pandas,json,csv}
                        Pandas tables are used as default output method but
                        one can also use 'json' or csv
```
#### Example

Output to Shell with Pandas format

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 --output=pandas edges_get --search=Branch1
activationKey                                HS7S-QKPA-ZZCC-PG74
activationKeyExpires                    2019-05-28T11:53:33.000Z
activationState                                        ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z
...
```

Or in JSON

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 --output=json edges_get --search=Branch1 | python -m json.tool
{
    "activationKey": {
        "0": "HS7S-QKPA-ZZCC-PG74"
    },
    "activationKeyExpires": {
        "0": "2019-05-28T11:53:33.000Z"
    },
    "activationState": {
        "0": "ACTIVATED"
    },
    "activationTime": {
        "0": "2019-04-28T11:55:38.000Z"
    },
...
```

or in CSV

```sh

[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 --output=csv edges_get --search=Branch1
,activationKey,activationKeyExpires,activationState,activationTime,alertsEnabled,buildNumber,certificates,configuration.enterprise.id,configuration.enterprise.modules,configuration.enterprise.name,configuration.operator.id,configuration.operator.modules,configuration.operator.name,created,description,deviceFamily,deviceId,dnsName,edgeHardwareId,edgeState,edgeStateTime,endpointPkiMode,enterpriseId,factoryBuildNumber,factorySoftwareVersion,haLastContact,haPreviousState,haSerialNumber,haState,id,isLive,lastContact,links,logicalId,modelNumber,modified,name,operatorAlertsEnabled,recentLinks,selfMacAddress,serialNumber,serviceState,serviceUpSince,site.city,site.contactEmail,site.contactMobile,site.contactName,site.contactPhone,site.country,site.created,site.id,site.lat,site.locale,site.lon,site.modified,site.name,site.postalCode,site.shippingAddress,site.shippingAddress2,site.shippingCity,site.shippingContactName,site.shippingCountry,site.shippingPostalCode,site.shippingSameAsLocation,site.shippingState,site.state,site.streetAddress,site.streetAddress2,site.timezone,siteId,softwareUpdated,softwareVersion,systemUpSince
0,HS7S-QKPA-ZZCC-PG74,2019-05-28T11:53:33.000Z,ACTIVATED,2019-04-28T11:55:38.000Z,1,R322-20190212-GA,"[{'id': 5, 'created': '2019-04-28T11:55:39.000Z', 'csrId': 5, 'edgeId': 2, 'edgeSerialNumber': 'VMware-42372a8feed7928a-96a106d97231cc5b', 'enterpriseId': 1, 'certificate': '-----BEGIN CERTIFICATE-----\nMIIDtTCCAp2gAwIBAgIJAMqB79bHrnyJMA0GCSqGSIb3DQEBCwUAMDAxDDAKBgNV\nBAMTA3ZjbzEMMAoGA1UECxMDT1BTMRIwEAYDVQQKEwlWZWxvQ2xvdWQwHhcNMTkw\nNDI3MTE1NTM5WhcNMTkwNzI3MTE1NTM5WjCBoDEtMCsGA1UEAxMkY2RmMTNlNmUt\nMTNlMC00YTZlLTgwYTgtNmQxZmQ1NTE1ZGM4MS0wKwYDVQQKEyRlZTllY2ZiMi01\nNDQyLTRjYzgtOTQ0MC01NzVkM2Y3MzIyMzYxMTAvBgNVBAUTKFZNd2FyZS00MjM3\nMmE4ZmVlZDc5MjhhLTk2YTEwNmQ5NzIzMWNjNWIxDTALBgNVBAwTBGVkZ2UwggEi\nMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5qm7tr5NdW/Ei9LA1Pq5L5B5B\nA2909MAk3bmnQUD3SGxaPmsaZOlQ4RZea0xX9i/1YicX+iv19/Uch5O7Ogp4qlua\ndWP6h/36ye1dosGXe5iS61gQBvyc862o1thoJwDrRQrrA6ls0dUmwpZ23yX6Po7T\n/12M0liYVM2rbMv9Cjp3IPp02wrKPmrrkQGPoi9L7nJXtw/ejOhpxb+j++pwsAlk\nPFdt1cU2OB+LCrrhCxivmuOw+TcS9a+H3qNnZaLkTGC7S3sv93u3+Uq0c1dBiNoQ\nLMAxRUE5jErVgfWMsKJGnHKFwr9KaIEgJ9iXDoWei5G0+Y5UL1AMLlaLV8RJAgMB\nAAGjYTBfMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAdBgNVHQ4EFgQU\nSELl9l8JeqVuteTUNDQdY+kcEwUwHwYDVR0jBBgwFoAUYaTXIGB2WA2o/jiiwmoZ\n69ZxPQ4wDQYJKoZIhvcNAQELBQADggEBAKwii0EYuR9GSpysBFLW42h3piYUQexV\n3bGl4l7ASo7OdUtUZ0Of/xls3qqKcZDz7DmbFnFgsxkraFfNJflzj+vhaBHf4kcS\n/rZGCKyS840lndGkqIPM9Gu+oBX1RoblVA3hRQvqSugye8srEgmG6YsEPAtv5Fo4\npw079wMmkTb3rP1LslMT3Mcrc/7VnGkq/F5owwpueBF13XJfJhXZP2/eAQ4gDSF/\n1f4DLHJzDliSYDRN5C+jrWm3JVIu5vvJUIQSN3PAimZOgo5pjOridJvIdxRjCrlf\n4oFWVTQM5R0IQZTIbBwBHE0vkwHPbIV9RybYOm9aaT60NRSYLCqmboI=\n-----END CERTIFICATE-----\n', 'serialNumber': 'CA81EFD6C7AE7C89', 'subjectKeyId': '4842e5f65f097aa56eb5e4d434341d63e91c1305', 'fingerPrint': '780ac499e5e4f2968c9b35d03bdc70ef87069050', 'validFrom': '2019-04-27T11:55:39.000Z', 'validTo': '2019-07-27T11:55:39.000Z'}, {'id': 6, 'created': '2019-04-28T12:18:30.000Z', 'csrId': 6, 'edgeId': 2, 'edgeSerialNumber':.
...
```

### Login - Method 

One needs to authenticate himself/herself via username and password to VCO. A user can be type "operator" or "enterprise" and hence has different rights in VCO.

**Please note:** Session cookie is getting created as soon as this method gets called. The session cookie gets saved under ``/tmp/<hostname>.txt``, and used later by new method calls (so one does not need to use the login method everytime). As the cookie has no expire date and VCO holds the time on the expiry of the session, it is recommended **to execute login method every so often** to ensure nothing gets broken over time. 

Maybe to-do for the future, to store session time and check accordingly. 

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py login --help
usage: vcoclient.py login [-h] --username USERNAME [--password PASSWORD]
                          [--no-operator]

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Username for Authentication
  --password PASSWORD  Password for Authentication
  --no-operator        Per default we login as operator to VCO. If not, use
                       this flag
```
#### Example

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 login --username=super@velocloud.net --password=VeloCloud123
```

### Logout - Method

The logout method logsout from VCO itself and deletes the session cookie stored under ``/tmp/<hostname>.txt``.

It is best practice to use it after done using different methods with vcoclient.py

#### Example

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 logout
```

### Get Edges - Method

To get a list of all or filtered VeloCloud Edges (VCEs) from VCO. One can ``--search`` per value, get only one ``--name`` VCE and ``--filters``only given keys. Each of the methods (``--name``, ``--filters`` or ``--name``), one can use "|" to search for several values (e.g. search for VCE with name Branch1 or Branch2, one can use ``--name="Branch1|Branch2"). This gives one a powerful option to compare and evaluate several VCEs against each other and use those returned values for another workflow. 

``--id`` can be used to specify VCEs from specific customer in VCO.

**Please note:** ``--name``, ``--search`` and ``--filters``are all doing a loose search rather then an exact match, meaning you will get more values then maybe requested but you do not need to be very specific for your search. 

```sh

usage: vcoclient.py edges_get [-h] [--search SEARCH] [--name NAME]
                              [--filters FILTERS] [--id ID]

optional arguments:
  -h, --help         show this help message and exit
  --search SEARCH    Search any data from properties of Edges, e.g. search for
                     USB interfaces
  --name NAME        Search Edge/Edges containing the given name
  --filters FILTERS  Returns only given filters out of the returned value.
                     Default all values are returned
  --id ID            Returns the Edges of only that given enterprise. Default
                     all Edges of all enterprises at operator view or all
                     Edges of an enterprise at customer view are returned.

```

#### Example

To get all VCEs, with all values and keys, use default:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get
                                                               0                                         1                                         2                                         3
activationKey                                HS7S-QKPA-ZZCC-PG74                       LHH3-8B4R-7XVJ-6J3V                       JTWH-EHNW-7LUG-YQ9T                       YZ8U-CKTY-8MTL-FP4R
activationKeyExpires                    2019-05-28T11:53:33.000Z                  2019-05-19T16:58:53.000Z                  2019-06-01T10:32:39.000Z                  2019-06-01T16:10:54.000Z
activationState                                        ACTIVATED                                 ACTIVATED                                 ACTIVATED                                 ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z                  2019-04-19T17:17:51.000Z                  2019-05-02T10:55:10.000Z                  2019-05-02T19:18:20.000Z
alertsEnabled                                                  1                                         1                                         1                                         1
buildNumber                                     R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA
created                                 2019-04-19T15:48:50.000Z                  2019-04-19T16:58:53.000Z                  2019-05-02T10:32:39.000Z                  2019-05-02T16:10:54.000Z
...                                     ...                                       ...                                       ...                                       ...
```
or use ``--name`` to filter one branch:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --name=Branch1
                                                               0
activationKey                                HS7S-QKPA-ZZCC-PG74
activationKeyExpires                    2019-05-28T11:53:33.000Z
activationState                                        ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z
alertsEnabled                                                  1
buildNumber                                     R322-20190212-GA
created                                 2019-04-19T15:48:50.000Z
...                                     ...
```

or several: 

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --name="Branch1|Branch-2"
                                                               0                                         1
activationKey                                HS7S-QKPA-ZZCC-PG74                       LHH3-8B4R-7XVJ-6J3V
activationKeyExpires                    2019-05-28T11:53:33.000Z                  2019-05-19T16:58:53.000Z
activationState                                        ACTIVATED                                 ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z                  2019-04-19T17:17:51.000Z
alertsEnabled                                                  1                                         1
buildNumber                                     R322-20190212-GA                          R322-20190212-GA
created                                 2019-04-19T15:48:50.000Z                  2019-04-19T16:58:53.000Z
...                                     ...                                       ...
```
Another option is to filter a specific value out of the return with ``--filters`` option, e.g. if one wants to filter activationKey and activationKeyExpires for all or some Edges:

```sh

[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55  edges_get --filters="activationKey|activationKeyExpires"

                                    Branch1-HA                  Branch-2                  Branch-3                  Branch-4
activationKey              HS7S-QKPA-ZZCC-PG74       LHH3-8B4R-7XVJ-6J3V       JTWH-EHNW-7LUG-YQ9T       YZ8U-CKTY-8MTL-FP4R
activationKeyExpires  2019-05-28T11:53:33.000Z  2019-05-19T16:58:53.000Z  2019-06-01T10:32:39.000Z  2019-06-01T16:10:54.000Z

```

or one can combine it with ``--name`` as well to filter it more specific:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55  edges_get --filters="activationKey|activationKeyExpires" --name="Branch1|Branch-2"
                                    Branch1-HA                  Branch-2
activationKey              HS7S-QKPA-ZZCC-PG74       LHH3-8B4R-7XVJ-6J3V
activationKeyExpires  2019-05-28T11:53:33.000Z  2019-05-19T16:58:53.000Z

```

Even more, one can search for any value within the VCE properties with ``--search``, let see what if we want to see all values:

```sh

[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --search="*"
                                                                        Branch1-HA  ...                                           Branch-4
...
certificates_0_certificate       -----BEGIN CERTIFICATE-----\nMIIDtTCCAp2gAwIBA...  ...  -----BEGIN CERTIFICATE-----\nMIIDtTCCAp2gAwIBA...
certificates_0_created                                    2019-04-28T11:55:39.000Z  ...                           2019-05-14T18:00:10.000Z
certificates_0_csrId                                                             5  ...                                                  8
certificates_0_edgeId                                                            2  ...                                                  5
certificates_0_edgeSerialNumber           VMware-42372a8feed7928a-96a106d97231cc5b  ...           VMware-4237c421fc52ed55-3ed39a20fbc24354
certificates_0_enterpriseId                                                      1  ...                                                  1
certificates_0_fingerPrint                780ac499e5e4f2968c9b35d03bdc70ef87069050  ...           af32143b2fee7e2bfca62ab0042244d7cb7f7e5e
certificates_0_id                                                                5  ...                                                  8
certificates_0_serialNumber                                       CA81EFD6C7AE7C89  ...                                   D4C2500333FE1757
...

```


In the background ``--search`` flattens the returned JSON and returns all values when ``*`` used. One can however, search for specific values as well, e.g. lets search for interface properties with 191. or 10. IPs:

```sh

[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --search="191.|10."

                                                     Branch1-HA     Branch-2                  Branch-3                  Branch-4
....
configuration_enterprise_modules_0_edgeSpecific...  191.168.1.2  191.168.3.2                       NaN                       NaN
configuration_enterprise_modules_0_edgeSpecific...  191.168.1.1  191.168.3.1                       NaN                       NaN
configuration_enterprise_modules_0_edgeSpecific...  191.168.2.2  191.168.4.2                  10.0.3.2                       NaN
configuration_enterprise_modules_0_edgeSpecific...  191.168.2.1  191.168.4.1                  10.0.3.1                       NaN
configuration_enterprise_modules_0_edgeSpecific...          NaN     10.2.1.2                       NaN                       NaN
configuration_enterprise_modules_0_edgeSpecific...          NaN     10.2.1.1                       NaN                       NaN
configuration_enterprise_modules_0_edgeSpecific...          NaN     10.2.2.2                       NaN                       NaN
configuration_enterprise_modules_0_edgeSpecific...          NaN     10.2.2.1                       NaN                       NaN
configuration_enterprise_modules_1_edgeSpecific...          NaN  191.168.0.3                10.0.254.2                       NaN
configuration_enterprise_modules_1_edgeSpecific...          NaN   10.0.254.2                       NaN                       NaN
links_0_displayName                                 191.168.1.2  191.168.3.2               191.168.0.5                       NaN
links_0_ipAddress                                   191.168.1.2  191.168.3.2               191.168.0.5                       NaN
links_1_displayName                                 191.168.2.2  191.168.4.2                       NaN                       NaN
links_1_ipAddress                                   191.168.2.2  191.168.4.2                       NaN                       NaN
links_2_ipAddress                                           NaN     10.2.1.2                       NaN                       NaN
links_3_ipAddress                                           NaN     10.2.2.2                       NaN                       NaN
...
```

and filter the 'ipAddress' column only for all VCEs (Branch1-HA, Branch-2, Branch-3 or Branch-4):

```sh

[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --search="191.|10." --filters="ipAddress"
                    Branch1-HA     Branch-2     Branch-3 Branch-4
links_0_ipAddress  191.168.1.2  191.168.3.2  191.168.0.5      NaN
links_1_ipAddress  191.168.2.2  191.168.4.2          NaN      NaN
links_2_ipAddress          NaN     10.2.1.2          NaN      NaN
links_3_ipAddress          NaN     10.2.2.2          NaN      NaN

```

All those outputs can be then converted into CSV or JSON.
 
### Set System Properties - Method

System properties of VCO can be changed/added. Only applicable at "operator" mode but needed for on-premiss installation of VCO.

**Please Note**: Some system properties can break VCO and use this method carefully.

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py sysprop_set --help
usage: vcoclient.py sysprop_set [-h] --name NAME --value VALUE

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    Name of the new/edit system property
  --value VALUE  New value of the system property

```

#### Example

Enable google API for VCO:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py sysprop_set --name=service.client.googleMapsApi.enable --value=true
```

## Changelog

All notable changes to this project will be documented in this file.

### [0.0.4] - 2019-06
#### Added:
- ``--search`` in edges_get for searching any value related to edges properties. Gives one a powerful method to extract/compare values between many edges.
#### Changed:
- Method login and logout will not return True anymore but will just execute as is and will raise an exception otherwise.
        
### [0.0.3] - 2019-05 
#### Added:
- Output of Pandas, JSON or CSV, will have the name of the Edge rather as a returned index. Simpler to read.
- ``--filters`` lets user to filter output more granular
- User can now define another enterprise ID rather then the default 1 
#### Changed:
- ``--search`` changed to ``--name``in edges_get, reflecting really what is filtered

### [0.0.2] - 2019-05
#### Added:
- README, Licences, and fixes bugs in vcoclient.py
### [0.0.1] - 2019-05
- First versions

## Future improvements

* Finishing the TODOs in client
* Add more useful functions:
    * Partner gateway provisioning method
    * Edge provisioning method

## Contributing

1. Fork it (<https://github.com/iddocohen/vcoclient/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Licence
MIT, see ``LICENSE``

<!-- Markdown link & img dfn's -->
[wiki]: https://github.com/iddocohen/vcoclient/wiki
