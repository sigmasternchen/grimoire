from grimoiressg.modules import available_modules
from grimoiressg.utils import logger


def test(data, context, config):
    logger.info("This is test module.")


available_modules["test"] = test
