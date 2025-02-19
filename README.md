# vcoclient.py (version 0.1.9) 

A simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the Linux methodology and to have one VCO client that can be used within a complex workflow under Linux.

### Simple usage

```sh
[iddoc@homeserver:/scripts] pip3 install vcoclient
[iddoc@homeserver:/scripts] export VCO_TOKEN='....'
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get

                                                         Branch1                                   Branch2                                   Branch3                                   Branch4
activationKey                                HS7S-QKPA-ZZCC-PG74                       LHH3-8B4R-7XVJ-6J3V                       JTWH-EHNW-7LUG-YQ9T                       YZ8U-CKTY-8MTL-FP4R
activationKeyExpires                    2019-05-28T11:53:33.000Z                  2019-05-19T16:58:53.000Z                  2019-06-01T10:32:39.000Z                  2019-06-01T16:10:54.000Z
activationState                                        ACTIVATED                                 ACTIVATED                                 ACTIVATED                                 ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z                  2019-04-19T17:17:51.000Z                  2019-05-02T10:55:10.000Z                  2019-05-02T19:18:20.000Z
alertsEnabled                                                  1                                         1                                         1                                         1
buildNumber                                     R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA
created                                 2019-04-19T15:48:50.000Z                  2019-04-19T16:58:53.000Z                  2019-05-02T10:32:39.000Z                  2019-05-02T16:10:54.000Z
...                                     ...                                       ...                                       ...                                       ...
```

### Or authentication based:

```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 login --username=super@domain.com --password
Password: 
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get

                                                         Branch1                                   Branch2                                   Branch3                                   Branch4
activationKey                                HS7S-QKPA-ZZCC-PG74                       LHH3-8B4R-7XVJ-6J3V                       JTWH-EHNW-7LUG-YQ9T                       YZ8U-CKTY-8MTL-FP4R
activationKeyExpires                    2019-05-28T11:53:33.000Z                  2019-05-19T16:58:53.000Z                  2019-06-01T10:32:39.000Z                  2019-06-01T16:10:54.000Z
activationState                                        ACTIVATED                                 ACTIVATED                                 ACTIVATED                                 ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z                  2019-04-19T17:17:51.000Z                  2019-05-02T10:55:10.000Z                  2019-05-02T19:18:20.000Z
alertsEnabled                                                  1                                         1                                         1                                         1
buildNumber                                     R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA                          R322-20190212-GA
created                                 2019-04-19T15:48:50.000Z                  2019-04-19T16:58:53.000Z                  2019-05-02T10:32:39.000Z                  2019-05-02T16:10:54.000Z
...                                     ...                                       ...                                       ...                                       ...

[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 logout
```

It uses argparse and it is functional hooks. Each functional hook, is a mini method to accomplish something. 

## Status

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/vcoclient.svg'></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/vcoclient.svg'></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://travis-ci.org/iddocohen/vcoclient.svg?branch=master'></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/vcoclient.svg'></td>
    </tr>
    <tr>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/vcoclient.svg'></td>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/vcoclient.svg'></td>
    </tr>
</table>


## Installation

### Compatibility

The matrix below gives one the vcoclient version on which VCO release it was tested against.

For sanity reasons, only the current VCO release will be used for testing and hence vcoclient (and the workflow_examples) will be updated/maintained accordingly. The current VCO release will be market as **bold**.

**CAUTION:** Using a different version of vcoclient against different VCO release, might cause unwanted results and is not recommended.

All tests where performed on a Linux and/or MacOS operation systems. There is no reason why it should not work with Windows but you have been warned. 

<table>
    <tr>
        <td>VCO release</td>
        <td>Tested with vcoclient version</td>
    </tr>
    <tr>
        <td><b>,4.x,5.x,6.x</b></td>
        <td>0.1.9</td>
    </tr>
    <tr>
        <td><b>3.3.1-GA-20190819</b></td>
        <td>0.1.8</td>
    </tr>
    <tr>
        <td>3.3.0-GA-20190724</td>
        <td>0.1.7</td>
    </tr>
    <tr>
        <td>3.2.2-GA-20190606</td>
        <td>0.1.4 and earlier</td>
    </tr>
</table>

### Instructions

To install the latest version use:

``pip3 install vcoclient``

