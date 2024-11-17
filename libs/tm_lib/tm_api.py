import requests
from logging import getLogger
from urllib3 import disable_warnings, exceptions

from hashlib import md5

from conf.log_conf import setup_logging
from libs.tm_lib.models.driver import Driver

# Отключение предупреждений InsecureRequestWarning
disable_warnings(exceptions.InsecureRequestWarning)
setup_logging()

logger = getLogger(__name__)

class TM:
    def __init__(
            self,domain,port,token
            ):
        self.base_url = f"https://{domain}:{port}/common_api/1.0"
        self.token = token

    def get_driver(self,id):
        "request driver from TM"
        logger.info("request driver:{id}".format(id=id))
        params = f"driver_id={id}"
        url = self.base_url + "/get_driver_info?" + params
        hash = md5((params + self.token).encode()).hexdigest()
        headers = {
            "Signature":hash,
            "X-User-Id": "2"
        }
        driver = requests.get(
            url=url,
            headers=headers,
            verify=False
        )
        if driver.status_code == 200:
            driver = Driver(**driver.json()["data"])
            logger.debug("his balance is {balance}".format(balance=driver.balance))
        
        return driver
    
    def get_drivers(self,driver_ids):
        "reuest drivers from TM"
        logger.info("request {drivers_count} drivers".format(
            drivers_count=len(driver_ids)
        ))
        drivers = []
        for driver_id in driver_ids:
            driver = self.get_driver(id=driver_id)
            drivers.append(driver)
        return(drivers)