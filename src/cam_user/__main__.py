from cam_user.core.user_core import UserCore
from cam_common.configs import FIXED_SERVER_IP, FIXED_SERVER_PORT
import argparse


DESC_STR = """Connect to the camgrill as a client."""


PARSER = argparse.ArgumentParser(prog="cam_user", description=DESC_STR)
PARSER.add_argument(
    "-i",
    "--ip",
    action="store",
    type=str,
    default=FIXED_SERVER_IP,
    help="set the ip of the server",
)
PARSER.add_argument(
    "-p",
    "--port",
    action="store",
    type=int,
    default=FIXED_SERVER_PORT,
    help="set the port of the server",
)
args = PARSER.parse_args()


c = UserCore(args.ip, args.port)
c.start()
