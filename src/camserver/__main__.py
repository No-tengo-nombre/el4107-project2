from camserver.core.sv_core import ServerCore
from camcommon.logger import setup_logger


setup_logger(False, False, True, None)
sv = ServerCore()
sv.start()
