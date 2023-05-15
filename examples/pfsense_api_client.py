#!/usr/bin/env python

import os
from loguru import logger
from pathlib import Path
from requests import Response, Session
# from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional

# See examples here:
# https://github.com/MikeWooster/api-client
# ref: https://github.com/MikeWooster/api-client/blob/master/README.md#extended-example

# from apiclient import APIClient
from apiclient import (
    APIClient,
    HeaderAuthentication,
    JsonResponseHandler,
    JsonRequestFormatter,
)
from apiclient.exceptions import APIClientError


# from apiclient.request_formatters import BaseRequestFormatter, NoOpRequestFormatter
# from apiclient.response_handlers import BaseResponseHandler, RequestsResponseHandler

class PFSenseConfig(BaseModel):
    """This defines the expected config file

        Example config file:
    ```json
    {
            "username" : "me",
            "password" : "mysupersecretpassword",
            "hostname" : "example.com",
            "port" : 8443,
    }
    ```
    """

    username: Optional[str]
    password: Optional[str]
    port: int = 443
    hostname: str
    mode: str = "local"
    jwt: Optional[str]
    client_id: Optional[str]
    client_token: Optional[str]


class APIResponse(BaseModel):
    """standard JSON API response from the pFsense API"""

    status: str
    code: int
    return_code: int = Field(
        ..., title="return", alias="return", description="The return field from the API"
    )
    message: str
    data: Any

    @validator("code")
    def validate_code(cls, value: int) -> int:
        """validates it's an integer in the expected list"""
        if value not in [200, 400, 401, 403, 404, 500]:
            raise ValueError(f"Got an invalid status code ({value}).")
        return value




class PFSenseAPIClient:
    """ Base """

    def __init__(
        self,
        config_filename: Optional[str] = None,
        requests_session: Session = None
    ):

        if config_filename:
            self.config = self.load_config(config_filename)

        self.api_client = APIClient(
            authentication_method=HeaderAuthentication(token=f"{self.config.client_id} {self.config.client_token}"),
            response_handler=JsonResponseHandler,
            request_formatter=JsonRequestFormatter,
        )
        if requests_session:
            self.session = requests_session
            self.api_client.set_session(requests_session)

    @property
    def baseurl(self) -> str:
        """ returns the base URL of the host """
        retval = f"https://{self.config.hostname}"
        if self.config.port:
            retval += f":{self.config.port}"
        return retval

    def load_config(self, filename: str) -> PFSenseConfig:
        """Loads the config from the specified JSON file (see the `PFSenseConfig` class for what fields are required)"""
        self.config_filename = Path(os.path.expanduser(filename))
        if not self.config_filename.exists():
            error = f"Filename {self.config_filename.as_posix()} does not exist."
            raise FileNotFoundError(error)
        with self.config_filename.open(encoding="utf8") as file_handle:
            pfsense_config = PFSenseConfig(
                **json.load(file_handle)
            )
        self.config = pfsense_config
        # self.hostname = pfsense_config.hostname
        # self.port = pfsense_config.port
        # self.mode = pfsense_config.mode or "local"

        return pfsense_config


    def get_dhcpd_leases(self):
        url = f"{self.baseurl}/api/v1/services/dhcpd/lease"
        return self.api_client.get(url)

    # def get_dhcpd_leases(self):
    #     url = "/api/v1/services/dhcpd/lease"
    #     response = self.call(url, method, payload)
    #     # return self.call_api_dict(url, payload=filterargs)


def get_client() -> PFSenseAPIClient:
    """ client factory """
    logger.remove()
    logger.add(format=LOGGER_FORMAT, sink=sys.stdout)
    session = requests.Session()
    session.verify = False
    client = PFSenseAPIClient(
        config_filename="~/.config/pfsense-api.json",
        requests_session=session
        )
    return client

@click.group()
def cli():
    """ DHCP CLI for pFsense """

@cli.command()
@click.option("--find", "-f", help="Does a wildcard match based on this")
@click.option("--expired", "-e", is_flag=True, default=False, help="Includes expired leases, off by default.")
@click.option("--debug", "-d", is_flag=True, default=False, help="Debug mode, dump more data.")
def list_leases(
    find: Optional[str]=None,
    expired: bool=False,
    debug: bool=False,
    ) -> None:
    """ lists DHCP leases """
    client = get_client()
    lease_info = client.get_dhcpd_leases()

    lease_data: List[Dict[str, str]] = lease_info.data

    for lease in lease_data:
        if find is not None:
            if find not in str(lease.values()):
                continue
        if not expired and lease['state'] == "expired":
            continue
        lease_message = f"{lease['type']}\t{lease['mac']}\t{lease['ip']}\t{lease.get('hostname', '')}"
        if "descr" in lease and lease["descr"]:
            lease_message += f" ({lease['descr']})"
        if not lease["online"]:
            logger.debug(lease_message)
        else:
            logger.info(lease_message)
        if debug:
            logger.debug(lease)


if __name__ == '__main__':
    cli()
