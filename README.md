# Just Another OpenStack and Contrail Simple Client (OCSC)

## Overview

In a nutshel, OCSC is a single script that serves as OpenStack and Contrail client. The purpose of this script is mainly for OpenStack/Contrail troubleshooting or system administration.
By design, this script is connecting directly to OpenStack and Contrail REST API instead of using OpenStack client comand line or Contrail VNC API. This way, we do not need to install any Contrail or OpenStack client package in order to send or retrive the data. 
The script has been built based on my personal experience during OpenStack or Contrail operation troubleshooting, so it will not have complete functionality as native OpenStack CLI client and it may or may not applicable to your use cases. 
Additionally, i believe we can use the script as a starting point to learn about raw REST API from OpenStack and Contrail. 


## What you can do with current version

#### OpenStack 

* Get authentication token
* List and show detail information of many of OpenStack components, e.g: nova, glance image, virtual-networks, floating IP, etc.
* Find specific component resource and display its detail information
* Create a HEAT stack (limited)


#### Contrail

* List and show detail information of many of Contrail components e.g: virtual-network, vrouter, xmpp-peer, etc
    * And, since Contrail API also cover OpenStack component, you can also get the detail information of the VM instance, and other things
* Find specific Contrail component resource and display its detail information
* List and display detail Contrail analytics data, e.g: VM CPU info, vrouter node info, etc
* List and display detail routing table from each vrouter node


## Pre-requisites

The following additional python modules are required. Depend on your Python 2.x version, they may not be installed by default. 

* requests
* argparse
* logging


## Example

#### Preparation

The script will read the following environment variable.  The example of the environment variables is shown below:

```
export OS_CONTRAIL_USERNAME='admin'
export OS_CONTRAIL_PASSWORD='mypasword'
export OS_CONTRAIL_TENANT_NAME='admin'
export OS_CONTRAIL_URL='http://10.200.155.33'

export OS_AUTH_URL="http://10.200.155.33:5000/v2.0"
export OS_USERNAME="admin"
export OS_PASSWORD="mypassword"
export OS_TENANT_NAME="admin"
```

The next update of the script may require additional env variable, please always check this README file. 

As common OpenStack operation, you can source your env variable before running this script, e.g:

```
# source openrc
# ./ocsc.py --help
```



#### OpenStack API

* Get the token 

    ```
    $ ./ocsc.py --get-token
    4f8a7fdee0a94928a8071c49ec5dcdf6
    ```

* List supported OpenStack API

    ```
    $ ./ocsc.py --list-support
    ```

* List all flavors

    ```
    $ ./ocsc.py --list flavors
    {
        "flavors": [
            {
                "id": "1",
                "links": [
                    {
                        "href": "http://10.200.155.33:8774/v1.1/8502bbacfeab4c70b830207c8a7753ef/flavors/1",
                        "rel": "self"
                    },
                    {
                        "href": "http://10.200.155.33:8774/8502bbacfeab4c70b830207c8a7753ef/flavors/1",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.tiny"
            },
            {
                "id": "56f8d692-abd1-4563-939f-8f646aac12e0",
                "links": [
                    {
                        "href": "http://10.200.155.33:8774/v1.1/8502bbacfeab4c70b830207c8a7753ef/flavors/56f8d692-abd1-4563-939f-8f646aac12e0",
                        "rel": "self"
                    },
                    {
                        "href": "http://10.200.155.33:8774/8502bbacfeab4c70b830207c8a7753ef/flavors/56f8d692-abd1-4563-939f-8f646aac12e0",
                        "rel": "bookmark"
                    }
                ],
                "name": "big.32g"
            },
        ... deleted..
    ```


