# Thofer@juniper.net 
# usage examples
# with "python hierachy.py <site1> <site2>" it takes the hierachy from <site1> and copies it into <site2>
# with "python hierachy.py <site>" prints the hierachy from site



import json
import requests
import sys
import yaml
from pprint import pprint


def get_hierachy(config) -> list:
    """
       https://10.10.0.88/api/config/network_hierarchy/networks
    """

    api_url = f"{config['api_url']}/config/network_hierarchy/networks"
    headers = {"content-type": "application/json",
               "SEC": f"{config['token']}"}
    
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200:
        print("\nRetrieved Network Hierachy from Src JSA Successfully\n")
        return json.loads(response.text)
    else:
        print(
            f"Something went wrong: {response.status_code} - {response.reason}")
    return None


def post_hierachy(hierachy_ld, config):
    'https://10.11.0.88/api/config/network_hierarchy/staged_networks'

    api_url = f"{config['api_url']}/config/network_hierarchy/staged_networks"
    headers = {"content-type": "application/json",
               "SEC": f"{config['token']}"}

    response = requests.put(api_url, headers=headers, verify=False,  data=json.dumps(hierachy_ld))
    if response.status_code == 200:
        print("\nNetwork Hierachy Copied to dst JSA\n")
        return json.loads(response.text)
    else:
        print(
            f"Something went wrong: {response.status_code} - {response.reason}")
    return None


def get_json_file(filename: str) -> dict:
    with open(filename) as f:
        json_d = json.load(f)
    json_d = json_d[select_site_first.upper()]
    return json_d


def get_yml_file(filename: str, select_site) -> dict:
    with open(filename) as f:
        json_d = yaml.safe_load(f)
    json_d = json_d[select_site.upper()]
    return json_d


if __name__ == "__main__":
    mode = ""
    if len(sys.argv) < 2:
        print("use Hierachy <site_src> <site_dst> - as defined in config.yml file\n")
        print("use Hierachy <site> - for getting the hierachy only")
        sys.exit()
    if len(sys.argv) == 3:
        mode = "copy"
    if len(sys.argv) == 2:
        mode = "config"   
    select_site_first = sys.argv[1]
    # just tried both json and yml
    #config = get_json_file("config.json")
    config_first = get_yml_file("config.yml", select_site_first)
    hierachy_ld = get_hierachy(config_first)
    if mode == "copy":
        select_site_second = sys.argv[2]
        config_second = get_yml_file("config.yml", select_site_second)
        post_hierachy(hierachy_ld, config_second) 
    if mode == "config":
        output_file = "JSA_Hierachy.txt"
        with open(output_file, "w") as file:
            print(f"config is in file: {output_file}")
            for text in hierachy_ld:
                file.write(f"{text}\n")