# vcoclient.py 

A simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the linux methodology and to have one VCO client that can be used within a complex workflow under Linux.

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 logout
True
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 login --username=super@velocloud.net --password=VeloCloud123
True
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

It uses argparse and it is functional hooks. Each functional hook, is a mini method to accomplish something. 

## Supported

On Mac OS and Linux

## Installation

TODO

## Useage
### Global Program Options

```sh
[iddoc@homeserver:/scripts] vcoclient.py --help
usage: vcoclient.py [-h] --vco HOSTNAME [--output {pandas,json}]
                    {login,logout,edges_get,sysprop_set} ...

A simple VeloCloud Orchestrator (VCO) client via Python

positional arguments:
  {login,logout,edges_get,sysprop_set}

optional arguments:
  -h, --help            show this help message and exit
  --vco HOSTNAME        Hostname/IP of VCO
  --output {pandas,json}
                        Pandas tables are used as default output method but
                        one can also use 'json'
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
....

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
True
```

### Logout - Method

The logout method logsout from VCO itself and deletes the session cookie stored under ``/tmp/<hostname>.txt``.

It is best practice to use it after done using different methods with vcoclient.py

#### Example

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 logout
True
```

### Get Edges - Method

To get a list of all or filtered VeloCloud Edges (VCEs) from VCO. 

```sh
usage: vcoclient.py edges_get [-h] [--search SEARCH]

optional arguments:
  -h, --help       show this help message and exit
  --search SEARCH  Search Edge/Edges containing the given name
```

#### Example

To get all, one does not need to ``--search`` parameter
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
but one can also search for one:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --search=Branch1
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

or even more then one: 

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 edges_get --search=Branch1\|Branch-2
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
True
```

## Release History

* 0.0.1
    * First versions

## Future improvements

* Finishing the TODOs in Python Client 

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
