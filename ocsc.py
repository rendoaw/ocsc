#!/usr/bin/env python

#######################################################
# ocsc.py
# A simple REST API client for OpenStack and Contrail 
# 
# rendo.aw at gmail.com @ 2016
#######################################################


import requests
import json
import yaml
import sys
import traceback
import datetime
import argparse
import logging
import logging.config
import os
import subprocess
import xmltodict

requests.packages.urllib3.disable_warnings()


def dump_env_variable():
    for key in os.environ:
        print key+" = "+os.environ[key]
    return 


def read_env_variable_file(env_file):
    command = ['bash', '-c', 'source '+env_file+' && env']
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.partition("=")
        os.environ[key] = str(value).replace('\n','')
    proc.communicate()
    return os.environ


def jsonpretty(text):
    return json.dumps(text, indent=4)


def yamlpretty(text):
    return yaml.dump(text, default_flow_style=False)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if type(obj) is datetime.date or type(obj) is datetime:
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def jsonprettystr(text):
    return json.dumps(text, indent=4, sort_keys=True, default=lambda x:str(x))


def yaml_file_to_json(yamlfile):
    with open(yamlfile, 'r') as f:
        yamldoc = yaml.load(f)
    f.close()
    return json.dumps(yamldoc, default=json_serial)


def json_to_csv(jsondata):
    for key in jsondata:
        txt = "#"
        for field in sorted(jsondata[key][0]):
            txt += str(field)+","
    txt += "\n"
    for key in jsondata:
        for item in jsondata[key]:
            for field in sorted(item):
                txt += str(item[field])+","
            txt += "\n"
    return txt


def get_curl_command(url, operation, headers, payload=None):
    cmd = "curl -g -i -X "+operation+" "+url+" "
    for header in headers:
        cmd += "-H \""+header+": "+headers[header]+"\" "
    if payload is not None:
        payload_text = str(payload).replace("'", "\"")
        cmd += "-d '"+payload_text+"'"
    return cmd



def arguments_parser():
    parser = argparse.ArgumentParser(description="Options:")
    parser.add_argument('--debug', action='store_true', help='print debug information to log file' )
    parser.add_argument('--verbose', action='store_true', help='print log to stdout' )
    
    parser.add_argument('--env', help='OpenStack/Contrail environment file. Default: read from existing environment variable.' )
    parser.add_argument('--find', help='find instance and print detail. Optional search criteria by --value <instance name>' )
    parser.add_argument('--get-token', action='store_true', help='Do OpenStack auth, get keystone token and exit' )
    parser.add_argument('--get-url', help='Access any given OpenStack REST API URL' )
    parser.add_argument('--csv', action='store_true', help='display output in csv format' )
    parser.add_argument('--list', help='list component instances' )
    parser.add_argument('--list-support', action='store_true', help='list supported resource' )
    parser.add_argument('--key', nargs='?', const=1, default="name", type=str, help='find resource by this attribute' )
    parser.add_argument('--value', nargs='?', const=1, default="", type=str, help='find resource by/show this value' )
    parser.add_argument('--show', help='show component instances' )
    parser.add_argument('--detail', action='store_true', help='enable detail mode' )
    parser.add_argument('--stack-template', help='HEAT stack template file' )
    parser.add_argument('--stack-parameter', help='HEAT stack parameter in json format' )
    parser.add_argument('--stack-parameter-file', help='HEAT stack parameter file' )
    parser.add_argument('--stack-create', help='Create HEAT Stack with name' )

    parser.add_argument('--contrail-find', help='find Contrail instance and print detail. Optional search criteria by --contrail-value <instance name>' )
    parser.add_argument('--contrail-get-resource', action='store_true', help='Do auth on Contrail, get list of all Contrail resources/components' )
    parser.add_argument('--contrail-get-token', action='store_true', help='Do auth on Contrail, get token and exit' )
    parser.add_argument('--contrail-get-url', help='Access any given Contrail REST API URL' )
    parser.add_argument('--contrail-key', nargs='?', const=1, default="fq_name", type=str, help='find Contrail resource by this attribute (for the future)' )
    parser.add_argument('--contrail-list', help='list Contrail specified component instances' )
    parser.add_argument('--contrail-show', help='show Contrail component instance specified by --contrail-value <instance id>' )
    parser.add_argument('--contrail-value', nargs='?', const=1, default="", type=str, help='find Contrail resource by/show this value' )
    parser.add_argument('--contrail-analytic-find', help='find Contrail analytic instance and print detail. Optional search criteria by --contrail-value <instance name>' )
    parser.add_argument('--contrail-analytic-list', help='list specified Contrail analytic component instances' )
    parser.add_argument('--contrail-analytic-show', help='show Contrail analytic component instance specified by --contrail-value <instance id>' )
    parser.add_argument('--contrail-vrouter-get-vrf-routes', help='Dump routing table of a VRF on specific compute. Usage: --contrail-vrouter-get-vrf-routes <vrfname>  --contrail-vrouter-host <vrouter hostname/IP>' )
    parser.add_argument('--contrail-vrouter-list-vrf', action='store_true', help='List VRF available in specific compute node. Usage: --contrail-vrouter-list-vrf --contrail-vrouter-host <vrouter hostname/IP>' )
    parser.add_argument('--contrail-vrouter-host', help='vrouter hostname or IP' )
    parser.set_defaults(detail=False)
    args = parser.parse_args()
    return args


