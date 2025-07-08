import colorama
import datetime

colorama.init(autoreset=True)


class Logger(object):
    def __init__(self, path: str) -> None:
        self.message_data = {
            'info': {
                'color': colorama.Fore.WHITE,
                'sign': 'i',
                'text': 'INFO'
            },
            'error': {
                'color': colorama.Fore.RED,
                'sign': '-',
                'text': 'ERROR'
            },
            'warning': {
                'color': colorama.Fore.YELLOW,
                'sign': '!',
                'text': 'WARNING'
            },
            'success': {
                'color': colorama.Fore.GREEN,
                'sign': '+',
                'text': 'SUCCESS'
            },
        }

        self.logger_path_file = path

    def open_logger(self):

        try:
            logger = open(self.logger_path_file, 'a')

            return logger
        except Exception as error:
            print(error)

    def create_info_log(self, message):

        timestamp = datetime.datetime.today().strftime("%d-%m-%Y, %H:%M:%S")

        print(colorama.Back.BLACK + self.message_data['info'][
            'color'] + f"[{self.message_data['info']['text']}]" + colorama.Fore.RESET + f" {message} ")

        logger = self.open_logger()
        logger.write(f"[{self.message_data['info']['sign']}] [{timestamp}] {message}\n")
        logger.close()

    def create_error_log(self, message):

        timestamp = datetime.datetime.today().strftime("%d-%m-%Y, %H:%M:%S")

        print(colorama.Back.BLACK + self.message_data['error'][
            'color'] + f"[{self.message_data['error']['text']}]" + colorama.Fore.RESET + f" {message} ")

        logger = self.open_logger()
        logger.write(f"[{self.message_data['error']['sign']}] [{timestamp}] {message}\n")
        logger.close()

    def create_success_log(self, message):

        timestamp = datetime.datetime.today().strftime("%d-%m-%Y, %H:%M:%S")

        print(colorama.Back.BLACK + self.message_data['success'][
            'color'] + f"[{self.message_data['success']['text']}]" + colorama.Fore.RESET + f" {message} ")

        logger = self.open_logger()
        logger.write(f"[{self.message_data['success']['sign']}] [{timestamp}] {message}\n")
        logger.close()

    def create_warning_log(self, message):

        timestamp = datetime.datetime.today().strftime("%d-%m-%Y, %H:%M:%S")

        print(colorama.Back.BLACK + self.message_data['warning'][
            'color'] + f"[{self.message_data['warning']['text']}]" + colorama.Fore.RESET + f" {message} ")

        logger = self.open_logger()
        logger.write(f"[{self.message_data['warning']['sign']}] [{timestamp}] {message}\n")
        logger.close()


