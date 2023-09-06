# This file is part of concourse-lp-livefs-resource
#
# Copyright 2023 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Tuple
from launchpadlib.credentials import (
    Credentials,
    CredentialStore,
    AccessToken,
    RequestTokenAuthorizationEngine,
)
from launchpadlib.launchpad import Launchpad, Consumer
from requests.auth import AuthBase

from requests_oauthlib import OAuth1


class DummyCredentialStore(CredentialStore):
    """This class provides oauth token and secret store"""

    def __init__(self, consumer_name, oauth_token, oauth_token_secret):
        super(DummyCredentialStore, self).__init__(credential_save_failed=None)
        self.credentials = Credentials()
        self.credentials.consumer = Consumer(consumer_name)
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
        consumer_name,
        application_name=None,
        allow_access_levels=None,
    ):
        super(DummyAuthorizationEngine, self).__init__(
            service_root, application_name, consumer_name, allow_access_levels
        )


def login_with_oauth(
    consumer_name, oauth_token, oauth_token_secret, service_root="production"
) -> Tuple[Launchpad, AuthBase]:
    """This function provides launchpadlib Launchpad instance with existing
    OAuth token and secret passed from elsewhere."""
    credstore = DummyCredentialStore(consumer_name, oauth_token, oauth_token_secret)
    authengine = DummyAuthorizationEngine(service_root, consumer_name)
    lp = Launchpad.login_with(
        consumer_name,
        service_root,
        version="devel",
        credential_store=credstore,
        authorization_engine=authengine,
    )
    auth = OAuth1(consumer_name, "", oauth_token, oauth_token_secret)
    return lp, auth
