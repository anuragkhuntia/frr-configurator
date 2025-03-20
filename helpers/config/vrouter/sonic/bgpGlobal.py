# this script is for reading and creating BGP GLOBAL configuration

import json
import csv
import os
import sys
import requests
import logging

sys.path.append("../../../")
from common.readCsv import get_ip_for_hostname, read_json_for_hostname

# Configure logging
logging.basicConfig(
    format='{"timestamp":"%(asctime)s","log_level":"%(levelname)s","message":"%(message)s","app":"%(name)s"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
)

logger = logging.getLogger("BgpGlobal")


class BgpGlobal:
    def __init__(self, username, password):
        # Initializing credentials
        self.username = username
        self.password = password

    def get_config(self, host):
        # GET request to fetch the configuration
        try:
            ip = get_ip_for_hostname(host)
            if not ip:
                logger.error(f"Failed to retrieve IP for hostname {host}")
                return

            url = f'https://{ip}/restconf/data/sonic-bgp-global:sonic-bgp-global'
            response = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.username, self.password), verify=False)

            # Check for successful response
            if response.status_code == 200:
                logger.info("GET request successful", extra={"response": response.text})
                return response.text
            else:
                logger.error(
                    f"Failed GET request with status code {response.status_code}",
                    extra={"response": response.text}
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")

    def post_config(self, host):
        # POST request to update the configuration
        try:
            ip = get_ip_for_hostname(host)
            if not ip:
                logger.error(f"Error: No IP found for hostname {host}")
                return

            url = f'https://{ip}/restconf/data/sonic-bgp-global:sonic-bgp-global'
            json_data = read_json_for_hostname(host, 'bgpGlobal')

            if not json_data:
                logger.error(f"Error: No JSON configuration found for {host}")
                return

            headers = {'Content-Type': 'application/yang-data+json'}

            logger.info(f"Sending POST request to {url} with data: {json.dumps(json_data, indent=2)}")

            response = requests.post(
                url, auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                headers=headers, data=json.dumps(json_data), verify=False
            )

            if response.status_code == 200:
                logger.info("POST request successful", extra={"response": response.text})
            else:
                logger.error(
                    f"Failed POST request with status code {response.status_code}",
                    extra={"response": response.text}
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")


def main():
    logger.info("Starting BGP Global configuration script")

    # Create an instance of the BgpGlobal class
    bgp_global = BgpGlobal(username='env.user', password='env.pass

    bgp_global.get_config('edge_leaf1')


if __name__ == "__main__":
    main()
