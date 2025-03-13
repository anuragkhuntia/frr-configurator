# this script is for fetching and creating BGP PEER GROUP configuration

import requests
import json
import csv
import os
import sys
import logging

sys.path.append("../../../")
from common.readCsv import get_ip_for_hostname, read_json_for_hostname

# Configure logging
logging.basicConfig(
    format='{"timestamp":"%(asctime)s","log_level":"%(levelname)s","message":"%(message)s","app":"%(name)s"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
)

logger = logging.getLogger("BgpPeergroup")


class BgpPeergroup:
    def __init__(self, username, password):
        # Initializing credentials
        self.username = username
        self.password = password

    def get_config(self, host):
        # GET request to fetch the configuration
        try:
            current_path = os.getcwd()
            logger.info(f"Current working directory: {current_path}")

            ip = get_ip_for_hostname(host)
            if not ip:
                logger.error(f"Failed to retrieve IP for hostname {host}")
                return

            url = f'https://{ip}/restconf/data/sonic-bgp-peergroup:sonic-bgp-peergroup'
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

            url = f'https://{ip}/restconf/data/sonic-bgp-peergroup:sonic-bgp-peergroup'
            json_data = read_json_for_hostname(host, 'bgpPeer')

            if not json_data:
                logger.error(f"Error: No JSON configuration found for {host}")
                return

            headers = {'Content-Type': 'application/yang-data+json'}

            logger.info(f"Sending PUT request to {url} with data: {json_data}")

            response = requests.post(
                url, auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                headers=headers, data=json.dumps(json_data), verify=False
            )

            if response.status_code == 200:
                logger.info("PUT request successful", extra={"response": response.text})
            else:
                logger.error(
                    f"Failed POST request with status code {response.status_code}",
                    extra={"response": response.text}
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")


def main():
    logger.info("Starting BGP Peergroup configuration script")

    # Create an instance of the BgpPeergroup class
    bgp_config = BgpPeergroup(username='admin', password='npci@123')

    # Call GET method to fetch the configuration
    bgp_config.get_config('edge_leaf1')