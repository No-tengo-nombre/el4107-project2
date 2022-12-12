from cam_server.core.server_core import ServerCore
from cam_common.logger import setup_logger
from cam_common.configs import DEFAULT_SERVER_PORT, DEFAULT_CLIENT_PORT
import argparse


DESC_STR = """Open the camgrill server."""


PARSER = argparse.ArgumentParser(prog="cam_server", description=DESC_STR)
PARSER.add_argument(
    "-i",
    "--ip",
    action="store",
    type=str,
    default="",
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
    "-c",
    "--client-port",
    action="store",
    type=int,
    default=DEFAULT_CLIENT_PORT,
    help="set the port of the server exposed to the client",
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
    default="cam_server/logs/",
    help="directory for the created logs",
)
args = PARSER.parse_args()


setup_logger(args.quiet, args.debug, args.verbose, args.logs)
sv = ServerCore(args.ip, args.port, args.client_port)
sv.start()