class my_client(object):

    def __init__(self):
        pass
   

    def auth(self):
        headers = {'Content-Type':'application/json', 'Cache-Control': 'no-cache' }
        payload = {"auth": {"tenantName": self.tenant, "passwordCredentials": {"username": self.username, "password": self.password}}}
        logger.info("url = "+self.auth_url)
        logger.debug(get_curl_command(self.auth_url, "POST", headers, payload))
        r = requests.post(self.auth_url, verify=False, headers=headers, data=json.dumps(payload))
        self.auth_data = r.json()
        self.auth_status = r.status_code
        if r.status_code == 200:
            self.token = self.auth_data["access"]["token"]["id"]
        logger.info("status:"+str(r.status_code))
        logger.debug("data:"+jsonpretty(r.json()))
        return self.auth_status, self.auth_data

    
    def get_resource_url(self):
        pass
   

    def find_resource_url(self, resource_type, is_show=False):
        pass


    def find(self, resource_type, target_id="", target_field="", id_field="id", is_analytic=False):
        status, data = self.list(resource_type, is_analytic=is_analytic)
        if status != 200:
            logger.debug("HTTP status="+str(status))
            logger.debug("Data="+jsonpretty(data))
            return

        result = {}
        logger.debug("target_id="+target_id+" target_field="+target_field+" id_field="+id_field)
        for key in data:
            for item in data[key]:
                if target_id == "":
                    item_status, item_data = self.list(resource_type, is_show=True, resource_id=item[id_field])
                    result[item[id_field]] = item_data
                else:
                    '''TODO: find by any attribute'''
                    if target_field not in item:
                        result = "{'Error', 'Target field is not valid'}"
                        break
                    if isinstance(item[target_field], list):
                        '''contrail fq_name field is a list'''
                        if item[target_field][-1] == target_id:
                            item_status, item_data = self.list(resource_type, is_show=True, resource_id=item[id_field], is_analytic=is_analytic)
                            result[item[id_field]] = item_data
                    elif isinstance(item[target_field], int) or isinstance(item[target_field], float):
                        '''contrail fq_name field is an int'''
                        if str(item[target_field]) == target_id:
                            item_status, item_data = self.list(resource_type, is_show=True, resource_id=item[id_field], is_analytic=is_analytic)
                            result[item[id_field]] = item_data
                    else:
                        '''openstack name field is a string'''
                        if item[target_field] == target_id:
                            item_status, item_data = self.list(resource_type, is_show=True, resource_id=item[id_field], is_analytic=is_analytic)
                            result[item[id_field]] = item_data
        return result


    def get_url(self, url=""):
        '''TODO: check expiration time instead of re-auth every time'''
        data = {}
        self.auth()
        if self.auth_status != 200:
            return "" 
        
        headers = {'Content-Type':'application/json', 'Cache-Control': 'no-cache', 'X-Auth-Token': self.token }
        logger.info("url = "+url)
        logger.debug(get_curl_command(url, "GET", headers, None))
        
        r = requests.get(url, verify=False, headers=headers)
        status = r.status_code
        if status == 404:
            return status, { "Error": r.text }
        data = r.json()
        logger.info("status:"+str(r.status_code))
        logger.debug("data:"+jsonpretty(r.json()))
        return status, data


    def list(self, resource_type, is_show=False, resource_id="", is_detail=False, all_tenant=False, is_analytic=False):
        '''TODO: check expiration time instead of re-auth every time'''
        url = ""
        data = {}
        
        self.auth()
        if self.auth_status != 200:
            return "" 
      
        if is_show:
            service_url = self.find_resource_url(resource_type, is_show=True, is_analytic=is_analytic)
            service_url += "/"+resource_id
        else:
            service_url = self.find_resource_url(resource_type, is_show=False, is_analytic=is_analytic)
            if is_detail:
                service_url += "/detail"
            if all_tenant:
                service_url += "?all_tenants=1"
        if service_url == "":
            return 999, { "Error": "can not decide the url to query" }
       
        status, data = self.get_url(service_url)
        return status, data

   

