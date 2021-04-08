#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Description:
This program is a simple VeloCloud Orchestrator (VCO) Python client

The idea is to embrace the Linux methodology and to have a VCO client that can be used within a complex workflow under Linux.

For more visit: https://github.com/iddocohen/vcoclient
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
import numpy as np
from pandas import json_normalize

# Specific imports
from requests.packages.urllib3.exceptions import InsecureRequestWarning


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

    def login(self, **kwargs):
        self.authenticate(**kwargs)

    def logout(self, **kwargs):
        self.authenticate(logout=True, **kwargs)

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

        #print(payload)
        if method in ("liveMode/readLiveData", "liveMode/requestLiveActions", "liveMode/clientExitLiveMode"):
            url = self._livepull_url
        else:
            url = self._portal_url

        r = self._session.post(url, headers=headers,
                               data=json.dumps(payload), verify=self._verify_ssl)

        response_dict = r.json()
        #print(response_dict)
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
    Executing dynmaic RestAPI calls based on the config dicts defined. 
    """
    def __init__(self, **args):
        if "dest" not in args:
            raise VcoApiExecuteError("Dest not defined in argparse object")        
        name        = args["dest"]
        self.url    = config[name]["url"]
        self.param  = self.__replace_placeholder(config[name]["param"], **args)
        self.call   = config[name]["call"]
        self.out    = config[name]["mani"]
        self.client = VcoRequestManager(args["hostname"])
        self.p      = None

        self.__internal_call(**args)

    def __internal_call(self, **args):
        """
        Uses VcoRequestManager object and associated config dicts to execute the APIs.
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

    def format_by_name(self, j, name=None, search=None, filters=None, output=None, rows=None, stats=None, **args):
        """
        Converting JSON into Panda dataframe for filtering/searching given keys/values from that datastructure. 
        """
        df  = pd.DataFrame.from_dict(json_normalize(j, sep='_'), orient='columns')
        # some return value does not have "name" field
        if hasattr(df, "name"):
            df.rename(index=df.name.to_dict(), inplace=True)

        found = 1 
        if search:
            expand = {}
            for k,v in self.__search_value(j, search):
                i, *_ = k.split("_")
                n = j[int(i)]["name"]
                k = k[len(i)+1:]
                expand.setdefault(n,{})
                expand[n].setdefault(k,{})
                expand[n]["name"] = n 
                expand[n][k] = v

          # TODO: Not sure what is more efficient, ...(found).T or ...from_dict(found, orient='index'). Fact is, from_dict does not preserve order, hence using .T for now.
            found = bool(expand)
            df = pd.DataFrame(expand).T
          
        if name and found:
            df = df[df['name'].str.contains(name)]

        if filters and found:
            df = df[df.columns[df.columns.str.contains(filters)]]

        if stats and found:
            #df = df.describe(include='all')
            df = df.describe()

        if "name" in df:
            df.drop("name", axis=1, inplace=True)

        df = df.T
        df.fillna(value=np.nan, inplace=True)
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
    epoch = datetime.datetime.utcfromtimestamp(0)
    def unix_time_millis(dt):
        return int((dt - epoch).total_seconds() * 1000)

    try:
        return unix_time_millis(datetime.datetime.strptime(arg_datetime_str, "%Y-%m-%d %H:%M"))
    except ValueError:
        try:
            return unix_time_millis(datetime.datetime.strptime(arg_datetime_str, "%Y-%m-%d"))
        except ValueError:
            msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-MM-DD HH:mm' or 'YYYY-MM-DD'!".format(arg_datetime_str)
            raise argparse.ArgumentTypeError(msg)  


