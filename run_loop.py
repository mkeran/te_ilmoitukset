import logging
from time import sleep
import te_palvelut


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

fh = logging.FileHandler(filename="example.log")
fh.setFormatter(formatter)
fh.setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG, handlers=[ch, fh])

SEC = 1500


def time_loop():
    logger.info("skripti alkaa")
    while True:
        try:
            te_palvelut.main()
        except Exception:
            logger.info("kaatui")

        logger.debug("Sleep for: %s seconds", SEC)
        sleep(SEC)

if __name__ == '__main__':
    time_loop()