To install a particular version, e.g. version 0.1.4 use:

``pip3 install vcoclient==0.1.4``

## Useage

### Global Environment Variables

To influence program behaviour and avoiding using ``--``options, one can use global environment variables, for some of the options:

<table>
    <tr>
        <td>Name</td>
        <td>Example Usage</td>
        <td>Same as Using</td>
        <td>Default Value</td>
    </tr>
    <tr>
        <td>VCO_HOST</td>
        <td>export VCO_HOST="vco.domain.net"</td>
        <td>vcoclient.py --vco="vco.domain.net"</td>
        <td>None</td>
    </tr>
    <tr>
        <td>VCO_TOKEN (working only with 0.1.9+)</td>
        <td>export VCO_TOKEN="yourtoken here"</td>
        <td></td>
        <td>None</td>
    </tr>
    <tr>
        <td>VCO_USER</td>
        <td>export VCO_USER="my_username@domain.net"</td>
        <td>vcoclient.py login --username="my_username@domain.net"</td>
        <td>None</td>
    </tr>
    <tr>
        <td>VCO_PASS</td>
        <td>export VCO_PASS="MySuperSecretPassword"</td>
        <td>vcoclient.py login --password="MySuperSecretPassword"</td>
        <td>None</td>
    </tr>
    <tr>
        <td>VCO_COOKIE_PATH</td>
        <td>export VCO_COOKIE_PATH="/path/where/I/save/cookies/"</td>
        <td>None (yet)</td>
        <td>/tmp/</td>
    </tr>
    <tr>
        <td>VCO_VERIFY_SSL</td>
        <td>export VCO_VERIFY_SSL="TRUE"</td>
        <td>None (yet)</td>
        <td>False</td>
    </tr>

</table> 

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

One can also use a special os variable called VCO_HOST for ``--vco``, without the need to input the hostname all the time, e.g.:

```sh
[iddoc@homeserver:/scripts] export VCO_HOST="192.168.2.55"
[iddoc@homeserver:/scripts] vcoclient.py edges_get 
```

#### Example

Output to Shell with Pandas format

```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 --output=pandas edges_get --search=Branch1
activationKey                                HS7S-QKPA-ZZCC-PG74
activationKeyExpires                    2019-05-28T11:53:33.000Z
activationState                                        ACTIVATED
activationTime                          2019-04-28T11:55:38.000Z
...
```

Or in JSON