config = {
    "default"               : {

                                "url"        :  "",
                                "param"      : None,
                                "mani"       : "format_by_name",
                                "call"       : "call_api",
                                "argparse"   : {
                                    "name"     : {"action":"store",  "type":str, "help":"Search column which contains the given name"},
                                    "filters"  : {"action":"store",  "type":str, "help":"Returns only given filters out of the returned value. Default all values are returned"},
                                    "search"   : {"action":"store",  "type":str, "help":"Search any value within the return, e.g. search for USB interfaces"},
                                    "rows_name": {"action":"store_true", "dest":"rows", "default":False, "help":"Returns only the row names from the output result."},
                                    "stats"    : {"action":"store_true", "default":False, "help":"Returns the statistics of the datastructure"}
                                 }
                              },
    "login"                 : {
                                    "call"       : "login",
                                    "mani"       : "", 
                                    "description": "Login method into VCO. First method that should be called before execuiting any other. Will store authentication cookie.",
                                    "argparse"   : { 
                                        "username":    {"action":"store",      "type":str,            "default":os.getenv('VCO_USER', None), "help":"Username for authentication"},
                                        "password":    {"action":Password,     "type":str,"nargs":'?',"default":os.getenv('VCO_PASS', ""),   "help":"Password for authentication"},
                                        "no-operator": {"action":"store_false","dest":"is_operator",  "default":True,                        "help":"Login not as operator user"},
                                        "name": None,
                                        "filters": None,
                                        "rows_name": None,
                                        "stats" : None,
                                        "search": None 
                                    }
                             },
    "logout"                 : { 
                                    "call"       : "logout",
                                    "mani"       : "", 
                                    "description": "Logout from VCO. Last method that should be called, for cleaning up. Will delete try to delete the authentication cookie.",
                                    "argparse"   : {
                                        "name": None,
                                        "filters": None,
                                        "rows_name": None,
                                        "stats" : None,
                                        "search": None 
                                    }
                              },
    "edges_get"              : {
                                    "url"        : "enterprise/getEnterpriseEdges",
                                    "param"      : '{ "with":["certificates","configuration","links","recentLinks","site","vnfs","licences","cloudServices","cloudServiceSiteStatus"], "enterpriseId": %(enterpriseid)i }',
                                    "description": "Get basic information for all/some VCEs",
                                    "argparse"   : { 
                                        "enterpriseid": {"action":"store", "type":int, "default":1, "help":"Returns the Edges of only that given enterprise. Default all Edges of all enterprises at operator view or all Edges of an enterprise at customer view are returned." }
                                    }
                             },
    "edges_get_lm"           : {
                                    "url"        : "metrics/getEdgeLinkMetrics",
                                    "param"      : '{ "edgeId": %(edgeid)i, "enterpriseId": %(enterpriseid)i, "interval": { "end": %(endtime)i, "start": %(starttime)i}, "metrics": ["bytesRx", "bytesTx", "totalBytes", "totalPackets", "p1BytesRx", "p1BytesTx", "p1PacketsRx", "p1PacketsTx", "p2BytesRx", "p2BytesTx", "p2PacketsRx", "p2PacketsTx", "p3BytesRx", "p3BytesTx", "p3PacketsRx", "p3PacketsTx", "packetsRx", "packetsTx", "controlBytesRx", "controlBytesTx", "controlPacketsRx", "controlPacketsTx", "bestBwKbpsRx", "bestBwKbpsTx", "bestJitterMsRx", "bestJitterMsTx", "bestLatencyMsRx", "bestLatencyMsTx", "bestLossPctRx", "bestLossPctTx", "bpsOfBestPathRx", "bpsOfBestPathTx", "signalStrength", "scoreTx", "scoreRx"]}',
                                    "description": "Collect link statistics for a VCE between a given period",
                                    "argparse"   : { 
                                        "enterpriseid": {"action":"store", "type":int, "default":0, "help":"Get information for that specific Edge in that specific customer. EnterpriseId can be either found from *_customers_get method under id or edges_get method under enterpriseId." },
                                        "edgeid"      : {"action":"store", "type":int, "required":True, "help":"Get information for that specific Edge. Edgeid can be found under edges_get method under id."},
                                        "starttime"   : {"action":"store", "type":valid_datetime_type, "required":True,"help":"The start time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM."},
                                        "endtime"     : {"action":"store", "type":valid_datetime_type, "default":valid_datetime_type(str(datetime.date.today())),"help":"The end time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM."}
                                    }
                             },
    "edges_get_agg_lm"           : {
                                    "url"        : "monitoring/getAggregateEdgeLinkMetrics",
                                    "param"      : '{ "enterpriseId": %(enterpriseid)i, "interval": { "end": %(endtime)i, "start": %(starttime)i}, "metrics": ["bytesRx", "bytesTx", "totalBytes", "totalPackets", "p1BytesRx", "p1BytesTx", "p1PacketsRx", "p1PacketsTx", "p2BytesRx", "p2BytesTx", "p2PacketsRx", "p2PacketsTx", "p3BytesRx", "p3BytesTx", "p3PacketsRx", "p3PacketsTx", "packetsRx", "packetsTx", "controlBytesRx", "controlBytesTx", "controlPacketsRx", "controlPacketsTx", "bestBwKbpsRx", "bestBwKbpsTx", "bestJitterMsRx", "bestJitterMsTx", "bestLatencyMsRx", "bestLatencyMsTx", "bestLossPctRx", "bestLossPctTx", "bpsOfBestPathRx", "bpsOfBestPathTx", "signalStrength", "scoreTx", "scoreRx"]}',
                                    "description": "Collect aggregated link statistics for several VCEs between a given period",
                                    "argparse"   : { 
                                        "enterpriseid": {"action":"store", "type":int, "required": True, "default":0, "help":"Get information for that specific Edge in that specific customer. EnterpriseId can be either found from *_customers_get method under id or edges_get method under enterpriseId." },
                                        "starttime"   : {"action":"store", "type":valid_datetime_type, "required":True,"help":"The start time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM."},
                                        "endtime"     : {"action":"store", "type":valid_datetime_type, "default":valid_datetime_type(str(datetime.date.today())),"help":"The end time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM."}
                                    }
                             },
    "operator_customers_get" : {
                                    "url"        : "network/getNetworkEnterprises",
                                    "param"      : '{ "with":["edges"], "networkId": 1}',
                                    "description": "Get all customers as an operator user",
                                     "argparse"   : {}
                             },
    "msp_customers_get"      : {
                                    "url"        : "enterpriseProxy/getEnterpriseProxyEnterprises",
                                    "param"      : '{ "with":["edges"] }',
                                    "description": "Get all customers as an msp user",
                                    "argparse"   : {}
                             },
    "gateway_get_edges"      : {
                                    "url"        : "gateway/getGatewayEdgeAssignments",
                                    "param"      : '{ "gatewayId": %(gatewayid)i }',
                                    "description": "Get edges behind given gateway",
                                    "argparse"   : { 
                                        "gatewayid"   : {"action":"store", "type":int, "required":True, "help":"Provide gatewayid to get the edges" }
                                    }
                             },
    "enterprise_get"         : {
                                    "url"        : "enterprise/getEnterprise",
                                    "param"      : '{ "with":[], "enterpriseId": %(enterpriseid)i }',
                                    "description": "Get data for the specified enterprise",
                                    "argparse"   : {
                                        "enterpriseid": {"action":"store", "type":int, "default":1, "help":"Returns the data of only that given enterprise." }
                                    }
                             },
    "enterprise_get_gateway" : {
                                    "url"        : "enterprise/getEnterpriseAddresses",
                                    "param"      : '{ "enterpriseId": %(enterpriseid)i }',
                                    "description": "Get gateways associated to given enterprise",
                                    "argparse"   : { 
                                        "enterpriseid": {"action":"store", "type":int, "required":True, "help":"Provide enterpriseid to get the gateways" }
                                    }
                             },
    "enterprise_get_users"   : {
                                    "url"        : "enterprise/getEnterpriseUsers",
                                    "param"      : '{ "enterpriseId": %(enterpriseid)i }',
                                    "description" : "Get users associated to given enterprise",
                                    "argparse": {
                                       "enterpriseid": {"action": "store", "type": int, "required": True,
                                                        "help": "Provide enterpriseid to get the gateways"}
                                    }
                              },
    "enterprise_get_net_segs": {
        "url": "enterprise/getEnterpriseNetworkSegments",
        "param": '{ "enterpriseId": %(enterpriseid)i }',
        "description": "Get all network segments for given enterprise",
        "argparse": {
            "enterpriseid": {"action": "store", "type": int, "required": True,
                             "help": "Provide enterpriseid to get the network segments"}
        }
    },
    "enterprise_get_services": {
        "url": "enterprise/getEnterpriseServices",
        "param": '{ "enterpriseId": %(enterpriseid)i }',
        "description": "Get all services for given enterprise",
        "argparse": {
            "enterpriseid": {"action": "store", "type": int, "required": True,
                             "help": "Provide enterpriseid to get the services"}
        }
    },

    #"enterprise_get_edge_status": {
                                    #"url"        : "/monitoring/getEnterpriseEdgeStatus",
                                    #"param"       : '{ "enterpriseId": %(enterpriseid)i, "edgeids":[13220], "time": %(time)i, "more": True, "limit": 100, "sort": "cpuPct", "metrics": ["tunnelCount", "memoryPct", "flowCount", "cpuPct", "handoffQueueDrops" ]}',
                                    #"param"       : '{ "enterpriseId": %(enterpriseid)i, "interval": {"start": %(time)i},"sort": "tunnelCount", "metrics": ["tunnelCount", "memoryPct", "flowCount", "cpuPct", "handoffQueueDrops" ]}',
                                    #"param"       : '{ "enterpriseId": %(enterpriseid)i, "edgeids":[13220], "interval": {"start": %(time)i}, "more": True, "limit": 100, "sort": "cpuPct", "metrics": ["tunnelCount", "memoryPct", "flowCount", "cpuPct", "handoffQueueDrops" ]}',
     #                               "param"       : '{ "enterpriseId": %(enterpriseid)i, "edgeIds": [5994], "limit": 10000, "sort": "tunnelCount"}',
     #                               "mani"       : "",
     #                               "description": "Get status of all enterprise edges",
     #                               "argparse"   : { 
     #                                   "enterpriseid": {"action":"store", "type":int, "default":0, "help":"EnterpriseId can be either found from *_customers_get method under id or edges_get method under enterpriseId." },
     #                                   "time"      : {"action":"store", "type":valid_datetime_type, "default":valid_datetime_type(str(datetime.date.today())),"help":"The end time from when one wants to get the data. Format is in YYYY-MM-DD or YYYY-MM-DD HH:MM."},
     #                                   "filters"   : None,
     #                                   "rows_name" : None,
     #                                   "stats"     : None,
     #                                   "search"    : None
     #                               }
     #                       },
    "sysprop_set"            : {
                                    "url"        : "systemProperty/insertOrUpdateSystemProperty",
                                    "param"      : '{ "name": "%(name)s", "value": "%(value)s"}',
                                    "description": "Set new/edit system property values",
                                    "argparse": {
                                        "name"      : {"action":"store", "type":str, "required":True, "help":"Name of the new/edit system property"},
                                        "value"     : {"action":"store", "type":str, "required":True, "help":"New value of the system properties"},
                                        "filters"   : None,
                                        "rows_name" : None,
                                        "stats"     : None,
                                        "search"    : None
                            }

    }
}

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

    dic = {}
    for method in config:
        if method == "default":
            continue
        dic[method] = subparsers.add_parser(method, description=config[method].get("description",""))
        for key, value in config["default"].items():
            config[method].setdefault(key, value) 
        for key, value in config["default"]["argparse"].items():
            config[method]["argparse"].setdefault(key, value) 
        for key in config[method]["argparse"]:
            if not config[method]["argparse"][key]:
                continue
            args = config[method]["argparse"][key]
            if "dest" not in args:
                   args["dest"] = key
            dic[method].add_argument("--{}".format(key), **args)
        dic[method].set_defaults(dest=method)


    args = parser.parse_args()

    if "dest" not in args:
        parser.print_help(sys.stderr)
    else:
        obj = VcoApiExecute(**vars(args))
        if obj.p is not None:
            print(obj.p)
