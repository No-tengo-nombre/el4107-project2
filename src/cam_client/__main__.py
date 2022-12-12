from cam_client.core.client_core import ClientCore
from cam_common.configs import (
    DEFAULT_SERVER_IP,
    DEFAULT_CLIENT_PORT,
    LOCAL_CAMERA_IP,
    LOCAL_CAMERA_PORT,
)
from cam_common.logger import setup_logger

import argparse


DESC_STR = """Connect to the camgrill as a client."""


PARSER = argparse.ArgumentParser(prog="cam_client", description=DESC_STR)
PARSER.add_argument(
    "-i",
    "--ip",
    action="store",
    type=str,
    default=DEFAULT_SERVER_IP,
    help="set the public ip of the server",
)
PARSER.add_argument(
    "-p",
    "--server-port",
    action="store",
    type=int,
    default=DEFAULT_CLIENT_PORT,
    help="set the port of the server for the client",
)
PARSER.add_argument(
    "-t",
    "--target-ip",
    action="store",
    type=str,
    default=LOCAL_CAMERA_IP,
    help="set target ip",
)
PARSER.add_argument(
    "-r",
    "--target-port",
    action="store",
    type=int,
    default=LOCAL_CAMERA_PORT,
    help="set target port",
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
    default="cam_client/logs/",
    help="directory for the created logs",
)
args = PARSER.parse_args()

setup_logger(args.quiet, args.debug, args.verbose, args.logs)
c = ClientCore(args.ip, args.server_port, args.target_ip, args.target_port)
c.start()
