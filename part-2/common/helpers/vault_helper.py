from dotenv import load_dotenv
import requests
import os

load_dotenv()

class VaultHelper:
    """
    A helper class for interacting with Hashicorp's Vault.

    This class provides methods for retrieving secrets from Vault.
    """

    def __init__(self):
        load_dotenv()
        self._vault_address = os.getenv('VAULT_ADDR')
        self._vault_role_id = os.getenv('VAULT_ROLE_ID')
        self._vault_secret_id = os.getenv('VAULT_SECRET_ID')
        self._client_token = self.__get_client_token()

    def __get_client_token(self):
        """
        Get the client token for Vault.

        :return: str
        """
        resp = requests.post(
            url=f'{self._vault_address}/v1/auth/approle/login',
            json={
                "role_id": self._vault_role_id,
                "secret_id": self._vault_secret_id
            }
        )

        json_data = resp.json()
        return json_data['auth']["client_token"]

    def __get_secrets(self, secret_path):
        """
        Get the secrets from Vault.

        :param secret_path: str
        :return: dict
        """
        resp = requests.get(
            url=f'{self._vault_address}/v1/secrets/data/{secret_path}',
            headers={
                "X-Vault-Token": self._client_token
            }
        )

        json_data = resp.json()
        return json_data['data']['data']

    def get_api_key(self, alias):
        """
        Get the API key from Vault.

        :param alias: str
        :return: str
        """
        return self.__get_secrets(secret_path='apiKeys')[alias]

    def get_rabbitmq_credentials(self):
        """
        Get the RabbitMQ credentials from Vault.

        :return: dict
        """
        return self.__get_secrets(secret_path='rabbitmq')


def main():
    vault_helper = VaultHelper()
    print(vault_helper.get_api_key('weather-api-key'))

if __name__ == '__main__':
    main()