```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 --output=json edges_get --search=Branch1 | python -m json.tool
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

[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 --output=csv edges_get --search=Branch1
,activationKey,activationKeyExpires,activationState,activationTime,alertsEnabled,buildNumber,certificates,configuration.enterprise.id,configuration.enterprise.modules,configuration.enterprise.name,configuration.operator.id,configuration.operator.modules,configuration.operator.name,created,description,deviceFamily,deviceId,dnsName,edgeHardwareId,edgeState,edgeStateTime,endpointPkiMode,enterpriseId,factoryBuildNumber,factorySoftwareVersion,haLastContact,haPreviousState,haSerialNumber,haState,id,isLive,lastContact,links,logicalId,modelNumber,modified,name,operatorAlertsEnabled,recentLinks,selfMacAddress,serialNumber,serviceState,serviceUpSince,site.city,site.contactEmail,site.contactMobile,site.contactName,site.contactPhone,site.country,site.created,site.id,site.lat,site.locale,site.lon,site.modified,site.name,site.postalCode,site.shippingAddress,site.shippingAddress2,site.shippingCity,site.shippingContactName,site.shippingCountry,site.shippingPostalCode,site.shippingSameAsLocation,site.shippingState,site.state,site.streetAddress,site.streetAddress2,site.timezone,siteId,softwareUpdated,softwareVersion,systemUpSince
0,HS7S-QKPA-ZZCC-PG74,2019-05-28T11:53:33.000Z,ACTIVATED,2019-04-28T11:55:38.000Z,1,R322-20190212-GA,"[{'id': 5, 'created': '2019-04-28T11:55:39.000Z', 'csrId': 5, 'edgeId': 2, 'edgeSerialNumber': 'VMware-42372a8feed7928a-96a106d97231cc5b', 'enterpriseId': 1, 'certificate': '-----BEGIN CERTIFICATE-----\nMIIDtTCCAp2gAwIBAgIJAMqB79bHrnyJMA0GCSqGSIb3DQEBCwUAMDAxDDAKBgNV\nBAMTA3ZjbzEMMAoGA1UECxMDT1BTMRIwEAYDVQQKEwlWZWxvQ2xvdWQwHhcNMTkw\nNDI3MTE1NTM5WhcNMTkwNzI3MTE1NTM5WjCBoDEtMCsGA1UEAxMkY2RmMTNlNmUt\nMTNlMC00YTZlLTgwYTgtNmQxZmQ1NTE1ZGM4MS0wKwYDVQQKEyRlZTllY2ZiMi01\nNDQyLTRjYzgtOTQ0MC01NzVkM2Y3MzIyMzYxMTAvBgNVBAUTKFZNd2FyZS00MjM3\nMmE4ZmVlZDc5MjhhLTk2YTEwNmQ5NzIzMWNjNWIxDTALBgNVBAwTBGVkZ2UwggEi\nMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5qm7tr5NdW/Ei9LA1Pq5L5B5B\nA2909MAk3bmnQUD3SGxaPmsaZOlQ4RZea0xX9i/1YicX+iv19/Uch5O7Ogp4qlua\ndWP6h/36ye1dosGXe5iS61gQBvyc862o1thoJwDrRQrrA6ls0dUmwpZ23yX6Po7T\n/12M0liYVM2rbMv9Cjp3IPp02wrKPmrrkQGPoi9L7nJXtw/ejOhpxb+j++pwsAlk\nPFdt1cU2OB+LCrrhCxivmuOw+TcS9a+H3qNnZaLkTGC7S3sv93u3+Uq0c1dBiNoQ\nLMAxRUE5jErVgfWMsKJGnHKFwr9KaIEgJ9iXDoWei5G0+Y5UL1AMLlaLV8RJAgMB\nAAGjYTBfMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAdBgNVHQ4EFgQU\nSELl9l8JeqVuteTUNDQdY+kcEwUwHwYDVR0jBBgwFoAUYaTXIGB2WA2o/jiiwmoZ\n69ZxPQ4wDQYJKoZIhvcNAQELBQADggEBAKwii0EYuR9GSpysBFLW42h3piYUQexV\n3bGl4l7ASo7OdUtUZ0Of/xls3qqKcZDz7DmbFnFgsxkraFfNJflzj+vhaBHf4kcS\n/rZGCKyS840lndGkqIPM9Gu+oBX1RoblVA3hRQvqSugye8srEgmG6YsEPAtv5Fo4\npw079wMmkTb3rP1LslMT3Mcrc/7VnGkq/F5owwpueBF13XJfJhXZP2/eAQ4gDSF/\n1f4DLHJzDliSYDRN5C+jrWm3JVIu5vvJUIQSN3PAimZOgo5pjOridJvIdxRjCrlf\n4oFWVTQM5R0IQZTIbBwBHE0vkwHPbIV9RybYOm9aaT60NRSYLCqmboI=\n-----END CERTIFICATE-----\n', 'serialNumber': 'CA81EFD6C7AE7C89', 'subjectKeyId': '4842e5f65f097aa56eb5e4d434341d63e91c1305', 'fingerPrint': '780ac499e5e4f2968c9b35d03bdc70ef87069050', 'validFrom': '2019-04-27T11:55:39.000Z', 'validTo': '2019-07-27T11:55:39.000Z'}, {'id': 6, 'created': '2019-04-28T12:18:30.000Z', 'csrId': 6, 'edgeId': 2, 'edgeSerialNumber':.
...
```

### Login - Method 

One needs to authenticate himself/herself via username and password to VCO. A user can be type "operator" or "enterprise" and hence has different rights in VCO.

**Please note:** Session cookie is getting created as soon as this method gets called. The session cookie gets saved under ``/tmp/<hostname>.txt``, and used later by new method calls (so one does not need to use the login method everytime). As the cookie has no expire date and VCO holds the time on the expiry of the session, it is recommended **to execute login method every so often** to ensure nothing gets broken over time. 

Maybe to-do for the future, to store session time and check accordingly. 

