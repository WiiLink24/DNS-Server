WiiLink DNS Server [![Actions Status](https://github.com/WiiLink24/DNS-Server/workflows/Build/badge.svg)](https://github.com/WiiLink24/DNS-Server/actions)
===

This DNS Server will run locally on your computer and allow your Wii to connect to WiiLink servers to use additional services, even if your ISP blocks connections to our DNS Server. When you use the DNS on your Wii or with this app, it also enhances the use of services such as Wiimmfi. This tool can also be used as a DNS server for Nintendo DS games.

## Setup

You will only need to change DNS settings on your console.

First, make sure that your console is connected to the same network as your computer is.

**If you use Pi-hole, please see [Setting up Pi-hole](#Setting-up-Pi-hole)**

# Running on Windows:

Run the .exe provided [on the releases page](https://github.com/WiiLink24/-DNS-Server/releases). If your antivirus notifies you about the .exe file, allow it and run it. If it doesn't work, ensure you have allowed communication for this this .exe in your firewall settings.

# Running on Linux/macOS:

You will need to install Python 3 and run these commands in the Terminal:

> pip install dnslib requests

To run it, simply type in:

> sudo python3 DNS-Server.py

Replace `python3` with the name/path to your Python binary if necessary

# How to use it?

After starting the program, it will download the current list of the DNS Addresses to forward and will run. 

On screen, you will see the IP Address assigned to your computer by the DHCP Server on your NAT (router).

If your Wii is connected to the same network as your PC, it will be able to connect to the server on your PC.

<p align="center">
  <img src="https://i.imgur.com/oageZQ3.jpg">
<i>My local IP Address, yours <b>WILL</b> be different.</i>
</p>


# Compiling on Windows

To compile this app on Windows, you will need to run these two commands:
>pip install dnslib requests pyinstaller

Once it's done installing, run:
>pyinstaller DNS-Server.spec

| Tip: You may need to edit DNS-Server.spec so the compiling process works on your computer.

# Setting up Pi-hole

## Pi-hole v5 and below
On the server running Pi-hole, run the following command:

```bash
curl https://raw.githubusercontent.com/WiiLink24/DNS-Server/master/dns_zones-hosts.txt >> /etc/pihole/custom.list
```
WiiLink domains will be listed on Pi-hole webpage menu under "Local DNS Records".

## Pi-hole v6
On a device that can access the Pi-hole server, download the "pihole6-setup.py" file.

Install the requests library (`pip install requests`) and run the file with the url to your server as an argument (with ports; typically port 80 or 443):

```bash
python3 pihole6-setup.py <SERVER URL>
```

It will then ask for your server password so it can access its API to add the hosts. Once done, hosts should be added automatically.

# Need more help?
You can talk to us over on our [Discord server](https://discord.gg/wiilink), where people can try and help you out!
