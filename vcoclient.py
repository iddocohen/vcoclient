#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Description:

This program is a simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the Linux methodology and to have a VCO client that can be used within a complex workflow under Linux. For example:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 login --username=super@velocloud.net --password
Password:
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

Under https://github.com/iddocohen/vcoclient one can read methods implemented.

"""


# Generic Libs
import requests
import pickle
import json
import re 
import argparse
import os
import sys
import getpass

# Specific Libs
import pandas as pd
from pandas.io.json import json_normalize

# Specific imports
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Global Variables
VERIFY_SSL=False

# TODO: Might want to have some logic to increase rows/columns
#pd.set_option('display.max_columns', 100)
#pd.set_option('display.max_rows', 100)

__author__ = "Iddo Cohen"
__copyright__ = "Copyright 2019"
__credits__ = "Iddo Cohen"
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ ="Iddo Cohen"
__email__ = "iddocohen@gmail.com"
__status__ = "Dev"

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

class ApiException(Exception):
    pass

class VcoRequestManager(object):

    #TODO: Give path outside here for the user to alter
    def __init__(self, hostname, verify_ssl=VERIFY_SSL, path="/tmp/"):
        """
        Init the Class
        """
        if not hostname:
            raise ApiException("Hostname not defined")
        self._session = requests.Session()
        self._verify_ssl = verify_ssl
        if self._verify_ssl == False:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self._root_url = self._get_root_url(hostname)
        self._portal_url = self._root_url + "/portal/"
        self._livepull_url = self._root_url + "/livepull/liveData/"
        self._store_cookie = path + hostname + ".txt"
        self._seqno = 0

    def _get_root_url(self, hostname):
        """
        Translate VCO hostname to a root url for API calls 
        """
        if hostname.startswith("http"):
            re.sub('http(s)?://', '', hostname)
        proto = "https://"
        return proto + hostname

    def authenticate(self, username="", password="", logout=False, is_operator=True):
        """
        Authenticate to API - on success, a cookie is stored in the session and file
        """
        if not logout:
          path = "/login/operatorLogin" if is_operator else "/login/enterpriseLogin"
          data = { "username": username, "password": password }
        else:
          path = "/logout"
          data = {}

        url = self._root_url + path
        headers = { "Content-Type": "application/json" }
        r = self._session.post(url, headers=headers, data=json.dumps(data),
                               allow_redirects=True, verify=self._verify_ssl)

        # TODO: Different status for "missing" string in cookie
        #if r.status_code == 200 and "missing" not in self._session.cookies["velocloud.session"] and self._save_cookie():
        if r.status_code == 200:
            if not logout:
                self._save_cookie()
            else:
                self._del_cookie()
        else:
            raise ApiException(response_dict["error"]["message"])
        
         
    def call_api(self, method, params):
        """
        Build and submit a request
        Returns method result as a Python dictionary
        """
        if "velocloud.session" not in self._session.cookies: 
            if not self._load_cookie():
                raise ApiException("Cannot load session cookie") 
        
        self._seqno += 1
        headers = { "Content-Type": "application/json" }
        method = self._clean_method_name(method)
        payload = { "jsonrpc": "2.0",
                    "id": self._seqno,
                    "method": method,
                    "params": params }

        if method in ("liveMode/readLiveData", "liveMode/requestLiveActions", "liveMode/clientExitLiveMode"):
            url = self._livepull_url
        else:
            url = self._portal_url

        r = self._session.post(url, headers=headers,
                               data=json.dumps(payload), verify=self._verify_ssl)

        response_dict = r.json()
        if "error" in response_dict:
            raise ApiException(response_dict["error"]["message"])
        return response_dict["result"]

    def _clean_method_name(self, raw_name):
        """
        Ensure method name is properly formatted prior to initiating request
        """
        return raw_name.strip("/")
    
    def _save_cookie(self):
        """
        Save cookie from VCO
        """
        with open(self._store_cookie, "wb") as f:
            try:
                pickle.dump(self._session.cookies, f)
            except Exception as e:
                raise ApiException(str(e)) 	

    def _load_cookie(self):
        """
        Load VCO session cookie
        """
        if not os.path.isfile(self._store_cookie):
            return False
        
        with open(self._store_cookie, "rb") as f:
            try:
               self._session.cookies.update(pickle.load(f))
               return True
            except Exception as e:
               raise ApiException(str(e)) 	

    def _del_cookie(self):
        """
        Delete VCO session cookie
        """
        try: 
           os.remove(self._store_cookie)
           return True
        except Exception as e:
           raise ApiException(str(e))


def rsearch(x, s, p=''):
    if isinstance(x, dict):
        for _ in x:
            yield from rsearch(x[_], s, p + _ + "_")
    elif isinstance(x, list):
        i = 0
        for _ in x:
            yield from rsearch(_, s, p + str(i) + "_")
            i += 1
    elif s != "*":
        for _ in s.split("|"):
            if _.upper() in str(x).upper():
                yield p[:-1], x
    else:
        yield p[:-1], x


def format_print(j, name=None, search=None, filters=None, output=None, rows=None, **args):
    df  = pd.DataFrame.from_dict(json_normalize(j, sep='_'), orient='columns')
    # TODO: Removing the shalow rename warning received by Pandas. Need to investigate why I get such a warning.
    pd.options.mode.chained_assignment = None

    df.rename(index=df.name.to_dict(), inplace=True)

    # Searches through JSON to find any value in search and converts it to pandas 
    if search:

      found = {}

      for k,v in rsearch(j, search):
        i, *_ = k.split("_")
        n = j[int(i)]["name"]
        k = k[len(i)+1:]
        found.setdefault(n,{})
        found[n].setdefault(k,{})
        found[n]["name"] = n 
        found[n][k] = v

      # TODO: Not sure what is more efficient, ...(found).T or ...from_dict(found, orient='index'). Fact is, from_dict does not preserve order, hence using .T for now.
      df = pd.DataFrame(found).T
      df.fillna(value=pd.np.nan, inplace=True)
      
    if name:
      df = df[df['name'].str.contains(name)]

    if filters:
      df = df[df.columns[df.columns.str.contains(filters)]]

    if "name" in df:
        df.drop("name", axis=1, inplace=True)

    df = df.T

    if rows:
        df = list(df.index)

    if output == "json":
      df = df.to_json()
    elif output == "csv":
      df = df.to_csv()
    

    pd.options.mode.chained_assignment = 'warn'
    
    return df


def logout(args):
    """
    Logout from VCO
    """ 
    client = VcoRequestManager(args.hostname)
    client.authenticate(logout=True) 
    

def login (args):
    """
    Login at VCO
    """
    client = VcoRequestManager(args.hostname)
    client.authenticate(args.username, args.password, is_operator=args.operator)

def customers_get (args):
    """
    Gets customers from VCO.
    """
    client = VcoRequestManager(args.hostname)
    o = client.call_api("network/getNetworkEnterprises", { "with":["edges", "edgeCount", "edgeConfigUpdate"], "networkId": 1})
    j = json.loads(json.dumps(o))

    out = format_print(j, **vars(args))

    print(out)
    
   
def edges_get (args):  
    """
    Gets edges from VCO.  
    """
    client = VcoRequestManager(args.hostname)
    o = client.call_api("enterprise/getEnterpriseEdges", { "with":["certificates","configuration","links","recentLinks","site","vnfs","licences","cloudServices","cloudServiceSiteStatus"], "enterpriseId": args.id })
    j = json.loads(json.dumps(o))

    out = format_print(j, **vars(args)) 

    print(out)

def sysprop_set (args):
    """
    Set system properties 
    """
    #TODO: There must be a better way but Namespace object does not have .copy() or .remove() 
    payload = {}
    for k in vars(args):
      payload[k] = getattr(args, k)
    
    del payload["func"]
    del payload["hostname"]
    del payload["output"]

    client = VcoRequestManager(args.hostname)
    o = client.call_api("systemProperty/insertOrUpdateSystemProperty", payload)
    if "rows" in o:
      print("Done")
    

if __name__ == "__main__":
    """
    Based on the arguements provided, it will execute a given function
    """
    parser = argparse.ArgumentParser(description="A simple VeloCloud Orchestrator (VCO) client via Python")
    parser.add_argument("--vco", action="store", type=str, dest="hostname", default=os.getenv('VCO_HOST', None),
                        help="Hostname/IP of VCO")
    parser.add_argument("--output", action="store", type=str, dest="output", default="pandas", choices=["pandas", "json", "csv"],
                        help="Pandas tables are used as default output method but one can also use 'json' or 'csv'")

    
    subparsers = parser.add_subparsers()

    # Login function
    parser_login = subparsers.add_parser("login")
    parser_login.add_argument("--username", action="store", type=str, dest="username", default=os.getenv('VCO_USER', None),
                              help="Username for Authentication")

    parser_login.add_argument("--password", action=Password, type=str, dest="password", nargs='?', default=os.getenv('VCO_PASS', ""),
                              help="Password for Authentication")
    
    parser_login.add_argument("--no-operator", action="store_false", dest="operator", default=True,
                              help="Per default we login as operator to VCO. If not, use this flag")

    parser_login.set_defaults(func=login)
    
    # Logout function
    parser_logout = subparsers.add_parser("logout")
    parser_logout.set_defaults(func=logout)


    # Get all Edges
    parser_getedges = subparsers.add_parser("edges_get")
    
    parser_getedges.add_argument("--name", action="store", type=str, dest="name", 
                              help="Search Edge/Edges containing the given name")
    
    parser_getedges.add_argument("--filters", action="store", type=str, dest="filters",
                              help="Returns only given filters out of the returned value. Default all values are returned")

    parser_getedges.add_argument("--search", action="store", type=str, dest="search", 
                              help="Search any data from properties of Edges, e.g. search for USB interfaces")
    
    parser_getedges.add_argument("--id", action="store", type=int, dest="id", default=1,
                              help="Returns the Edges of only that given enterprise. Default all Edges of all enterprises at operator view or all Edges of an enterprise at customer view are returned.")

    parser_getedges.add_argument("--rows_name", action="store_true", dest="rows", default=False,
                              help="Returns only the row names from the output result.")

    parser_getedges.set_defaults(func=edges_get)

    # Get all Customers
    parser_getcustomers = subparsers.add_parser("customers_get")
    
    parser_getcustomers.add_argument("--name", action="store", type=str, dest="name", 
                              help="Search Enterprise/Enterprises containing the given name")
    
    parser_getcustomers.add_argument("--filters", action="store", type=str, dest="filters",
                              help="Returns only given filters out of the returned value. Default all values are returned")
    

    parser_getcustomers.set_defaults(func=customers_get)


    # Update/insert system properties in VCO
    parser_sysprop_set = subparsers.add_parser("sysprop_set")
    
    parser_sysprop_set.add_argument("--name", action="store", type=str, dest="name", required=True, 
                              help="Name of the new/edit system property")

    parser_sysprop_set.add_argument("--value", action="store", type=str, dest="value", required=True, 
                              help="New value of the system property")
    
    parser_sysprop_set.set_defaults(func=sysprop_set)
    
    args = parser.parse_args()
    args.func(args)

