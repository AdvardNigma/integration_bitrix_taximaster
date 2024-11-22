from os import getenv
from logging import getLogger
import time

from dotenv import load_dotenv

from libs.tm_lib.tm_api import TM
from libs.bx_lib.bx_api import BX
from conf.log_conf import setup_logging


setup_logging()
load_dotenv()

logger = getLogger(__name__)
bx_webhook = getenv("BX_WEBHOOK")
tm_domain = getenv("TM_DOMAIN")
tm_port = getenv("TM_PORT")
tm_token = getenv("TM_TOKEN")
request_time_sleep = int(getenv("REQUEST_TIME_SLEEP"))
drivers_request_count = int(getenv("DRIVERS_REQUEST_COUNT"))
bx_category_id = int(getenv("BX_CATEGORY_ID"))
bx_stage_ids = getenv("BX_STAGE_IDS").split(",")
min_balance = int(getenv("MIN_BALANCE"))


tm = TM(
    domain=tm_domain,
    port=tm_port,
    token=tm_token
)
bx = BX(webhook=bx_webhook)

def update_contacts(contacts,drivers):
    """Update contacts balance"""
    for driver in drivers:
        for contact in contacts:
            if contact.tm_id == driver.id and contact.balance != driver.balance:
                logger.info("old balance:{old_balance} | new_balance:{new_balance}".format(
                    old_balance=contact.balance,new_balance=driver.balance
                ))
                bx.update_contact_balance(
                    id=contact.id,balance=driver.balance
                )

def update_contacts_balance(driver_ids,contacts,step=drivers_request_count):
    """Reuest drivers from TM and update contacts balance"""
    driver_ids = [driver_ids[i:i + step] for i in range(0, len(driver_ids), step)]
    for ids in driver_ids:
        drivers = tm.get_drivers(driver_ids=ids) # получение водителей 
        update_contacts(contacts=contacts,drivers=drivers) # обновление контактов
        logger.info("time to sleep")
        time.sleep(request_time_sleep)


#   TASKS
def update_deals():
    logger.info("START UPDATING DEALS TASK")
    deals = bx.get_deals(category_id=bx_category_id,stage_id=bx_stage_ids)  # Получение седлок на этапах воронки
    contact_ids = [deal.contact_id for deal in deals] # получение id контактов
    contact_ids = list(set(contact_ids)) # удаление повторяющихся id
    contacts = bx.get_contacts(contact_ids=contact_ids) # получение контактов
    for contact in contacts:
        for deal in deals:
            if deal.contact_id == contact.id:
                if deal.stage_id == "C9:PREPARATION" and contact.balance < min_balance:
                    bx.update_deal(deal.id,stage_id="C9:PREPAYMENT_INVOICE")
                elif deal.stage_id == "C9:PREPAYMENT_INVOICE" and contact.balance > min_balance:
                    bx.update_deal(id=deal.id,stage_id="C9:PREPARATION")
    logger.info("UPDATING DEALS TASK FINISHED")

def main():
    logger.info("START MAIN TASK")
    deals = bx.get_deals(category_id=bx_category_id,stage_id=bx_stage_ids)  # Получение седлок на этапах воронки
    contact_ids = [deal.contact_id for deal in deals] # получение id контактов
    contact_ids = list(set(contact_ids)) # удаление повторяющихся id
    contacts = bx.get_contacts(contact_ids=contact_ids) # получение контактов
    driver_ids = [contact.tm_id for contact in contacts] # получение id_tm
    update_contacts_balance(driver_ids=driver_ids,contacts=contacts)
    logger.info("MAIN TASK FINISHED")
