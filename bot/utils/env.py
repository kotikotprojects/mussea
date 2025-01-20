import os
import sys

from dotenv import load_dotenv

try:
    load_dotenv()

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    SIGNER_MICROSERVICE_URL = os.environ["SIGNER_MICROSERVICE_URL"]

except KeyError as e:
    print("Can't parse environment", e)
    sys.exit(1)