```sh
[iddoc@homeserver:/scripts] vcoclient.py login --help
usage: vcoclient.py login [-h] --username USERNAME [--password PASSWORD]
                          [--no-operator]

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Username for Authentication
  --password [PASSWORD]
                        Password for Authentication
  --no-operator        Per default we login as operator to VCO. If not, use
                       this flag
```
#### Example

Either use the  unsecure method to provide a password:
```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 login --username=super@domain.com --password=VeloCloud123
[iddoc@homeserver:/scripts]
```
or use the more secure method to provide it:
```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 login --username=super@domain.com --password
Password:
[iddoc@homeserver:/scripts]
```
or use VCO_USER and/or VCO_PASS environment variables to pass no login information to the script itself:
```sh
[iddoc@homeserver:/scripts] export VCO_USER="super@domain.com"
[iddoc@homeserver:/scripts] export VCO_PASS="SuperSecretPassword"
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 login
[iddoc@homeserver:/scripts]
```

### Logout

The logout method logsout from VCO itself and deletes the session cookie stored under ``/tmp/<hostname>.txt``.

It is best practice to use it after done using different methods with vcoclient.py

#### Example

```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 logout
```

### Get edges

To get a list of all or filtered VeloCloud Edges (VCEs) from VCO. One can ``--search`` per value, get only one ``--name`` VCE and ``--filters``only given keys. Each of the methods (``--name``, ``--filters`` or ``--search``), one can use "|" to find for several values (e.g. to find several VCEs with names Branch1 or Branch2, use ``--name="Branch1|Branch2"). This gives one a powerful option to compare and evaluate several VCEs against each other and use those returned values for another workflow. 

``--enterpriseid`` can be used to find all specify VCEs from specific customer in VCO. For msp based users this is a must to use. 

**Please note:** ``--name``, ``--search`` and ``--filters``are all doing a loose search rather then an exact match, meaning you will get more values then maybe requested but you do not need to be very specific for your search. Maybe as a to-do, give different options in the future. 

```sh

usage: vcoclient.py edges_get [-h] [--name NAME] [--filters FILTERS]
                              [--search SEARCH] [--enterpriseid ID] [--rows_name]

optional arguments:
  -h, --help         show this help message and exit
  --name NAME        Search Edge/Edges containing the given name
  --filters FILTERS  Returns only given filters out of the returned value.
                     Default all values are returned
  --search SEARCH    Search any data from properties of Edges, e.g. search for
                     USB interfaces
  --enterpriseid ID            Returns the Edges of only that given enterprise. Default
                     all Edges of all enterprises at operator view or all
                     Edges of an enterprise at customer view are returned.
  --rows_name        Returns only the row names from the output result.

```

#### Example

To get all VCEs, with all values and keys, use default:

```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get
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
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get --name=Branch1
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
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get --name="Branch1|Branch-2"
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

[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55  edges_get --filters="activationKey|activationKeyExpires"

                                    Branch1-HA                  Branch-2                  Branch-3                  Branch-4
activationKey              HS7S-QKPA-ZZCC-PG74       LHH3-8B4R-7XVJ-6J3V       JTWH-EHNW-7LUG-YQ9T       YZ8U-CKTY-8MTL-FP4R
activationKeyExpires  2019-05-28T11:53:33.000Z  2019-05-19T16:58:53.000Z  2019-06-01T10:32:39.000Z  2019-06-01T16:10:54.000Z

```

or one can combine it with ``--name`` as well to filter it more specific:

```sh
[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55  edges_get --filters="activationKey|activationKeyExpires" --name="Branch1|Branch-2"
                                    Branch1-HA                  Branch-2
activationKey              HS7S-QKPA-ZZCC-PG74       LHH3-8B4R-7XVJ-6J3V
activationKeyExpires  2019-05-28T11:53:33.000Z  2019-05-19T16:58:53.000Z

```

Even more, one can search for any value within the VCE properties with ``--search``, let see what if we want to see all values:

```sh

[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get --search="*"
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

[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get --search="191.|10."

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

[iddoc@homeserver:/scripts] vcoclient.py --vco=192.168.2.55 edges_get --search="191.|10." --filters="ipAddress"
                    Branch1-HA     Branch-2     Branch-3 Branch-4
links_0_ipAddress  191.168.1.2  191.168.3.2  191.168.0.5      NaN
links_1_ipAddress  191.168.2.2  191.168.4.2          NaN      NaN
links_2_ipAddress          NaN     10.2.1.2          NaN      NaN
links_3_ipAddress          NaN     10.2.2.2          NaN      NaN

```

