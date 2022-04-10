"""DNS Authenticator for Dynu."""
import logging
from typing import Any
from typing import Callable
from typing import Optional

from lexicon.providers import dynu
from requests import HTTPError

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Dynu."""

    description = 'Obtain certificates using a DNS TXT record ' + \
                  '(if you are using Dynu for DNS.)'

    ttl = 60

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None],
                             default_propagation_seconds: int = 10) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="Dynu credentials file.")

    def more_info(self) -> str:
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'Dynu API'

    def _setup_credentials(self):
        self._configure_file('credentials',
                             'Absolute path to Dynu credentials file')
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            'credentials',
            'Dynu credentials file INI file',
            {
                'auth-token': 'Dynu-compatible API key (API-Key)',
            }
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_dynu_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_dynu_client().del_txt_record(domain, validation_name, validation)

    def _get_dynu_client(self) -> "_DynuLexiconClient":
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _DynuLexiconClient(
            self.credentials.conf('auth-token'),
            self.ttl
        )


class _DynuLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Dynu via Lexicon.
    """

    def __init__(self, auth_token: str, ttl: int) -> None:
        super().__init__()

        config = dns_common_lexicon.build_lexicon_config('dynu', {
            'ttl': ttl,
        }, {
            'auth_token': auth_token,
        })

        self.provider = dynu.Provider(config)

    def _handle_http_error(self, e: HTTPError, domain_name: str) -> Optional[errors.PluginError]:
        if domain_name in str(e) and (
            # 4.0 and 4.1 compatibility
            str(e).startswith('422 Client Error: Unprocessable Entity for url:') or
            # 4.2
            str(e).startswith('404 Client Error: Not Found for url:')
        ):
            return None  # Expected errors when zone name guess is wrong

        return super()._handle_http_error(e, domain_name)