* Show detail on specific flavor

    ```
    $ ./ocsc.py --show flavors --value 56f8d692-abd1-4563-939f-8f646aac12e0
    {
        "flavor": {
            "name": "big.32g",
            "links": [
                {
                    "href": "http://10.200.155.33:8774/v1.1/8502bbacfeab4c70b830207c8a7753ef/flavors/56f8d692-abd1-4563-939f-8f646aac12e0",
                    "rel": "self"
                },
                {
                    "href": "http://10.200.155.33:8774/8502bbacfeab4c70b830207c8a7753ef/flavors/56f8d692-abd1-4563-939f-8f646aac12e0",
                    "rel": "bookmark"
                }
            ],
            "ram": 32000,
            "OS-FLV-DISABLED:disabled": false,
            "vcpus": 4,
            "swap": "",
            "os-flavor-access:is_public": false,
            "rxtx_factor": 1.0,
            "OS-FLV-EXT-DATA:ephemeral": 0,
            "disk": 100,
            "id": "56f8d692-abd1-4563-939f-8f646aac12e0"
        }
    }
    ```


* List virtual-networks

    ```
    $ ./ocsc.py --list networks
    {
        "networks": [
            {
                "status": "ACTIVE",
                "router:external": false,
                "subnets": [
                    "83760d52-9c20-411d-811c-c803a6a06efb"
                ],
                "name": "net_dummy_104",
                "admin_state_up": true,
                "tenant_id": "8502bbacfeab4c70b830207c8a7753ef",
                "contrail:subnet_ipam": [
                    {
                        "subnet_cidr": "11.255.104.0/24",
                        "ipam_fq_name": [
                            "default-domain",
                            "default-project",
                            "default-network-ipam"
                        ]
                    }
                ],
                "shared": false,
                "contrail:instance_count": 0,
                "id": "84cd8888-419d-4d59-841b-c77c01113363",
                "contrail:fq_name": [
                    "default-domain",
                    "admin",
                    "net_dummy_104"
                ]
            },
        ...deleted...
    ```


* Find and show virtual-network based on the name

    ```
    $ ./ocsc.py --find networks --value net_159
    {
        "f2028ffd-5918-42e9-b7b9-e9557708ea57": {
            "network": {
                "status": "ACTIVE",
                "router:external": true,
                "subnets": [
                    "81b53511-e0c6-4d6e-87fb-e9ce571d366a",
                    "42eda272-49c6-43d7-8064-37225a1d5eb7"
                ],
                "name": "net_159",
                "admin_state_up": true,
                "tenant_id": "8502bbacfeab4c70b830207c8a7753ef",
                "contrail:subnet_ipam": [
                    {
                        "subnet_cidr": "10.200.158.0/24",
                        "ipam_fq_name": [
                            "default-domain",
                            "default-project",
                            "default-network-ipam"
                        ]
                    },
                    {
                        "subnet_cidr": "10.200.159.0/24",
                        "ipam_fq_name": [
                            "default-domain",
                            "default-project",
                            "default-network-ipam"
                        ]
                    }
                ],
                "shared": true,
                "contrail:policys": [
                    [
                        "default-domain",
                        "default-project",
                        "default-network-policy"
                    ]
                ],
                "contrail:instance_count": 0,
                "id": "f2028ffd-5918-42e9-b7b9-e9557708ea57",
                "contrail:fq_name": [
                    "default-domain",
                    "admin",
                    "net_159"
                ]
            }
        }
    }
    ```


* Access (GET) any REST API URL

    ```
    $ ./ocsc.py --get-url http://10.200.155.33:8774/8502bbacfeab4c70b830207c8a7753ef/flavors/4
    {
        "choices": [
            {
                "status": "CURRENT",
                "media-types": [
                    {
                        "base": "application/xml",
                        "type": "application/vnd.openstack.compute+xml;version=2"
                    },
                    {
                        "base": "application/json",
                        "type": "application/vnd.openstack.compute+json;version=2"
                    }
                ],
                "id": "v2.0",
                "links": [
                    {
                        "href": "http://10.200.155.33:8774/v2/8502bbacfeab4c70b830207c8a7753ef/flavors/4",
                        "rel": "self"
                    }
                ]
            }
        ]
    }
    ```




