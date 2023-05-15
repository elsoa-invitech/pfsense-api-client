

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
    "client_id": "61623346e",
    "client_token": "605a69fbee4e8d3cc6cb5068386e11e8",
    "mode": "api_token",
    "hostname": "pfsense.johnson.int"
}
```

