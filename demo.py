from src.us_visa_approval.logger import logging
from src.us_visa_approval.exception import UsvisaException
import sys


logging.info("welcome to our custome log")

try:
    a = 2/0
except Exception as e:
    raise UsvisaException(e, sys)