class my_contrail(my_client):

    def __init__(self, auth_url="", username="", password="", tenant="", contrail_url=""):
        self.auth_url = auth_url
        self.contrail_url = contrail_url
        self.token_url = auth_url+"tokens"
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_data = {}
        self.service_data = {}
        self.auth_status = -1
        self.token = ""
        self.publicURL = {}
        self.is_authenticated = False
        #self.resource_map = {}
        #self.init_map()

    
#    def init_map(self):
#        self.add_resource_map(resource_type="virtual-network", list_url="virtual-networks", show_url="virtual-network", port="8082", analytic_url="virtual-network")
#        self.add_resource_map(resource_type="virtual-router", list_url="virtual-routers", show_url="virtual-router", port="8082", analytic_url="vrouter")
#        
#
#    def add_resource_map(self, resource_type="", list_url="", show_url="", port=""):
#        self.resource_map[resource_type] = {}
#        self.resource_map[resource_type]["list_url"] = list_url
#        self.resource_map[resource_type]["show_url"] = show_url
#        if analytic_url != "":
#            self.resource_map[resource_type]["analytic_url"] = analytic_url
#        self.resource_map[resource_type]["port"] = port


    def get_resource_url(self):
        '''TODO: check expiration time instead of re-auth every time'''
        url = ""
        data = {}
        
        self.auth()
        if self.auth_status != 200:
            return "" 
        
        url = self.contrail_url+":8082/" 
        headers = {'Content-Type':'application/json', 'Cache-Control': 'no-cache', 'X-Auth-Token': self.token }
        logger.info("url = "+url)
        logger.debug(get_curl_command(url, "GET", headers, None))
        r = requests.get(url, verify=False, headers=headers)
        status = r.status_code
        if status == 404:
            return status, { "Error": r.text }
        self.service_data = r.json()
        logger.info("status:"+str(r.status_code))
        logger.debug("data:"+jsonpretty(r.json()))
        return status, data

    
    def find_resource_url(self, resource_type, is_show=False, is_analytic=False):
        url = ""
       
        url = self.contrail_url
        #if resource_type in self.resource_map:
        #    show_url = self.resource_map[resource_type]["show_url"]
        #    list_url = self.resource_map[resource_type]["list_url"]
        #    port = self.resource_map[resource_type]["port"]
        #else:
        #    return 999, { "Error": "can not decide openstack component to query" }
        
        #if is_show:
        #    url += ":"+port+"/"+show_url
        #else:
        #    url += ":"+port+"/"+list_url
        
        '''TODO: fix this, hardcoded for now'''
        if is_analytic:
            port = "8081/analytics/uves"
        else:
            port = "8082"
        if is_show:
            url += ":"+port+"/"+resource_type
        else:
            url += ":"+port+"/"+resource_type+"s"
        return url

    
    def introspect_access(self, host="", parameter=""):
        url = "http://"+host+":8085/"+parameter
        headers = {'Content-Type':'application/json', 'Cache-Control': 'no-cache', 'X-Auth-Token': self.token }
        logger.info("url = "+url)
        logger.debug(get_curl_command(url, "GET", headers, None))
        r = requests.get(url, verify=False, headers=headers)
        status = r.status_code
        if status == 404:
            return status, { "Error": r.text }
        data = xmltodict.parse(r.text, xml_attribs=True)
        logger.info("status:"+str(r.status_code))
        logger.debug("data:"+jsonpretty(data))
        return status, data

    
    def introspect_get_vrf_list(self, host):
        parameter = "Snh_VrfListReq?name="
        status, data = self.introspect_access(host, parameter)
        result = "#VRF Name,ucindex,uc6index,mcindex,l2index,vxlan_id\n"
        if status == 200:
            try:
                vrflist = data["__VrfListResp_list"]["VrfListResp"]["vrf_list"]["list"]["VrfSandeshData"]
            except:
                return status, { 'Error', 'VrfSandeshData can not be decoded' }
            for item in vrflist:
                result += item["name"]["#text"]+","+item["ucindex"]["#text"]+","+item["uc6index"]["#text"]+","+item["mcindex"]["#text"]+","+item["l2index"]["#text"]+","+item["vxlan_id"]["#text"]
                result += "\n"
        return status, data, result


    def introspect_get_Layer2Route(self, host="", vn_name="", vrf_id=""):
        #parameter = "Snh_Layer2RouteReq?vrf_index="+vrf_id+"&mac=&stale="
        parameter = "Snh_PageReq?x=begin:-1,end:-1,table:"+vn_name+".l2.route.0,"
        status, data = self.introspect_access(host, parameter)
        return status, data


    def introspect_get_Inet4UcRoute(self, host="", vn_name="", vrf_id=""):
        #parameter = "Snh_Inet4UcRouteReq?vrf_index="+vrf_id+"&src_ip=&prefix_len=&stale="
        parameter = "Snh_PageReq?x=begin:-1,end:-1,table:"+vn_name+".uc.route.0,"
        status, data = self.introspect_access(host, parameter)
        return status, data


    def introspect_get_Inet6UcRoute(self, host="", vn_name="", vrf_id=""):
        #parameter = "Snh_Inet4UcRouteReq?vrf_index="+vrf_id+"&src_ip=&prefix_len=&stale="
        parameter = "Snh_PageReq?x=begin:-1,end:-1,table:"+vn_name+".uc.route6.0,"
        status, data = self.introspect_access(host, parameter)
        return status, data


    def introspect_get_Inet4McRoute(self, host="", vn_name="", vrf_id=""):
        #parameter = "Snh_Inet4UcRouteReq?vrf_index="+vrf_id+"&src_ip=&prefix_len=&stale="
        parameter = "Snh_PageReq?x=begin:-1,end:-1,table:"+vn_name+".mc.route.0,"
        status, data = self.introspect_access(host, parameter)
        return status, data


    def introspect_get_all_routes(self, host="", vn_name="", vrf_id=""):
        routes = {}
        status, data = self.introspect_get_Inet4UcRoute(host=host, vn_name=vn_name)
        routes["Inet4UcRoute"] = data
        status, data = self.introspect_get_Inet6UcRoute(host=host, vn_name=vn_name)
        routes["Inet6UcRoute"] = data
        status, data = self.introspect_get_Inet4McRoute(host=host, vn_name=vn_name)
        routes["Inet4McRoute"] = data
        status, data = self.introspect_get_Layer2Route(host=host, vn_name=vn_name)
        routes["InetLayer2Route"] = data
        return routes