#### Contrail API

* List Contrail Resources

    ```
    $ ./ocsc.py --contrail-get-resource | less
    {
        "href": "http://10.200.155.33:8082",
        "links": [
            ..deleted..
            {
                "link": {
                    "href": "http://10.200.155.33:8082/domains",
                    "name": "domain",
                    "rel": "collection"
                }
            },
            {
                "link": {
                    "href": "http://10.200.155.33:8082/global-vrouter-configs",
                    "name": "global-vrouter-config",
                    "rel": "collection"
                }
            },
            {
                "link": {
                    "href": "http://10.200.155.33:8082/instance-ips",
                    "name": "instance-ip",
                    "rel": "collection"
                }
            },
            {
                "link": {
                    "href": "http://10.200.155.33:8082/network-policys",
                    "name": "network-policy",
                    "rel": "collection"
                }
            },
            ..deleted..
    ```


* List virtual-networks

    ```
    $ ./ocsc.py --contrail-list virtual-network | less
    {
        "virtual-networks": [
            {
                "href": "http://10.200.155.33:8082/virtual-network/84cd8888-419d-4d59-841b-c77c01113363",
                "fq_name": [
                    "default-domain",
                    "admin",
                    "net_dummy_104"
                ],
                "uuid": "84cd8888-419d-4d59-841b-c77c01113363"
            },
            {
                "href": "http://10.200.155.33:8082/virtual-network/af523e87-1bc4-48dc-9720-a9126db2208e",
                "fq_name": [
                    "default-domain",
                    "admin",
                    "launchTest1_net"
                ],
                "uuid": "af523e87-1bc4-48dc-9720-a9126db2208e"
            },
    ```

