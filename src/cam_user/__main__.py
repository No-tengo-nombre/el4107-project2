from cam_user.core.user_core import UserCore
from cam_common.configs import DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT
from cam_common.logger import setup_logger
import argparse


DESC_STR = """Connect to the camgrill as a user."""


PARSER = argparse.ArgumentParser(prog="cam_user", description=DESC_STR)
PARSER.add_argument(
    "-i",
    "--ip",
    action="store",
    type=str,
    default=DEFAULT_SERVER_IP,
    help="set the ip of the server",
)
PARSER.add_argument(
    "-p",
    "--port",
    action="store",
    type=int,
    default=DEFAULT_SERVER_PORT,
    help="set the port of the server",
)
PARSER.add_argument(
    "--quiet",
    action="store_true",
    help="run in quiet mode",
)
PARSER.add_argument(
    "--debug",
    action="store_true",
    help="run in debug mode",
)
PARSER.add_argument(
    "--verbose",
    action="store_true",
    help="run in verbose mode",
)
PARSER.add_argument(
    "--logs",
    action="store",
    default="cam_user/logs/",
    help="directory for the created logs",
)
args = PARSER.parse_args()

setup_logger(args.quiet, args.debug, args.verbose, args.logs)
c = UserCore(args.ip, args.port)
c.start()
