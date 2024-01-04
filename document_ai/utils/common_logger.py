import logging

class CommonLogger:
    @staticmethod
    def get_logger(name):
        # Configure the logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Create handlers (console, file, etc.)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('app.log')

        # Create formatters and add them to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger
