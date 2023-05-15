

## Install dependencies

```shell
pip install -r ../requirements.txt
```

## Setup symbolic link if using local package source code

To use local package source code:

```shell
ln -s ../pfsense_api_client
```

## Setup config

Setup local client/auth config:

```shell
$ cat ~/.config/pfsense-api.json
{
    "client_id": "41123346e",
    "client_token": "605a69fbee4e8d3cc6cb5068386e11e8",
    "mode": "api_token",
    "hostname": "pfsense.johnson.int"
}
```

## Run simple query

```shell
$ python dhcp.py list-leases
static	00:0c:29:30:79:21	10.12.20.20	vcenter
static	00:25:90:bd:c6:b4	10.10.0.10	esx00
static	00:25:90:bb:54:4a	10.11.1.10	esx01
static	00:25:90:bb:54:c7	10.12.1.10	esx02
static	00:25:90:bb:54:c6	10.12.0.10	esx02
static	f4:4d:30:6e:4c:ca	10.10.10.10	esx10
static	00:50:56:81:93:2f	10.11.1.15	cyberpower-rack
static	00:50:56:81:c0:9c	10.10.10.15	cyberpower-esx10
...
static	00:0c:29:4f:7c:47	10.11.20.30	vcenter7
static	00:50:56:b7:f6:53	10.10.2.10	vcontrol01
static	00:50:56:8d:76:48	10.0.20.36	win2019-01
```

