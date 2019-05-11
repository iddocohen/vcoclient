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

## Help

## Useage Example

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

<!-- Markdown link & img dfn's -->
[wiki]: https://github.com/iddocohen/vcoclient/wiki