* Show specific virtual network by its uuid

    ```
    $ ./ocsc.py --contrail-show virtual-network --contrail-value 84cd8888-419d-4d59-841b-c77c01113363
    {
        "virtual-network": {
            "is_shared": false,
            "parent_href": "http://10.200.155.33:8082/project/8502bbac-feab-4c70-b830-207c8a7753ef",
            "display_name": "net_dummy_104",
            "virtual_network_network_id": 911,
            "router_external": false,
            "virtual_machine_interface_back_refs": [
                {
                    "to": [
                        "default-domain",
                        "admin",
                        "vmx104_fpc_port_7-ntg7arybm453"
                    ],
                    "href": "http://10.200.155.33:8082/virtual-machine-interface/0c172da2-6c05-4dab-8c2a-94b9d185cee5",
                    "attr": null,
                    "uuid": "0c172da2-6c05-4dab-8c2a-94b9d185cee5"
                },
                {
                    "to": [
                        "default-domain",
                        "admin",
                        "vmx104_fpc_port_8-inutsrdmbntx"
                    ],
                    "href": "http://10.200.155.33:8082/virtual-machine-interface/4313d250-8b0e-40a4-9e23-d0ac4dd31a94",
                    "attr": null,
                    "uuid": "4313d250-8b0e-40a4-9e23-d0ac4dd31a94"
                }
            ],
            "parent_type": "project",
            "uuid": "84cd8888-419d-4d59-841b-c77c01113363",
            "name": "net_dummy_104",
            "href": "http://10.200.155.33:8082/virtual-network/84cd8888-419d-4d59-841b-c77c01113363",
            "id_perms": {
                "enable": true,
                "uuid": {
                    "uuid_mslong": 9569454902029929817,
                    "uuid_lslong": 9519421572785451875
                },
                "created": "2016-08-16T14:07:21.330232",
                "description": null,
                "creator": null,
                "user_visible": true,
                "last_modified": "2016-08-16T14:07:41.759711",
                "permissions": {
                    "owner": "admin",
                    "owner_access": 7,
                    "other_access": 7,
                    "group": "KeystoneServiceAdmin",
                    "group_access": 7
                }
            },
            "instance_ip_back_refs": [
                {
                    "to": [
                        "00670925-5352-413d-8343-77d2260d7d64"
                    ],
                    "href": "http://10.200.155.33:8082/instance-ip/00670925-5352-413d-8343-77d2260d7d64",
                    "attr": null,
                    "uuid": "00670925-5352-413d-8343-77d2260d7d64"
                },
                {
                    "to": [
                        "49d9f22d-7fc4-47dc-81e4-b78ca1c61c4c"
                    ],
                    "href": "http://10.200.155.33:8082/instance-ip/49d9f22d-7fc4-47dc-81e4-b78ca1c61c4c",
                    "attr": null,
                    "uuid": "49d9f22d-7fc4-47dc-81e4-b78ca1c61c4c"
                }
            ],
            "fq_name": [
                "default-domain",
                "admin",
                "net_dummy_104"
            ],
            "routing_instances": [
                {
                    "to": [
                        "default-domain",
                        "admin",
                        "net_dummy_104",
                        "net_dummy_104"
                    ],
                    "href": "http://10.200.155.33:8082/routing-instance/1346314d-90c8-4d0b-816b-3e46e11bd62e",
                    "uuid": "1346314d-90c8-4d0b-816b-3e46e11bd62e"
                }
            ],
            "network_ipam_refs": [
                {
                    "to": [
                        "default-domain",
                        "default-project",
                        "default-network-ipam"
                    ],
                    "href": "http://10.200.155.33:8082/network-ipam/572de811-2598-41a6-8c5c-0ec576d4dd27",
                    "attr": {
                        "ipam_subnets": [
                            {
                                "subnet": {
                                    "ip_prefix": "11.255.104.0",
                                    "ip_prefix_len": 24
                                },
                                "addr_from_start": true,
                                "enable_dhcp": false,
                                "default_gateway": "11.255.104.1",
                                "dns_nameservers": [],
                                "dhcp_option_list": null,
                                "subnet_uuid": "83760d52-9c20-411d-811c-c803a6a06efb",
                                "allocation_pools": [],
                                "host_routes": null,
                                "dns_server_address": "11.255.104.2",
                                "subnet_name": "subnet_dummy_104-tsms6xliu4kz"
                            }
                        ],
                        "host_routes": null
                    },
                    "uuid": "572de811-2598-41a6-8c5c-0ec576d4dd27"
                }
            ],
            "parent_uuid": "8502bbac-feab-4c70-b830-207c8a7753ef"
        }
    }
    ```


* Find virtual-network by its name

    ```
    $ ./ocsc.py --contrail-find virtual-network --contrail-value net_dummy_104
    {
        "84cd8888-419d-4d59-841b-c77c01113363": {
            "virtual-network": {
                "is_shared": false,
                "parent_href": "http://10.200.155.33:8082/project/8502bbac-feab-4c70-b830-207c8a7753ef",
                "display_name": "net_dummy_104",
                "virtual_network_network_id": 911,
                "router_external": false,
                "virtual_machine_interface_back_refs": [
                    {
                        "to": [
                            "default-domain",
                            "admin",
                            "vmx104_fpc_port_7-ntg7arybm453"
                        ],
                        "href": "http://10.200.155.33:8082/virtual-machine-interface/0c172da2-6c05-4dab-8c2a-94b9d185cee5",
                        "attr": null,
                        "uuid": "0c172da2-6c05-4dab-8c2a-94b9d185cee5"
                    },
                    {
                        "to": [
        ...deleted.. 
    ```


* Get any URL, e.g, get the url for virtual network above

    ```
    $ ./ocsc.py --contrail-get-url http://10.200.155.33:8082/virtual-network/84cd8888-419d-4d59-841b-c77c01113363 | less
    {
        "virtual-network": {
            "is_shared": false,
            "parent_href": "http://10.200.155.33:8082/project/8502bbac-feab-4c70-b830-207c8a7753ef",
            "display_name": "net_dummy_104",
            "virtual_network_network_id": 911,
            "router_external": false,
            "virtual_machine_interface_back_refs": [
                {
                    "to": [
                        "default-domain",
                        "admin",
                        "vmx104_fpc_port_7-ntg7arybm453"
                    ],
                    "href": "http://10.200.155.33:8082/virtual-machine-interface/0c172da2-6c05-4dab-8c2a-94b9d185cee5",
                    "attr": null,
                    "uuid": "0c172da2-6c05-4dab-8c2a-94b9d185cee5"
                },
            ...deleted.. 
    ```

