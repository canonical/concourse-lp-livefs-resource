from typing import Tuple
from launchpadlib.credentials import (
    Credentials,
    CredentialStore,
    AccessToken,
    RequestTokenAuthorizationEngine,
)
from launchpadlib.launchpad import Launchpad, SystemWideConsumer
from requests.auth import AuthBase

from requests_oauthlib import OAuth1


class DummyCredentialStore(CredentialStore):
    """This class provides oauth token and secret store"""

    def __init__(self, oauth_token, oauth_token_secret, consumer_name="dummy"):
        super(DummyCredentialStore, self).__init__(credential_save_failed=None)
        self.credentials = Credentials()
        self.credentials.consumer = SystemWideConsumer(consumer_name)
        self.credentials.access_token = AccessToken.from_params(
            {"oauth_token": oauth_token, "oauth_token_secret": oauth_token_secret}
        )

    def do_load(self, unique_key):
        return self.credentials


class DummyAuthorizationEngine(RequestTokenAuthorizationEngine):
    """This stub class prevents launchpadlib from nulling out consumer_name
    in its demented campaign to force the use of desktop integration.

    This was called ShutUpAndTakeMyTokenAuthorizationEngine"""

    def __init__(
        self,
        service_root,
        application_name=None,
        consumer_name="dummy",
        allow_access_levels=None,
    ):
        super(DummyAuthorizationEngine, self).__init__(
            service_root, application_name, consumer_name, allow_access_levels
        )


def login_with_oauth(
    oauth_token, oauth_token_secret, consumer_name="dummy", service_root="production"
) -> Tuple[Launchpad, AuthBase]:
    """This function provides launchpadlib Launchpad instance with existing
    OAuth token and secret passed from elsewhere."""
    credstore = DummyCredentialStore(oauth_token, oauth_token_secret)
    authengine = DummyAuthorizationEngine(service_root="production")
    lp = Launchpad.login_with(
        consumer_name,
        "production",
        version="devel",
        credential_store=credstore,
        authorization_engine=authengine,
    )
    auth = OAuth1(consumer_name, "", oauth_token, oauth_token_secret)
    return lp, auth
