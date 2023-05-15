#!/usr/bin/env python

from requests import Response, Session

## See examples here:
## https://github.com/MikeWooster/api-client

# from apiclient import APIClient

from apiclient import (
    APIClient,
    HeaderAuthentication,
)

# from apiclient.request_formatters import BaseRequestFormatter, NoOpRequestFormatter
# from apiclient.response_handlers import BaseResponseHandler, RequestsResponseHandler

class MyClient(APIClient):

    def __init__(
        self,
        config_filename: Optional[str] = None,
        requests_session: Session = Session(),
    ):

        self.session = requests_session

        if config_filename:
            self.config = self.load_config(config_filename)

    def list_customers(self):
        url = "http://example.com/customers"
        return self.get(url)

    def load_config(self, filename: str) -> PFSenseConfig:
        """Loads the config from the specified JSON file (see the `PFSenseConfig` class for what fields are required)"""
        self.config_filename = Path(os.path.expanduser(filename))
        if not self.config_filename.exists():
            error = f"Filename {self.config_filename.as_posix()} does not exist."
            raise FileNotFoundError(error)
        with self.config_filename.open(encoding="utf8") as file_handle:
            pydantic_config = PFSenseConfig(
                **json.load(file_handle)
            )
        self.config = pydantic_config
        # self.hostname = pydantic_config.hostname
        # self.port = pydantic_config.port
        # self.mode = pydantic_config.mode or "local"

        return pydantic_config


client = APIClient(
    authentication_method=HeaderAuthentication(token="secret"),
    response_handler=BaseResponseHandler,
    request_formatter=BaseRequestFormatter,
)
assert client.get_default_query_params() == {}
assert client.get_default_headers() == {"Authorization": "Bearer secret"}
assert client.get_default_username_password_authentication() is None
