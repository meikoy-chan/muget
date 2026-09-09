import logging
import colorama

class CustomLoggerFormatter(logging.Formatter):
    """Formateador de logs con colores"""
    
    base_format = "[%(levelname)-8s %(asctime)s]"
    format_colors = {
        logging.DEBUG: colorama.Style.DIM,
        logging.INFO: colorama.Fore.GREEN,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.RED,
    }
    date_format = "%H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        color = self.format_colors.get(record.levelno, "")
        reset = colorama.Style.RESET_ALL
        return logging.Formatter(
            color + self.base_format + reset + " %(message)s",
            datefmt=self.date_format,
        ).format(record)


def setup_logger(name="muget", level="INFO"):
    """Configura y devuelve un logger estilizado"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CustomLoggerFormatter())
        logger.addHandler(stream_handler)
    
    return logger