class my_openstack(my_client):

    def __init__(self, auth_url="", username="", password="", tenant=""):
        self.auth_url = auth_url
        self.token_url = auth_url+"tokens"
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_data = {}
        self.auth_status = -1
        self.token = ""
        self.publicURL = {}
        self.is_authenticated = False
        self.resource_map = {}
        self.init_map()

    
    def init_map(self):
        self.add_resource_map("images", "nova", "images", False)
        self.add_resource_map("servers", "nova", "servers", True)
        self.add_resource_map("flavors", "nova", "flavors", True)
        self.add_resource_map("stacks", "heat", "stacks", True)
        self.add_resource_map("networks", "neutron", "v2.0/networks", False)
        self.add_resource_map("subnets", "neutron", "v2.0/subnets", False)
        self.add_resource_map("routers", "neutron", "v2.0/routers", False)
        self.add_resource_map("ports", "neutron", "v2.0/ports", False)
        self.add_resource_map("floatingips", "neutron", "v2.0/floatingips", False)
        self.add_resource_map("security-groups", "neutron", "v2.0/security-groups", False)
        self.add_resource_map("security-group-rules", "neutron", "v2.0/security-group-rules", False)
        self.add_resource_map("quotas", "neutron", "v2.0/quotas", False)
        self.add_resource_map("lbaas/loadbalancers", "neutron", "v2.0/lbaas/loadbalancers", False)
        self.add_resource_map("lbaas/listeners", "neutron", "v2.0/lbaas/listeners", False)
        self.add_resource_map("lbaas/pools", "neutron", "v2.0/lbaas/pools", False)
        self.add_resource_map("lbaas/health_monitors", "neutron", "v2.0/lbaas/health_monitors", False)
        self.add_resource_map("lb/pools", "neutron", "v2.0/lb/pools", False)
        self.add_resource_map("lb/vips", "neutron", "v2.0/lb/vips", False)
        self.add_resource_map("lb/members", "neutron", "v2.0/lb/members", False)
        self.add_resource_map("lb/health_monitors", "neutron", "v2.0/lb/health_monitors", False)
        self.add_resource_map("fw/firewall_policies", "neutron", "v2.0/fw/firewall_policies", False)
        self.add_resource_map("fw/firewall_rules", "neutron", "v2.0/fw/firewall_rules", False)
        self.add_resource_map("fw/firewalls", "neutron", "v2.0/fw/firewalls", False)
        self.add_resource_map("auth/tokens", "keystone", "v3/auth/tokens", False)
        self.add_resource_map("credentials", "keystone", "v3/credentials", False)
        self.add_resource_map("domains", "keystone", "v3/domains", False)
        self.add_resource_map("groups", "keystone", "v3/groups", False)
        self.add_resource_map("projects", "keystone", "v3/projects", False)
        self.add_resource_map("regions", "keystone", "v3/regions", False)
        self.add_resource_map("tenants", "keystone", "v2.0/tenants", False)
        

    def add_resource_map(self, resource_type="", component="", url="", has_detail=False, can_create=False):
        self.resource_map[resource_type] = {}
        self.resource_map[resource_type]["component"] = component
        self.resource_map[resource_type]["url"] = url
        self.resource_map[resource_type]["has_detail"] = False
        self.resource_map[resource_type]["can_create"] = can_create


    def find_resource_url(self, resource_type, is_show=False, is_analytic=False):
        url_type = "publicURL"
        url = ""
        
        if resource_type in self.resource_map:
            component = self.resource_map[resource_type]["component"]
        else:
            print '{ "Error": "can not decide openstack component to query" }'
            sys.exit(102)
        
        for service in self.auth_data["access"]["serviceCatalog"]:
            if service["name"] == component:
                if resource_type in self.resource_map:
                    url = service["endpoints"][0][url_type]
                    break
        url = url+"/"+self.resource_map[resource_type]["url"]
        return url


    def stack_create(self, stack_name, template, parameters):
        '''TODO: check expiration time instead of re-auth every time'''
        url = ""
        data = {}
        self.auth()
        if self.auth_status != 200:
            return "" 
        for service in self.auth_data["access"]["serviceCatalog"]:
            if service["name"] == "heat":
                print jsonpretty(service)
                url = service["endpoints"][0]["publicURL"]+"/stacks"
        
        payload = {}
        payload["files"] = {}
        payload["disable_rollback"] = True
        payload["parameters"] = parameters
        payload["stack_name"] = stack_name
        payload["environment"] = {}
        payload["template"] = template
        
        headers = {'Content-Type':'application/json', 'Cache-Control': 'no-cache', 'X-Auth-Token': self.token }
        if url == "":
            return ""

        logger.info("url = "+url)
        logger.debug(get_curl_command(url, "GET", headers, payload))

        r = requests.post(url, verify=False, headers=headers, data=json.dumps(payload))
        status = r.status_code
        if status == 404:
            return status, { "Error": r.text }
        data = r.json()
        logger.info("status:"+str(r.status_code))
        logger.debug("data:"+jsonpretty(r.json()))
        return status, data




