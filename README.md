# vcoclient.py 

A simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the linux methodology and to have one VCO client, to create complex workflows with existing linux shell programs.

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

It uses argparse and it is functional hooks. Each functional hook, is a mini workflow by itself. 

## Installation

## Useage
### Global Program Options
```sh
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
Output shall be in Pandas format
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

### Login 
```sh
usage: vcoclient.py login [-h] --username USERNAME [--password PASSWORD]
                          [--operator]

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Username for Authentication
  --password PASSWORD  Password for Authentication
  --operator           Per default we login as operator to VCO. If not, one
                       can set this to false.
```
### Logout
### Get Edges
### Set System Properties

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