* Get Contrail token

    ```
    $ ./ocsc.py --contrail-get-token
    94e681c19959450ea96b375200ff354e
    ```



#### Contrail Analytic API

Similar as previous example, you can do any list (--contrail-analytic-list), find (--contrail-analytic-find), show (--contrail-analytic-show) operation. 

* List all vrouter

    ```
    $ ./ocsc.py --contrail-analytic-list vrouter | less
    [
        {
            "href": "http://10.200.155.33:8081/analytics/uves/vrouter/rungkut-ct1-compute6?flat",
            "name": "rungkut-ct1-compute6"
        },
        {
            "href": "http://10.200.155.33:8081/analytics/uves/vrouter/rungkut-ct1-compute7?flat",
            "name": "rungkut-ct1-compute7"
        },
        {
            "href": "http://10.200.155.33:8081/analytics/uves/vrouter/rungkut-ct1-compute5?flat",
            "name": "rungkut-ct1-compute5"
        },
    ...deleted..
    ```

* Show specific vrouter

    ```
    $ ./ocsc.py --contrail-analytic-show vrouter --contrail-value rungkut-ct1-compute6 | less
    {
        "NodeStatus": {
            "deleted": [
                [
                    {
                        "#text": "false",
                        "@type": "bool"
                    },
                    "rungkut-ct1-compute6:Compute:contrail-vrouter-nodemgr:0"
                ]
            ],
            "disk_usage_info": [
                [
                    {
                        "list": {
                            "DiskPartitionUsageStats": [
                                {
                                    "partition_space_available_1k": {
                                        "#text": "716995408",
                                        "@type": "u64"
                                    },
                                    "partition_space_used_1k": {
                                        "#text": "91986396",
                                        "@type": "u64"
                                    },
                                    "partition_name": {
                                        "#text": "/dev/sda1",
                                        "@type": "string"
                                    },
                                    "partition_type": {
                                        "#text": "ext4",
                                        "@type": "string"
                                    }
                                }
                            ],
                            "@type": "struct",
                            "@size": "1"
                        },

            ..deleted..

        "ComputeCpuState": {
            "cpu_info": {
                "@aggtype": "union",
                "list": {
                    "@type": "struct",
                    "@size": "1",
                    "VrouterCpuInfo": [
                        {
                            "mem_res": {
                                "#text": "122104",
                                "@type": "u32"
                            },
                            "mem_virt": {
                                "#text": "1396400",
                                "@type": "u32"
                            },
                            "cpu_share": {
                                "#text": "0.0982639",
                                "@type": "double"
                            },
                            "used_sys_mem": {
                                "#text": "40257028",
                                "@type": "u32"
                            },
                            "one_min_cpuload": {
                                "#text": "0.2525",
                                "@type": "double"
                            }
                        }
                    ]
                },
                "@type": "list",
                "@tags": ".mem_virt,.cpu_share,.mem_res"
            }
        }
    ```