if __name__ == "__main__":
    
    args = arguments_parser()
    
    logger = logging.getLogger(__name__)
    LOG_FORMAT = "%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s %(lineno) -5d: %(message)s"
    hdlr = logging.handlers.RotatingFileHandler(filename="ocsc.log", mode='a', maxBytes=10000000, backupCount=3, encoding="utf8")
    hdlr.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(hdlr)
    if args.verbose:
        LOG_FORMAT = "%(asctime)s %(message)s"
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter(LOG_FORMAT))
        logging.getLogger().addHandler(consoleHandler)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    logger.info("Program started")

    env = {}
    if args.env:
        env = read_env_variable_file(args.env)
    else:
        env = os.environ
   
    is_contrail_mode = False
    if args.contrail_list or args.contrail_show or args.contrail_get_url or args.contrail_get_resource or args.contrail_get_token or args.contrail_find:
        is_contrail_mode = True
    if args.contrail_analytic_list or args.contrail_analytic_show or args.contrail_analytic_find:
        is_contrail_mode = True
    if args.contrail_vrouter_get_vrf_routes or args.contrail_vrouter_list_vrf or args.contrail_vrouter_host:
        is_contrail_mode = True
    
    '''initialize contrail client only if any contrail related parameter is detected'''
    if is_contrail_mode == True:
        contrail_client = my_contrail(auth_url=env["OS_AUTH_URL"]+"/tokens", username=env["OS_CONTRAIL_USERNAME"], password=env["OS_CONTRAIL_PASSWORD"], tenant=env["OS_CONTRAIL_TENANT_NAME"], contrail_url=env["OS_CONTRAIL_URL"])
    
        if args.contrail_find:
            data = contrail_client.find(args.contrail_find, target_id=args.contrail_value, target_field=args.contrail_key, id_field="uuid")
            print jsonpretty(data)

        if args.contrail_get_resource:
            status, data = contrail_client.get_resource_url()
            #print "HTTP status code: "+str(status)
            if args.csv:
                print json_to_csv(data)
            else:
                print jsonpretty(data)

        if args.contrail_get_token:
            contrail_client.auth()
            print contrail_client.token

        if args.contrail_get_url:
            status, data = contrail_client.get_url(args.contrail_get_url)
            print jsonpretty(data)
        
        if args.contrail_list:
            '''example: list instances'''
            status, data = contrail_client.list(args.contrail_list)
            #print "HTTP status code: "+str(status)
            if args.csv:
                print json_to_csv(data)
            else:
                print jsonpretty(data)

        if args.contrail_show:
            if args.contrail_value == "":
                print "{ 'Error': '--name must not be empty. The correct syntax is --show <component name> --value <component ID>'}"
                sys.exit(104)
            else:
                status, data = contrail_client.list(args.contrail_show, resource_id=args.contrail_value, is_show=True)
            if args.csv:
                print json_to_csv(data)
            else:
                print jsonpretty(data)


        if args.contrail_analytic_find:
            data = contrail_client.find(args.contrail_analytic_find, target_id=args.contrail_value, target_field=args.contrail_key, id_field="uuid", is_analytic=True)
            print jsonpretty(data)

        if args.contrail_analytic_list:
            '''example: list instances'''
            status, data = contrail_client.list(args.contrail_analytic_list,is_analytic=True)
            #print "HTTP status code: "+str(status)
            if args.csv:
                print json_to_csv(data)
            else:
                print jsonpretty(data)

        if args.contrail_analytic_show:
            if args.contrail_value == "":
                print "{ 'Error': '--name must not be empty. The correct syntax is --show <component name> --value <component ID>'}"
                sys.exit(104)
            else:
                status, data = contrail_client.list(args.contrail_analytic_show, resource_id=args.contrail_value, is_show=True, is_analytic=True)
            if args.csv:
                print json_to_csv(data)
            else:
                print jsonpretty(data)

        if args.contrail_vrouter_list_vrf and args.contrail_vrouter_host: 
            status, data, csv = contrail_client.introspect_get_vrf_list(args.contrail_vrouter_host)
            if args.csv:
                print csv
            else:
                print jsonpretty(data)
            
        if args.contrail_vrouter_get_vrf_routes and args.contrail_vrouter_host: 
            data = contrail_client.introspect_get_all_routes(args.contrail_vrouter_host, args.contrail_vrouter_get_vrf_routes)
            print jsonpretty(data)



    '''initialize openstack client'''
    client = my_openstack(auth_url=env["OS_AUTH_URL"]+"/tokens", username=env["OS_USERNAME"], password=env["OS_PASSWORD"], tenant=env["OS_TENANT_NAME"])


    if args.find:
        data = client.find(args.find, target_id=args.value, target_field=args.key, id_field="id")
        print jsonpretty(data)

    if args.get_token:
        client.auth()
        print client.token

    if args.get_url:
        status, data = client.get_url(args.get_url)
        print jsonpretty(data)

    if args.list:
        status, data = client.list(args.list, is_detail=args.detail)
        #print "HTTP status code: "+str(status)
        if args.csv:
            print json_to_csv(data)
        else:
            print jsonpretty(data)
    
    if args.list_support:
        for item in client.resource_map:
            print item

    if args.show:
        if args.value == "":
            print "{ 'Error': '--name must not be empty. The correct syntax is --show <component name> --value <component ID>'}"
            sys.exit(103)
        status, data = client.list(args.show, is_show=True, resource_id=args.value)
        #print "HTTP status code: "+str(status)
        if args.csv:
            print json_to_csv(data)
        else:
            print jsonpretty(data)

    if args.stack_create:
        if args.stack_template:
            stack_template = yaml_file_to_json(args.stack_template)
        else:
            print "{'Error': 'Stack template file is not specified'}"

        if args.stack_parameter:
            stack_parameter = json.loads(args.stack_parameter)
        elif args.stack_parameter_file:
            stack_parameter = json.loads(yaml_file_to_json(args.stack_parameter_file))
        else:
            print "{'Error': 'Stack parameter/parameter-file is not specified'}"
        
        status, data = client.stack_create(args.stack_create, stack_template, stack_parameter)
        print jsonpretty(data)


