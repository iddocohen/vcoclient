# vcoclient.py 

A simple VeloCloud Orchestrator (VCO) Python client

The idea, with simple shell and with this simple client, create complex workflows with VCO.
The client uses barebone VCO API and python libaries to be slim as possible.

It uses argparse and functional hooks, to execute those. Each functional hook, has its help and one can use those to understand what is supported with client.

## How the synergy might work:
```sh
  ./vcoclient.py --vco=192.168.2.55 logout
  ./vcoclient.py --vco=192.168.2.55 login --username=super@velocloud.net --password=VeloCloud123
  ./vcoclient.py --vco=192.168.2.55 edges_get --search=VCE-Branch-1
  ./vcoclient.py --vco=192.168.2.55 edges_get
```

## Installation

## Useage
### Global Options
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
