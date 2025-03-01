# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: identity_sample_async.py
DESCRIPTION:
    These async samples demonstrate creating a user, issuing a token, revoking a token and deleting a user.

USAGE:
    python identity_samples_async.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_COMMUNICATION_SERVICE_ENDPOINT - Communication Service endpoint url
    2) COMMUNICATION_SAMPLES_CONNECTION_STRING - the connection string in your Communication Services resource
    3) AZURE_CLIENT_ID - the client ID of your active directory application
    4) AZURE_CLIENT_SECRET - the secret of your active directory application
    5) AZURE_TENANT_ID - the tenant ID of your active directory application
    6) COMMUNICATION_M365_APP_ID - the application id of M365
    7) COMMUNICATION_M365_AAD_AUTHORITY - the AAD authority of M365 
    8) COMMUNICATION_M365_AAD_TENANT - the tenant ID of M365 application
    9) COMMUNICATION_M365_SCOPE - the scope of M365 application
    10) COMMUNICATION_MSAL_USERNAME - the username for authenticating via the MSAL library
    11) COMMUNICATION_MSAL_PASSWORD - the password for authenticating via the MSAL library 
"""
from azure.communication.identity._shared.utils import parse_connection_str
from msal import PublicClientApplication
import asyncio
import os


class CommunicationIdentityClientSamples(object):

    def __init__(self):
        self.connection_string = os.getenv('COMMUNICATION_SAMPLES_CONNECTION_STRING')
        self.endpoint = os.getenv('AZURE_COMMUNICATION_SERVICE_ENDPOINT')
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.m365_app_id = os.getenv('COMMUNICATION_M365_APP_ID') 
        self.m365_aad_authority = os.getenv('COMMUNICATION_M365_AAD_AUTHORITY') 
        self.m365_aad_tenant = os.getenv('COMMUNICATION_M365_AAD_TENANT')
        self.m365_scope = os.getenv('COMMUNICATION_M365_SCOPE') 
        self.msal_username = os.getenv('COMMUNICATION_MSAL_USERNAME') 
        self.msal_password = os.getenv('COMMUNICATION_MSAL_PASSWORD')

    async def get_token(self):
        from azure.communication.identity.aio import CommunicationIdentityClient
        from azure.communication.identity import CommunicationTokenScope
        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity.aio import DefaultAzureCredential
            endpoint, _ = parse_connection_str(self.connection_string)
            identity_client = CommunicationIdentityClient(endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

        async with identity_client:
            user = await identity_client.create_user()
            print("Issuing token for: " + user.properties.get('id'))
            tokenresponse = await identity_client.get_token(user, scopes=[CommunicationTokenScope.CHAT])
            print("Token issued with value: " + tokenresponse.token)

    async def revoke_tokens(self):
        from azure.communication.identity.aio import CommunicationIdentityClient
        from azure.communication.identity import CommunicationTokenScope
        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity.aio import DefaultAzureCredential
            endpoint, _ = parse_connection_str(self.connection_string)
            identity_client = CommunicationIdentityClient(endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

        async with identity_client:
            user = await identity_client.create_user()
            tokenresponse = await identity_client.get_token(user, scopes=[CommunicationTokenScope.CHAT])
            print("Revoking token: " + tokenresponse.token)
            await identity_client.revoke_tokens(user)
            print(tokenresponse.token + " revoked successfully")

    async def create_user(self):
        from azure.communication.identity.aio import CommunicationIdentityClient
        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity.aio import DefaultAzureCredential
            endpoint, _ = parse_connection_str(self.connection_string)
            identity_client = CommunicationIdentityClient(endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

        async with identity_client:
            print("Creating new user")
            user = await identity_client.create_user()
            print("User created with id:" + user.properties.get('id'))

    async def create_user_and_token(self):
        from azure.communication.identity.aio import CommunicationIdentityClient
        from azure.communication.identity import CommunicationTokenScope
        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity.aio import DefaultAzureCredential
            endpoint, _ = parse_connection_str(self.connection_string)
            identity_client = CommunicationIdentityClient(endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

        async with identity_client:
            print("Creating new user with token")
            user, tokenresponse = await identity_client.create_user_and_token(scopes=[CommunicationTokenScope.CHAT])
            print("User created with id:" + user.properties.get('id'))
            print("Token issued with value: " + tokenresponse.token)

    async def delete_user(self):
        from azure.communication.identity.aio import CommunicationIdentityClient
        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity.aio import DefaultAzureCredential
            endpoint, _ = parse_connection_str(self.connection_string)
            identity_client = CommunicationIdentityClient(endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

        async with identity_client:
            user = await identity_client.create_user()
            print("Deleting user: " + user.properties.get('id'))
            await identity_client.delete_user(user)
            print(user.properties.get('id') + " deleted")

    async def get_token_for_teams_user(self):
        from azure.communication.identity.aio import CommunicationIdentityClient
        if self.client_id is not None and self.client_secret is not None and self.tenant_id is not None:
            from azure.identity.aio import DefaultAzureCredential
            endpoint, _ = parse_connection_str(self.connection_string)
            identity_client = CommunicationIdentityClient(endpoint, DefaultAzureCredential())
        else:
            identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

        async with identity_client:    
            msal_app = PublicClientApplication(client_id=self.m365_app_id, authority="{}/{}".format(self.m365_aad_authority, self.m365_aad_tenant))
            result = msal_app.acquire_token_by_username_password(
                username=self.msal_username,
                password=self.msal_password,
                scopes=[self.m365_scope])
            add_token =  result["access_token"]
            print("AAD access token of a Teams User: " + add_token)

            print("AAD access token of a Teams User: " + add_token)
            tokenresponse = await identity_client.get_token_for_teams_user(add_token)
            print("Token issued with value: " + tokenresponse.token)

async def main():
    sample = CommunicationIdentityClientSamples()
    await sample.create_user()
    await sample.create_user_and_token()
    await sample.get_token()
    await sample.revoke_tokens()
    await sample.delete_user()
    await sample.get_token_for_teams_user()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
