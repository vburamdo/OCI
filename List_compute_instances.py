#/usr/bin/env python
'''
Description: This script is to list following details:
    Instance Display name , public/prive ip and internal name
    LB name, IP, shape 
Author : vinod.buramdoddi
Date: 2-Mar-2019
Version: 4.0
'''

import oci
import json
import os,sys



subnet_info = {}
vcn_info = {}
private_ip_to_public_ip = {}
insta_list = {}
complete_data = {}
compartmtns = {}
all_lbs={}

def instance_list(comp_ocid):
    command = "oci compute instance list --compartment-id " + comp_ocid + " 2>/dev/null"
    instance_details = os.popen(command).read()
    if len(instance_details) > 0 :
        inst_jsondata = json.loads(instance_details)
        for line in inst_jsondata['data']:
            displayname = line['display-name']
            imageid = line['id']
            insta_list[displayname] = imageid
        if len(insta_list) > 0:
            for key in insta_list.keys():
                i_details = {}
                instance_id = insta_list[key]
                host_details = os.popen('oci compute instance list-vnics --instance-id  ' + instance_id).read()
                if len(host_details) > 0:
                    host_details_jsondata = json.loads(str(host_details))
                    for line in host_details_jsondata['data']:
                        i_details['private-ip'] =line['private-ip']
                        i_details['public-ip'] =line['public-ip']
                        i_details['internal_name'] = line['hostname-label']
                    complete_data[key] = i_details
                

def loadbalancer(comp_ocid):
    lbs = {}
    lbcommand = " oci lb load-balancer list --compartment-id " + comp_ocid + " 2>/dev/null"
    lb_command_details = os.popen(lbcommand).read()
    if len(lb_command_details) > 0:
        lb_jsondata = json.loads(str(lb_command_details))
        for line in lb_jsondata['data']:
            lb_name = line['display-name']
            lb_ip = line['ip-addresses']
            shape = line['shape-name']
            lbs['ip_details'] = lb_ip
            lbs['shape_name']= shape
        all_lbs[lb_name] = lbs


config = oci.config.from_file()
compartment_list = os.popen("oci iam compartment list --all").read()
compartment_jsondata = json.loads(str(compartment_list))


for line in compartment_jsondata['data']:
    ocid = line['id']
    name = line['name']
    compartmtns[name] = ocid



print("\n")
for line in compartmtns.keys():
    comp_ocid = compartmtns[line]
    print("Gathering instance details on compartment: " + line)
    instance_list(comp_ocid)
    loadbalancer(comp_ocid)



print("\n======================================================================================")
print("LBAAS &Instance Details : DISPLAY NAME / PUBLIC IP/ PRIVATE IP/ Inetnal name with fqdn")
print("======================================================================================\n")
for line in complete_data.keys():
    name = line.strip()
    print(name + ": ")
    for a in complete_data[line].keys():
        print('\t' + a + ":"),
        print('\t' + "".join(complete_data[line][a]))


#

for line in all_lbs.keys():
    lbname = line
    print(lbname +": ")
    for keys in all_lbs[lbname].keys():
        print('\t' +keys + ":") ,
        print("".join(str(all_lbs[lbname][keys])))

print("\n======================================================================================\n")

####