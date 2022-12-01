from camserver.core.sv_core import ServerCore
from camcommon.logger import setup_logger
from camcommon.configs import FIXED_SERVER_IP, FIXED_SERVER_PORT
import argparse


DESC_STR = """Open the camgrill server."""


PARSER = argparse.ArgumentParser(prog="camserver", description=DESC_STR)
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


setup_logger(False, False, True, None)
sv = ServerCore(args.ip, args.port)
sv.start()
