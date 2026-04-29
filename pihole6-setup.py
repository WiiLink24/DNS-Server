if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(
            prog='python3 pihole6-setup.py',
            description='Adds the current pihole list to your Pi-hole v6 server\'s DNS config via the server API.')
    parser.add_argument("server", help="URL to the server.")

    args = parser.parse_args()

    import getpass

    cur_pass = getpass.getpass('PiHole Password, used for API authentication: ')

    import requests
    import json
    
    url = args.server + "/api"
    payload = {'password': cur_pass}
    
    del cur_pass

    # get api key
    response = requests.request("POST", url + "/auth", json=payload, verify=False)

    auth_json = ""
    sid = ""
    csrf = ""

    try:
        auth_json = json.loads(response.text)
        sid = auth_json["session"]["sid"]
        csrf = auth_json["session"]["csrf"]
    except Exception as e:
        print("Error parsing json, exiting.")
        print(e)
        exit()

    print("Authentication complete.")
    
    # get hosts from url, and if not url, file.
    try:
        r = requests.get("https://raw.githubusercontent.com/WiiLink24/DNS-Server/master/dns_zones-hosts.txt")
        with open("dns_zones-hosts.txt", "wb") as file:
            file.write(r.content)
            file.close()
    finally:
        try:
            with open("dns_zones-hosts.txt", "r") as hosts:
                host_list = hosts.read()
        except FileNotFoundError as e:
            print("Unable to get hosts file.", e)
            exit()

    hosts = host_list.split("\n")

    print("Adding...")
    
    while True:
        try:
            blank = hosts.index('')
            hosts.pop(blank)
        except Exception as e: 
            break
    
    # check for old hosts

    headers = {"X-FTL-SID": sid, "X-FTL-CSRF": csrf}
    response = requests.request("GET", url + "/config/dns/hosts", headers=headers)
    try:
        new_json = json.loads(response.text)
    except Exception as e:
        print("Error parsing json. Exiting.")
        print(e)
        exit()
    hosts_old = new_json["config"]["dns"]["hosts"]

    from urllib.parse import quote

    import time
    
    skip = []

    for old_host in hosts_old:
        for new in hosts:
            if new.split(" ")[1] == old_host.split(" ")[1]: #prevent accidenally deleting everything else
                if new.split(" ")[0] != old_host.split(" ")[0]:
                    print("Deleting", old_host)
                    response = requests.request("DELETE", url + "/config/dns/hosts/" + quote(old_host), headers=headers)
                    time.sleep(1) # dont rate limit
                else: # they must be the same here
                    skip.append(old_host)
    # actually add the urls

    for host in hosts:
        if host not in skip: # save a lot of tkme.
            print("Adding", host)
            host = quote(host)
            response = requests.request("PUT", url + "/config/dns/hosts/" + host, headers=headers)
            time.sleep(1) #same here
    print("done!")

    # delete session to allow other api apps
    payload = {}
    headees = {"X-FTL-SID": sid}

    response = requests.request("DELETE", url + "/auth", headers=headers, data=payload, verify=False)

    if response.status_code == 204:
        print("Freed API session!")
else:
    raise Exception("This program must be run as a stsndalone python file..")
