from screan_cleaner import clean_screen

clean_screen()

import sys 
import Proxy

def is_valid_port(port):
    try:
        return 0 <= int(port) <= 65535
    except ValueError:
        return False
    
if (not is_valid_port(sys.argv[1])):
    print("Invalid port")
    sys.exit()
    
server_port = int(sys.argv[1])
server_host = "127.0.0.1"

proxy = Proxy.Proxy()
proxy.run(server_host, server_port)