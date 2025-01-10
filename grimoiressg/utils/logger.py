import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)-9s: %(message)s")
logger = logging.getLogger("grimoire")