All those outputs can be then converted into CSV or JSON.

### Get Customers VCEs (as MSP or Operator) - Method

To get a list of all VCEs as a MSP/Partner or as operator one can use ``msp_customers_get`` or ``operator_customers_get``. Same as edges_get method, one can use ``--search``. ``--filters`` and ``--names`` to narrow down the result accordingly.


#### Example

The help output for ``msp_customers_get``:

```sh

[iddoc@homeserver:/scripts] vcoclient.py msp_customers_get --help
usage: vcoclient.py msp_customers_get [-h] [--name NAME] [--filters FILTERS]
                                      [--search SEARCH] [--rows_name]

optional arguments:
  -h, --help         show this help message and exit
  --name NAME        Search Enterprise/Enterprises containing the given name
  --filters FILTERS  Returns only given filters out of the returned value.
                     Default all values are returned
  --search SEARCH    Search any data from properties of customers, e.g. search
                     for particular edge
  --rows_name        Returns only the row names from the output result.

```

and the help output for ``òperator_custmers_get``:

```sh
[iddoc@homeserver:/scripts] vcoclient.py operator_customers_get --help
usage: vcoclient.py operator_customers_get [-h] [--name NAME]
                                           [--filters FILTERS]
                                           [--search SEARCH] [--rows_name]

optional arguments:
  -h, --help         show this help message and exit
  --name NAME        Search Enterprise/Enterprises containing the given name
  --filters FILTERS  Returns only given filters out of the returned value.
                     Default all values are returned
  --search SEARCH    Search any data from properties of customers, e.g. search
                     for particular edge
  --rows_name        Returns only the row names from the output result.
```

Here an example (customer names and account numbers obscured on purpose):

```sh
[iddoc@homeserver:/scripts] vcoclient.py msp_customers_get --search="*"
                                                                 POC                         Customer Test  ...                            Customer 5                           Customer 4
accountNumber                                            XXX-XXX-H86                           XXX-XXX-BKW  ...                           XXX-XXXDGL                           XXX-XXX-4EB
alertsEnabled                                                      1                                     1  ...                                     1                                     1
city                                                             NaN                                   NaN  ...                                   NaN                                   NaN
contactEmail                                                     NaN                                   NaN  ...                                   NaN                                   NaN
contactMobile                                                    NaN                                   NaN  ...                                   NaN                                   NaN
contactName                                                      NaN                                   NaN  ...                                   NaN                                   NaN
contactPhone                                                     NaN                                   NaN  ...                                   NaN                                   NaN
country                                                          NaN                                   NaN  ...                                   NaN                                   NaN
created                                     2017-10-09T13:47:29.000Z              2018-02-01T21:56:50.000Z  ...              2019-05-17T18:11:40.000Z              2019-06-20T15:52:27.000Z
description                                                      NaN                                   NaN  ...                                   NaN                                   NaN
domain                                                           NaN                                   NaN  ...                                   NaN                                   NaN
....
```
### Get edges behind gateway

This method will give one the ability to get all/some gateways behind a given customer

```sh
[iddoc@homeserver:/scripts] vcoclient.py enterprise_get_gateway --help
usage: vcoclient.py enterprise_get_gateway [-h] --enterpriseid ENTERPRISEID
                                           [--name NAME]
                                           [--filters FILTERS]
                                           [--search SEARCH] [--rows_name]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           Search for a given column name
  --enterpriseid ENTERPRISEID
                        Get gateways associated to an enterprise
  --filters FILTERS     Returns only given filters out of the returned value.
                        Default all values are returned
  --search SEARCH       Search any data from properties of customers, e.g.
                        search for particular edge
  --rows_name           Returns only the row names from the output result.

```

#### Example

Get the gateways associated to that enterprise:

```sh
[iddoc@homeserver:/scripts] vcoclient.py enterprise_get_gateway --enterpriseid=26

vcg115-xxx1    vcg101-xxx2   vcg133-xxx1   vcg104-xxx2
address  xxx.193.30.11  xxx.193.31.36  xxx.193.29.52  xxx.193.28.72
```