* List virtual-machines, manually get the href URL and do get-url on it

    ```
    $ ./ocsc.py --contrail-analytic-list virtual-machine | less
    [
        {
            "href": "http://10.200.155.33:8081/analytics/uves/virtual-machine/c2ee8b62-dfb9-43c0-9569-5058a6614bc8?flat",
            "name": "c2ee8b62-dfb9-43c0-9569-5058a6614bc8"
        },
        {
            "href": "http://10.200.155.33:8081/analytics/uves/virtual-machine/4c17ca30-4917-456c-927a-4a4ecfedc382?flat",
            "name": "4c17ca30-4917-456c-927a-4a4ecfedc382"
        },

        ...deleted...




    $ ./ocsc.py --contrail-get-url http://10.200.155.33:8081/analytics/uves/virtual-machine/c2ee8b62-dfb9-43c0-9569-5058a6614bc8?flat | less
    {
        "VirtualMachineStats": {
            "cpu_stats": [
                {
                    "virt_memory": 9130800,
                    "cpu_one_min_avg": 12.8333,
                    "disk_used_bytes": 4294967295,
                    "vm_memory_quota": 4194304,
                    "peak_virt_memory": 9558892,
                    "disk_allocated_bytes": 4294967295,
                    "rss": 4235572
                }
            ]
        },
        "UveVirtualMachineAgent": {
            "vm_name": "linux001",
            "cpu_info": {
                "virt_memory": 9130800,
                "cpu_one_min_avg": 12.8333,
                "disk_used_bytes": 4294967295,
                "vm_memory_quota": 4194304,
                "peak_virt_memory": 9558892,
                "disk_allocated_bytes": 4294967295,
                "rss": 4235572
            },
            "interface_list": [
                "default-domain:admin:linux001_port_0-bvdld75lhitn",
                "default-domain:admin:linux001_port_1-nwbhpiqzpib4"
            ],
            "uuid": "c2ee8b62-dfb9-43c0-9569-5058a6614bc8",
            "vrouter": "rungkut-ct1-compute18"
        }
    }
    ```


## Contrail Sandesh API

* List all VRF on a compute node/vrouter node

    ```
    $ ./ocsc.py --contrail-vrouter-list-vrf --contrail-vrouter-host 10.200.155.34 --csv
    #VRF Name,ucindex,uc6index,mcindex,l2index,vxlan_id
    default-domain:admin:launchTest1-net_12:launchTest1-net_12,5,5,5,5,334
    default-domain:admin:launchTest1-net_24:launchTest1-net_24,6,6,6,6,311
    default-domain:admin:private2:private2,1,1,1,1,5
    ...deleted...
    ```

