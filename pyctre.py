# pyctre: Simple Python script for communicating with CTRE's Phoenix Diagnostics Server
# By gvl610
# I will try to keep names close to the names in Phoenix Tunner's code

import requests
import json

def HttpGet(host: str, port: int, model: str = "", canbus: str = "", deviceID: int = 0, action: str = None, extraOptions: str = "", timeout: int = 200):
    # Prepare payload
    p = {}

    # Model: talon srx, talon fx, victor spx, canifier, pigeon, pigeon over ribbon, pcm, pdp
    if model != "":
        p["model"] = model

    # CAN bus (currently uninvestigated)
    if canbus != "":
        p["canbus"] = canbus
    
    # Action: getversion, getdevices, blink, setid (newid=), setname (newname=), selftest, fieldupgrade, progress, getconfig, setconfig
    if action == None:
        # Error
        raise Exception("Error: No action is specified")
    else:
        p["action"] = action
    
    # Send request
    #print(p)
    r = requests.get('http://' + host + ":" + str(port), params=p, timeout=timeout/1000)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return None

def printhelp():
    print("pyctre: Simple Python script for communicating with CTRE's Phoenix Diagnostics Server")
    print("Usage: pyctre.py [hostname][]:port] [action] ...")
    print("\thostname\thostname/ip of your roboRIO/whatever the server is running on")
    print("\tport\t\tthe port that the server is listening on. Default is 1250 if not specified. For example, to specify host and port, use 10.TE.AM.2:1250")
    print("\taction\t\tthe action you want to perform. Actions include getversion, getdevices, blink, setid, setname, selftest, fieldupgrade, progress, getconfig, setconfig")
    print("Other parameters can be passed after the action:")
    print("\t--model\t\tmodel name. Model names include talon srx, talon fx, victor spx, canifier, pigeon, pigeon over ribbon, pcm, pdp. Example: --model \"talon srx\"")
    print("\t--canbus\tspecify canbus. Haven't tested, use with caution! canbus is passed as a string")
    print("\t--id\t\tdevice's CAN ID. Example: --id 0. Default is 0 if this parameter is not available.")
    print("\t--extraOptions\textra options (as a string) to send to server. This is used in rename and change device's ID.")
    print("\t--timeout\trequest timeout time, in miliseconds")

def pp(host: str, port: int, model: str = "", canbus: str = "", deviceID: int = 0, action: str = None, extraOptions: str = "", timeout: int = 200):
    print(json.dumps(HttpGet(host, port, model, canbus, deviceID, action, extraOptions, timeout), indent=4))

def parse_addr(inp):
    s = inp.split(":")
    if len(s) == 1:
        return (s[0], 1250)
    else:
        return (s[0], s[1])

def get_param(p):
    try:
        i = sys.argv.index(p)
        return sys.argv[i + 1]
    except ValueError:
        if p == "--id":
            return 0
        elif p == "--timeout":
            return 200
        else:
            return ""

# If called directly instead of as a library
if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 2:
        # Print help
        printhelp()
    elif len(sys.argv) >= 3:
        host, port = parse_addr(sys.argv[1])
        pp(host, port, get_param("--model")[1:-1], get_param("--canbus")[1:-1], get_param("--id"), sys.argv[2], get_param("--extraOptions")[1:-1], get_param("--timeout"))