### Get gateways behind customer

This method will give one the ability to get all/some edges behind a given gateway

```sh
[iddoc@homeserver:/scripts] vcoclient.py gateway_get_edges --help
usage: vcoclient.py gateway_get_edges [-h] --gatewayid GATEWAYID [--name NAME]
                                      [--filters FILTERS] [--search SEARCH]
                                      [--rows_name]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           Search for a given column name
  --gatewayid GATEWAYID
                        Get edges associated to a gateway
  --filters FILTERS     Returns only given filters out of the returned value.
                        Default all values are returned
  --search SEARCH       Search any data from properties of customers, e.g.
                        search for particular edge
  --rows_name           Returns only the row names from the output result.
```

#### Example

Get all edges behind gateway (output hidden): 

```sh
[iddoc@homeserver:/scripts] vcoclient.py --gatewayid 5

                                          Alpharetta xxxxxxx                   Dallas xxxx
activationKey                            3WCR-xxxx-xxxx-xxxx                   3MQZ-xxx-xxxx-xxx
activationKeyExpires                2018-10-20T13:26:00.000Z              2018-04-06T02:11:14.000Z
activationState                         REACTIVATION_PENDING                             ACTIVATED
activationTime                      2018-05-25T00:02:08.000Z              2018-03-07T18:50:44.000Z
alertsEnabled                                              1                                     1
buildNumber                     R321-20181018-GA-27175-28009                      R320-20180409-GA
city                                                 Phoenix                                Dallas
country                                                   US                                    US
created                             2018-04-04T20:51:55.000Z              2018-03-07T02:11:14.000Z

```

### Get link metric of a given edge

One can get the link metric of a particular VCE for a given time.

```sh
[iddoc@homeserver:/scripts] vcoclient.py edge_get_lm --help
usage: vcoclient.py edge_get_lm [-h] [--filters FILTERS] [--search SEARCH]
                                --edgeid EDGEID [--enterpriseid ENTERPRISEID]
                                --starttime STARTTIME [--endtime ENDTIME]
                                [--rows_name]

Collect link statistics for a VCE between a given period.

optional arguments:
  -h, --help            show this help message and exit
  --filters FILTERS     Returns only given filters out of the returned value.
                        Default all values are returned
  --search SEARCH       Search for the metric value
  --edgeid EDGEID       Get information for that specific Edge. Edgeid can be
                        found under edges_get method under id.
  --enterpriseid ENTERPRISEID
                        Get information for that specific Edge in that
                        specific customer. EnterpriseId can be either found
                        from *_customers_get method under id or edges_get
                        method under enterpriseId.
  --starttime STARTTIME
                        The start time from when one wants to get the data.
                        Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM.
  --endtime ENDTIME     The end time from when one wants to get the data.
                        Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM. End time
                        is default to time now.
  --rows_name           Returns only the row names from the output result.

```

#### Example

Get the metric of all the links of a given edge from a given customer in the past until now:

```sh
[iddoc@homeserver:/scripts] vcoclient.py edge_get_lm --edgeid=1712 --enterpriseid=214 --starttime="2019-07-21"

                                                             GE3                                   GE4
bestJitterMsRx                                            0.0708                                 0.429
bestJitterMsTx                                            0.0007                                0.0677
bestLatencyMsRx                                           5.9113                                5.6578
bestLatencyMsTx                                           8.2916                                 9.771
bestLossPctRx                                            1.00436                              0.009067
bestLossPctTx                                           0.992402                              0.010039
bpsOfBestPathRx                                         10000000                               5000000
bpsOfBestPathTx                                         10000000                               5000000
bytesRx                                               6756806035                             942812687
bytesTx                                               5831454620                            1543851068
controlBytesRx                                        3161065177                             798578528
controlBytesTx                                        4174190874                            1477374932
controlPacketsRx                                        28229649                               7410590
controlPacketsTx                                        28763213                               9038440
....
link_networkType                                        ETHERNET                              ETHERNET
link_operatorAlertsEnabled                                     1                                     1
link_serviceState                                     IN_SERVICE                            IN_SERVICE
link_state                                                STABLE                                STABLE
link_vpnState                                             STABLE                                STABLE
p1BytesRx                                                9879820                              19802676
p1BytesTx                                               98164614                              40242590
p1PacketsRx                                                53984                                111780
p1PacketsTx                                               144023                                 86695
p2BytesRx                                             1342611884                             123590823
p2BytesTx                                              988377584                              25282998
p2PacketsRx                                              1806817                                510994
p2PacketsTx                                              2058099                                 57703
p3BytesRx                                             2243249154                                840660
p3BytesTx                                              570721548                                950548
p3PacketsRx                                             12891737                                  2738
p3PacketsTx                                              3279254                                  3994
packetsRx                                               42982187                               8036102
packetsTx                                               34244589                               9186832
scoreRx                                                  4.33582                               4.39847
scoreTx                                                  4.33613                               4.39684
signalStrength                                                 0                                     0
totalBytes                                           12588260655                            2486663755
totalPackets                                            77226776                              17222934
```

