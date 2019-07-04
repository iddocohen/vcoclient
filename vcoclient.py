#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Description:

This program is a simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the Linux methodology and to have a VCO client that can be used within a complex workflow under Linux. For example:

```sh
[iddoc@homeserver:/scripts] ./vcoclient.py --vco=192.168.2.55 login --username=super@domain.com --password
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
import ast
import time
import datetime

# Specific Libs
import pandas as pd
from pandas.io.json import json_normalize

# Specific imports
from requests.packages.urllib3.exceptions import InsecureRequestWarning

config_api_url = {
    "login"                  :    "",
    "logout"                 :    "",
    "operator_customers_get" :    "network/getNetworkEnterprises",
    "msp_customers_get"      :    "enterpriseProxy/getEnterpriseProxyEnterprises",
    "edge_get_lm"            :    "metrics/getEdgeLinkMetrics",
    "gateway_get_edges"      :    "gateway/getGatewayEdgeAssignments",
    "sysprop_set"            :    "systemProperty/insertOrUpdateSystemProperty",
    "edges_get"              :    "enterprise/getEnterpriseEdges",
    "default"                :    ""
}
config_api_param   = {
    "edges_get"              :    '{ "with":["certificates","configuration","links","recentLinks","site","vnfs","licences","cloudServices","cloudServiceSiteStatus"], "enterpriseId": %(id)i }',    
    "operator_customers_get" :    '{ "with":["edges"], "networkId": 1}',
    "msp_customers_get"      :    '{ "with":["edges"]}',
    "edge_get_lm"            :    '{ "edgeId": %(edgeid)i, "enterpriseId": %(enterpriseid)i, "interval": { "end": "%(endtime)s", "start": "%(starttime)s"}, "metrics": ["bytesRx", "bytesTx", "totalBytes", "totalPackets", "p1BytesRx", "p1BytesTx", "p1PacketsRx", "p1PacketsTx", "p2BytesRx", "p2BytesTx", "p2PacketsRx", "p2PacketsTx", "p3BytesRx", "p3BytesTx", "p3PacketsRx", "p3PacketsTx", "packetsRx", "packetsTx", "controlBytesRx", "controlBytesTx", "controlPacketsRx", "controlPacketsTx", "bestBwKbpsRx", "bestBwKbpsTx", "bestJitterMsRx", "bestJitterMsTx", "bestLatencyMsRx", "bestLatencyMsTx", "bestLossPctRx", "bestLossPctTx", "bpsOfBestPathRx", "bpsOfBestPathTx", "signalStrength", "scoreTx", "scoreRx"]}',
    "gateway_get_edges"      :    '{ "gatewayId": %{gatewayid}i }',
    "sysprop_set"            :    '{ "name": "%(name)s", "value": "%(value)s"}',
    "default"                :    None
}
config_api_call  = {
    "login"                  :    "authenticate", 
    "logout"                 :    "authenticate",
    "default"                :    "call_api"
}
config_out_mani  = {
    "login"                  :    None,
    "logout"                 :    None,
    "sysprop_set"            :    None,
    "default"                :    "format_by_name",
}



# TODO: Might want to have some logic to increase rows/columns
#pd.set_option('display.max_columns', 100)
#pd.set_option('display.max_rows', 100)

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

class ApiException(Exception):
    pass

class VcoRequestManager(object):

    #TODO: Give path outside here for the user to alter
    def __init__(self, hostname, verify_ssl=os.getenv('VCO_VERIFY_SSL', False), path=os.getenv('VCO_COOKIE_PATH', "/tmp/")):
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

    def authenticate(self, username="", password="", logout=False, is_operator=True, *args, **kwargs):
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

        if r.status_code == 200:
            if not logout:
                if "velocloud.message" in self._session.cookies:
                    if "Invalid" in self._session.cookies["velocloud.message"]:
                        raise ApiException(self._session.cookies["velocloud.message"].replace("%20", " "))

                if "velocloud.session" not in self._session.cookies:
                    raise ApiException("Cookie not received by server - something is very wrong")

                self._save_cookie()

            else:
                self._del_cookie()
        else:
            raise ApiException(r.text)
        
         
    def call_api(self, method=None, params=None, *args, **kwargs):
        """
        Build and submit a request
        Returns method result as a Python dictionary
        """
        if "velocloud.session" not in self._session.cookies: 
            if not self._load_cookie():
                raise ApiException("Cannot load session cookie") 

        if not method:
            raise ApiException("No Api Method defined")        

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


class VcoApiExecuteError(Exception):
   pass

class VcoApiExecute(object):
    """
    Executing dynmaic RestAPI calls based on the config_ dicts defined. 
    """
    def __init__(self, **args):
        if "dest" not in args:
            raise VcoApiExecuteError("Dest not defined in argparse object")        

        name        = args["dest"]
        self.url    = config_api_url.get(name, "")
        self.param  = self.__replace_placeholder(config_api_param.get(name, config_api_param["default"]), **args)
        self.call   = config_api_call.get(name, config_api_call["default"])
        self.out    = config_out_mani.get(name, config_out_mani["default"])
        self.client = VcoRequestManager(args["hostname"])
        self.p      = None

        self.__internal_call(**args)

    def __internal_call(self, **args):
        """
        Uses VcoRequestManager object and associated config_ dicts to execute the APIs.
        """
        try:
            if self.call:
                args["method"] = self.url
                args["params"] = self.param
                o = getattr(self.client, self.call)(**args)
                if self.out and o:
                    self.p = getattr(self, self.out)(o, **args)
        except Exception as e:
            if type(e).__name__ != "ApiException":
                raise VcoApiExecuteError(str(e))
            raise e

    def format_by_name(self, j, name=None, search=None, filters=None, output=None, rows=None, **args):
        """
        Converting JSON into Panda dataframe for filtering/searching given keys/values from that datastructure. 
        """
        df  = pd.DataFrame.from_dict(json_normalize(j, sep='_'), orient='columns')
        df.rename(index=df.name.to_dict(), inplace=True)

        if search:

          found = {}

          for k,v in self.__search_value(j, search):
            i, *_ = k.split("_")
            n = j[int(i)]["name"]
            k = k[len(i)+1:]
            found.setdefault(n,{})
            found[n].setdefault(k,{})
            found[n]["name"] = n 
            found[n][k] = v

          # TODO: Not sure what is more efficient, ...(found).T or ...from_dict(found, orient='index'). Fact is, from_dict does not preserve order, hence using .T for now.
          df = pd.DataFrame(found).T
          
        if name:
          df = df[df['name'].str.contains(name)]

        if filters:
          df = df[df.columns[df.columns.str.contains(filters)]]

        if "name" in df:
            df.drop("name", axis=1, inplace=True)

        df = df.T
        df.fillna(value=pd.np.nan, inplace=True)
        df.dropna(axis='columns', how='all', inplace=True)

        if rows:
            df = list(df.index)

        if output == "json":
          df = df.to_json()
        elif output == "csv":
          df = df.to_csv()
        
        return df


    @staticmethod 
    def __replace_placeholder (dic, **ph):
        """
        Searches and replaces a value under payload config. 
        """
        def string_sub(x):
            try:
                r = x % ph
                d = ast.literal_eval(r)
            except Exception as e:
                raise VcoApiExecuteError(str(e))
            
            if not isinstance(d, dict):
                raise VcoApiExecuteError("Payload is not type dict")
            return d 
        if dic is None:
            return {}
        return string_sub(dic)

    @staticmethod
    def __search_value(y, z):
        """
        Recrusively searches through dict to find given values seperated by |
        """
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
        return rsearch(y, z)

def valid_datetime_type(arg_datetime_str):
    """custom argparse type for user datetime values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            return datetime.datetime.strptime(arg_datetime_str, "%Y-%m-%d")
        except ValueError:
            msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-MM-DD HH:mm' or 'YYYY-MM-DD'!".format(arg_datetime_str)
            raise argparse.ArgumentTypeError(msg)  

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
    
    parser_login.add_argument("--no-operator", action="store_false", dest="is_operator", default=True,
                              help="Per default we login as operator to VCO. If not, use this flag")

    parser_login.set_defaults(dest="login")
    
    # Logout function
    parser_logout = subparsers.add_parser("logout")
    parser_logout.set_defaults(dest="logout")
    parser_logout.set_defaults(logout=True)


    # Get all Edges
    parser_getedges = subparsers.add_parser("edges_get", description="Get basic information for all/some VCEs.")
    
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

    parser_getedges.set_defaults(dest="edges_get")

    # Get link metric per Edge
    parser_getedgelm = subparsers.add_parser("edge_get_lm", description="Collect link statistics for a VCE between a given period.")
    
    parser_getedgelm.add_argument("--filters", action="store", type=str, dest="filters",
                              help="Returns only given filters out of the returned value. Default all values are returned")

    parser_getedgelm.add_argument("--search", action="store", type=str, dest="search", 
                              help="Search for the metric value")
    
    parser_getedgelm.add_argument("--edgeid", action="store", type=int, dest="edgeid", required=True,
                              help="Get information for that specific Edge. Edgeid can be found under edges_get method under id.")

    parser_getedgelm.add_argument("--enterpriseid", action="store", type=int, dest="enterpriseid", default=0,
                              help="Get information for that specific Edge in that specific customer. EnterpriseId can be either found from *_customers_get method under id or edges_get method under enterpriseId.")

    parser_getedgelm.add_argument("--starttime", action="store", type=valid_datetime_type, dest="starttime", required=True,
                              help="The start time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM.")
    
    parser_getedgelm.add_argument("--endtime", action="store", type=valid_datetime_type, dest="endtime", default=datetime.date.today(),
                              help="The end time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM. End time is default to time now.")

    parser_getedgelm.add_argument("--rows_name", action="store_true", dest="rows", default=False,
                              help="Returns only the row names from the output result.")

    parser_getedgelm.set_defaults(dest="edge_get_lm")


    # Get all Customers as operator
    parser_getcustomers_operator = subparsers.add_parser("operator_customers_get")
    
    parser_getcustomers_operator.add_argument("--name", action="store", type=str, dest="name", 
                              help="Search Enterprise/Enterprises containing the given name")
    
    parser_getcustomers_operator.add_argument("--filters", action="store", type=str, dest="filters",
                              help="Returns only given filters out of the returned value. Default all values are returned")
    
    parser_getcustomers_operator.add_argument("--search", action="store", type=str, dest="search", 
                              help="Search any data from properties of customers, e.g. search for particular edge")

    parser_getcustomers_operator.add_argument("--rows_name", action="store_true", dest="rows", default=False,
                              help="Returns only the row names from the output result.")

    parser_getcustomers_operator.set_defaults(dest="operator_customers_get")

    # Get all Customers as msp
    parser_getcustomers_msp = subparsers.add_parser("msp_customers_get")
    
    parser_getcustomers_msp.add_argument("--name", action="store", type=str, dest="name", 
                              help="Search Enterprise/Enterprises containing the given name")
    
    parser_getcustomers_msp.add_argument("--filters", action="store", type=str, dest="filters",
                              help="Returns only given filters out of the returned value. Default all values are returned")
    
    parser_getcustomers_msp.add_argument("--search", action="store", type=str, dest="search", 
                              help="Search any data from properties of customers, e.g. search for particular edge")

    parser_getcustomers_msp.add_argument("--rows_name", action="store_true", dest="rows", default=False,
                              help="Returns only the row names from the output result.")

    parser_getcustomers_msp.set_defaults(dest="msp_customers_get")


    # TODO: Think about supporting gateway_get_edges in the future
    #parser_getgatewayedges = subparsers.add_parser("gateway_get_edges")
    #parser_getgatewayedges.add_argument(
    #parser_getgatewayedges.set_defaults(dest="gateway_get_edges")

    # Update/insert system properties in VCO
    parser_sysprop_set = subparsers.add_parser("sysprop_set")
    
    parser_sysprop_set.add_argument("--name", action="store", type=str, dest="name", required=True, 
                              help="Name of the new/edit system property")

    parser_sysprop_set.add_argument("--value", action="store", type=str, dest="value", required=True, 
                              help="New value of the system property")
    
    parser_sysprop_set.set_defaults(dest="sysprop_set")
    
    args = parser.parse_args()

    if "dest" not in args:
        parser.print_help(sys.stderr)
    else:
        obj = VcoApiExecute(**vars(args))
        if obj.p is not None:
            print(obj.p)

