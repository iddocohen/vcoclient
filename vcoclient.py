#!/usr/bin/env python3

# Needed libaries
import requests, pickle, json, re, argparse, os
import pandas as pd
from pandas.io.json import json_normalize

# To be able to disable SSL warnings as needed e.g. development environment
from requests.packages.urllib3.exceptions import InsecureRequestWarning

VERIFY_SSL=False

# TODO: Might want to have some logic to increase rows/columns
#pd.set_option('display.max_columns', 100)
#pd.set_option('display.max_rows', 100)

class ApiException(Exception):
    pass

class VcoRequestManager(object):

    #TODO: Give path outside here for the user to alter
    def __init__(self, hostname, verify_ssl=VERIFY_SSL, path="/tmp/"):
        """
        Init the Class
        """
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
            return True
        return False
        
         
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
                return True
            except:
                return False	

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
            except:
               return False

    def _del_cookie(self):
        """
        Delete VCO session cookie
        """
      
        try: 
           os.remove(self._store_cookie)
        except:
           raise ApiException("Cannot delete cookie file")

def logout(args):
    """
    Logout from VCO
    """ 
    client = VcoRequestManager(args.hostname)
    o = client.authenticate(logout=True) 
    print(o)
    

def login (args):
    """
    Login at VCO
    """
    client = VcoRequestManager(args.hostname)
    o = client.authenticate(args.username, args.password, is_operator=args.operator)
    print (o)
        
def edges_get (args):  
    """
    Gets edges from VCO.  
    """
    client = VcoRequestManager(args.hostname)
    o = client.call_api("enterprise/getEnterpriseEdges", { "with":["certificates","configuration","links","recentLinks","site"], "enterpriseId": args.id })
    j = json.loads(json.dumps(o))
    df = pd.DataFrame.from_dict(json_normalize(j), orient='columns')
    out = df
    pd.options.mode.chained_assignment = None
    if args.name:
      out = df[df['name'].str.contains(args.name)]

    if args.parameter:
      out = out[out.columns[out.columns.str.match(args.parameter)]]

    out.rename(index=out.name.to_dict(), inplace=True)
    out = out.T

    # Wow how complicated the above is much easier, indeed uses a bit more memory...
    '''
    out = None 
    if args.name and args.parameter:
      out = df[df['name'].str.contains(args.name)]
      out = out[out.columns[out.columns.str.match(args.parameter)]].T
    elif args.name and not args.parameter:
      out = df[df['name'].str.contains(args.name)].T
    elif not args.name and args.parameter:
      out = df[df.columns[df.columns.str.match(args.parameter)]].T
    else:
      out = df.T
    '''

    # TODO: Lets not convert it twice in a case JSON is chosen as default output
    if args.output == "json":
      out = out.T.to_json()
    elif args.output == "csv":
      out = out.T.to_csv()

    print(out)
    pd.options.mode.chained_assignment = 'warn'

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
      print("True")
    else:
      print(o)
    

if __name__ == "__main__":
    """
    Based on the arguements provided, it will execute a given function
    """
    parser = argparse.ArgumentParser(description="A simple VeloCloud Orchestrator (VCO) client via Python")
    parser.add_argument("--vco", action="store", type=str, dest="hostname", required=True,
                        help="Hostname/IP of VCO")
    parser.add_argument("--output", action="store", type=str, dest="output", default="pandas", choices=["pandas", "json", "csv"],
                        help="Pandas tables are used as default output method but one can also use 'json' or 'csv'")

    
    subparsers = parser.add_subparsers()

    # Login function
    parser_login = subparsers.add_parser("login")
    parser_login.add_argument("--username", action="store", type=str, dest="username", required=True,
                              help="Username for Authentication")

    parser_login.add_argument("--password", action="store", type=str, dest="password", default="",
                              help="Password for Authentication")
    
    parser_login.add_argument("--no-operator", action="store_false", dest="operator", default=True,
                              help="Per default we login as operator to VCO. If not, use this flag")

    parser_login.set_defaults(func=login)
    
    # Logout function
    parser_logout = subparsers.add_parser("logout")
    parser_logout.set_defaults(func=logout)


    # Get all Edges from Operator View
    parser_getedges = subparsers.add_parser("edges_get")
    
    parser_getedges.add_argument("--name", action="store", type=str, dest="name", 
                              help="Search Edge/Edges containing the given name")
    
    parser_getedges.add_argument("--parameter", action="store", type=str, dest="parameter",
                              help="Returns only given parameters out of the returned value. Default all values are returned")
    
    parser_getedges.add_argument("--id", action="store", type=int, dest="id", default=1,
                              help="Returns the Edges of only that given enterprise. Default all Edges of all enterprises at operator view or all Edges of an enterprise at customer view are returned.")

    parser_getedges.set_defaults(func=edges_get)

    # Update/insert system properties in VCO
    parser_sysprop_set = subparsers.add_parser("sysprop_set")
    
    parser_sysprop_set.add_argument("--name", action="store", type=str, dest="name", required=True, 
                              help="Name of the new/edit system property")

    parser_sysprop_set.add_argument("--value", action="store", type=str, dest="value", required=True, 
                              help="New value of the system property")
    
    parser_sysprop_set.set_defaults(func=sysprop_set)
    
    args = parser.parse_args()
    args.func(args)

