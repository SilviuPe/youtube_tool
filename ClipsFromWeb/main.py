import os
import platform

from .monitors import MixkitMonitor,PexelsMonitor
from .log.logger import Logger

from threading import Thread

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'
if platform.system() == 'Linux':
    slash = "/"


errors_logger = Logger(f"{CURRENT_DIR}{slash}log{slash}errors.log")
access_logger = Logger(f"{CURRENT_DIR}{slash}log{slash}access.log")

pexels_monitor = PexelsMonitor()
mixkit_monitor = MixkitMonitor()

Thread(target=mixkit_monitor.run).start()
Thread(target=pexels_monitor.run).start()

helper_display = """
    Commands:
        - exit -> close the program
        - stop pexels -> stop pexels searcher
        - stop mixkit -> stop mixkit searcher
        - start pexels -> start pexels searcher
        - start mixkit -> start mixkit searcher
"""

def run_main_monitor():

    command = ''

    while command.strip() != 'exit':

        command = input("_>")

        if command == 'stop pexels':
            pexels_monitor.running_script = False
            access_logger.create_info_log("Stopped PEXELS monitor [object-file] ClipsFromWeb.main [function] run_main_monitor()")

        elif command == 'stop mixkit':
            mixkit_monitor.running_script = True
            access_logger.create_info_log("Stopped MIXKIT monitor [object-file] ClipsFromWeb.main [function] run_main_monitor()")

        elif command == 'start mixkit':
            mixkit_monitor.running_script = True
            Thread(target=mixkit_monitor.run).start()
            access_logger.create_info_log("Started MIXKIT monitor [object-file] ClipsFromWeb.main [function] run_main_monitor()")

        elif command == 'start pexels':
            pexels_monitor.running_script = True
            Thread(target=pexels_monitor.run).start()
            access_logger.create_info_log("Started PEXELS monitor [object-file] ClipsFromWeb.main [function] run_main_monitor()")

        elif command == 'help':
            print()
            print(helper_display)
            print()

    access_logger.create_info_log("Main monitor stopped [object-file] ClipsFromWeb.main [function] run_main_monitor()")

    mixkit_monitor.running_script = False
    pexels_monitor.running_script = False

run_main_monitor()