### Get link metric for the whole enterprise

One can get the link metrics of all VCEs of a given enterprise.

```sh
[iddoc@homeserver:/scripts] vcoclient.py edge_get_agg_lm --help
usage: vcoclient.py edges_get_agg_lm [-h] [--enterpriseid ENTERPRISEID]
                                     --starttime STARTTIME [--endtime ENDTIME]
                                     [--name NAME] [--filters FILTERS]
                                     [--search SEARCH] [--rows_name] [--stats]

Collect aggregated link statistics for several VCEs between a given period

optional arguments:
  -h, --help            show this help message and exit
  --enterpriseid ENTERPRISEID
                        Get information for that specific Edge in that
                        specific customer. EnterpriseId can be either found
                        from *_customers_get method under id or edges_get
                        method under enterpriseId.
  --starttime STARTTIME
                        The start time from when one wants to get the data.
                        Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM.
  --endtime ENDTIME     The end time from when one wants to get the data.
                        Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM.
  --name NAME           Search column which contains the given name
  --filters FILTERS     Returns only given filters out of the returned value.
                        Default all values are returned
  --search SEARCH       Search any value within the return, e.g. search for
                        USB interfaces
  --rows_name           Returns only the row names from the output result.
  --stats               Returns the statistics of the datastructure
```

#### Example

Get the metric of all the links of a given edge from a given customer in the past until now:

```sh
[iddoc@homeserver:/scripts] vcoclient.py edges_get_agg_lm --enterpriseid=214 --starttime="2019-10-04"
                                                          GE3                                   GE4  ...                                   GE4                                   GE4
bestJitterMsRx                                              0                                     0  ...                                     0                                     0
bestJitterMsTx                                              0                                     0  ...                                     1                                     0
bestLatencyMsRx                                            28                                    30  ...                                    14                                    13
bestLatencyMsTx                                            36                                    37  ...                                     9                                     5
bestLossPctRx                                               0                                     0  ...                                     0                                     0
bestLossPctTx                                               0                                     0  ...                                     0                                     0
bpsOfBestPathRx                                     200000000                             200000000  ...                              30114000                              98408000
bpsOfBestPathTx                                     200000000                             200000000  ...                               1392000                              10185000
bytesRx                                                813833                                144354  ...                                560482                                922079
bytesTx                                                901650                                171777  ...                                736663                                874260
controlBytesRx                                         683561                                144354  ...                                399858                                435730
controlBytesTx                                         820243                                171777  ...                                736663                                512154
controlPacketsRx                                         5906                                  2398  ...                                  5543                                  4928
controlPacketsTx                                         5747                                  2399  ...                                  5865                                  4752
linkId                                                   3163                                  3166  ...                                 37009                                 38690
...
```

### Set system properties

System properties of VCO can be changed/added. Only applicable at "operator" mode but needed for on-premiss installation of VCO.

**Please Note**: Some system properties can break VCO and use this method carefully.

```sh
[iddoc@homeserver:/scripts] vcoclient.py sysprop_set --help
usage: vcoclient.py sysprop_set [-h] --name NAME --value VALUE

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    Name of the new/edit system property
  --value VALUE  New value of the system property

```

#### Example

Enable google API for VCO:

```sh
[iddoc@homeserver:/scripts] vcoclient.py sysprop_set --name=service.client.googleMapsApi.enable --value=true
```

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
