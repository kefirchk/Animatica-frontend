import logging

from colorama import init, Fore, Style

init(autoreset=True)


class CustomLogger:
    def __init__(self, name: str, log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def info(self, message: str):
        self.logger.info(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

    def warning(self, message: str):
        self.logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def error(self, message: str):
        self.logger.error(f"{Fore.RED}{message}{Style.RESET_ALL}")

    def critical(self, message: str):
        self.logger.critical(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")