* Get all routing table of a specific VRF on a compute/vrouter node

    ```
    {
        "Inet4UcRoute": {
            "__Inet4UcRouteResp_list": {
                "@type": "slist",
                "Inet4UcRouteResp": [
                    {
                        "@type": "sandesh",
                        "route_list": {
                            "@type": "list",
                            "@identifier": "1",
                            "list": {
                                "@type": "struct",
                                "@size": "100",
                                "RouteUcSandeshData": [
                                    {
                                        "src_ip": {
                                            "@type": "string",
                                            "@identifier": "1",
                                            "#text": "0.0.0.0"

                                            ...deleted...


                                    {
                                        "src_ip": {
                                            "@type": "string",
                                            "@identifier": "1",
                                            "#text": "172.19.2.10"
                                        },
                                        "src_plen": {
                                            "@type": "i32",
                                            "@identifier": "2",
                                            "#text": "32"
                                        },
                                        "src_vrf": {
                                            "@type": "string",
                                            "@identifier": "3",
                                            "@link": "VrfListReq",
                                            "#text": "default-domain:admin:private2:private2"
                                        },
                                        "path_list": {
                                            "@type": "list",
                                            "@identifier": "4",
                                            "list": {
                                                "@type": "struct",
                                                "@size": "2",
                                                "PathSandeshData": [
                                                    {
                                                        "nh": {
                                                            "@type": "struct",
                                                            "@identifier": "1",
                                                            "NhSandeshData": {
                                                                "type": {
                                                                    "@type": "string",
                                                                    "@identifier": "1",
                                                                    "#text": "tunnel"
                                                                },
                                                                "ref_count": {
                                                                    "@type": "i32",
                                                                    "@identifier": "2",
                                                                    "#text": "277"
                                                                },
                                                                "valid": {
                                                                    "@type": "string",
                                                                    "@identifier": "3",
                                                                    "#text": "true"
                                                                },
                                                                "policy": {
                                                                    "@type": "string",
                                                                    "@identifier": "4",
                                                                    "#text": "disabled"
                                                                },
                                                                "sip": {
                                                                    "@type": "string",
                                                                    "@identifier": "5",
                                                                    "#text": "10.200.155.34"
                                                                },
                                                                "dip": {
                                                                    "@type": "string",
                                                                    "@identifier": "6",
                                                                    "#text": "10.200.155.35"
                                                                },
                                                                "vrf": {
                                                                    "@type": "string",
                                                                    "@identifier": "7",
                                                                    "@link": "VrfListReq",
                                                                    "#text": "default-domain:default-project:ip-fabric:__default__"
                                                                },
                                                                "mac": {
                                                                    "@type": "string",
                                                                    "@identifier": "9",
                                                                    "#text": "c:c4:7a:57:e:40"
                                                                },
                                                                "tunnel_type": {
                                                                    "@type": "string",
                                                                    "@identifier": "16",
                                                                    "#text": "MPLSoGRE"
                                                                },
                                                                "nh_index": {
                                                                    "@type": "i32",
                                                                    "@identifier": "21",
                                                                    "#text": "42"
                                                                },
                                                                "vxlan_flag": {
                                                                    "@type": "bool",
                                                                    "@identifier": "24",
                                                                    "#text": "false"
                                                                }
                                                            }
                                                        },
                                                        "label": {
                                                            "@type": "i32",
                                                            "@identifier": "2",
                                                            "#text": "108"
                                                        },
                                                        "vxlan_id": {
                                                            "@type": "i32",
                                                            "@identifier": "3",
                                                            "#text": "0"
                                                        },
                                                        "peer": {
                                                            "@type": "string",
                                                            "@identifier": "4",
                                                            "#text": "10.200.155.33"
                                                        },
                                                        "dest_vn": {
                                                            "@type": "string",
                                                            "@identifier": "5",
                                                            "@link": "VnListReq",
                                                            "#text": "default-domain:admin:private2"
                                                        },
                                                        "unresolved": {
                                                            "@type": "string",
                                                            "@identifier": "6",
                                                            "#text": "false"
                                                        },
                                                        "sg_list": {
                                                            "@type": "list",
                                                            "@identifier": "10",
                                                            "list": {
                                                                "@type": "i32",
                                                                "@size": "1",
                                                                "element": "8000001"
                                                            }
                                                        },
                                                        "supported_tunnel_type": {
                                                            "@type": "string",
                                                            "@identifier": "11",
                                                            "#text": "MPLSoGRE MPLSoUDP"
                                                        },
                                                        "active_tunnel_type": {
                                                            "@type": "string",
                                                            "@identifier": "12",
                                                            "#text": "MPLSoGRE"
                                                        },
                                                        "stale": {
                                                            "@type": "bool",
                                                            "@identifier": "13",
                                                            "#text": "false"
                                                        },
                                                        "path_preference_data": {
                                                            "@type": "struct",
                                                            "@identifier": "14",
                                                            "PathPreferenceSandeshData": {
                                                                "sequence": {
                                                                    "@type": "i32",
                                                                    "@identifier": "1",
                                                                    "#text": "0"
                                                                },
                                                                "preference": {
                                                                    "@type": "i32",
                                                                    "@identifier": "2",
                                                                    "#text": "100"
                                                                },
                                                                "ecmp": {
                                                                    "@type": "bool",
                                                                    "@identifier": "3",
                                                                    "#text": "false"
                                                                },

                                                    ...deleted...
    ```


## To Do

* add create/modify/delete functionality, especially for Nova, virtual-network, and subnet.
* add glance image upload/download functionality
* automatic crawler/data correlation between multiple resource objects



## Help Needed

If anyone has information how to query every vrouter routing table from central Contrail controller instead of going to each vrouter introspect port, please let me know. Thanks!!!



