from logging import getLogger

from bitrix24 import Bitrix24

from conf.log_conf import setup_logging
from libs.bx_lib.models.deal import Deal
from libs.bx_lib.models.contact import Contact

setup_logging()

logger = getLogger(__name__)

class BX:
    def __init__(self,webhook):
        self.bx = Bitrix24(webhook)

    def get_deals(self,category_id,stage_id):
        "get deals from Bitrix"
        logger.info("request deals")
        deals = self.bx.callMethod(
            method="crm.deal.list",
            params={
                "filter":{
                    "CATEGORY_ID":category_id,
                    "STAGE_ID":stage_id,
                    ">CONTACT_ID": 0
                    },
                "select":[
                    "ID",
                    "CONTACT_ID",
                    "STAGE_ID"
                    ]
            }
        )
        deals = [Deal(**deal) for deal in deals]
        logger.info("{deals_count} deals on stages".format(deals_count=len(deals)))
        return deals
    
    def get_contact(self,id):
        "get contact from Bitrix"
        logger.info("request contact: {id}".format(id=id))
        contact = self.bx.callMethod(
            method="crm.contact.get",
            params={
                "ID":id
            }
        )
        return Contact(**contact)

    def get_contacts(self,contact_ids,step=200):
        "request contacts from Bitrix"
        logger.info("request contacts")
        contact_ids = [contact_ids[i:i + step] for i in range(0, len(contact_ids), step)]
        all_contacts = []
        for ids in contact_ids:
            contacts = self.bx.callMethod(
                method="crm.contact.list",
                params={
                    "filter":{
                        "ID":ids,
                        ">UF_CRM_1727700536348": 0
                    },
                    "select":[
                        "ID",
                        "UF_CRM_1727700536348",
                        "UF_CRM_1729781383"
                    ]
                }
            )
            all_contacts.extend([Contact(**contact) for contact in contacts])
        logger.info("correct contacts count: {contacts_count} on stages".format(
            contacts_count=len(all_contacts)
        ))
        return all_contacts

    def update_contact_balance(self,id,balance):
        "update balance for Bitrix contacts"
        logger.info("update for contact: {id} balance: {balance}".format(
            id=id,balance=balance
        ))
        self.bx.callMethod(
            method="crm.contact.update",
            params={
                "id":id,
                "fields":{
                    "UF_CRM_1729781383":balance
                }
            }
        )
    
    def update_deal(self,id,stage_id):
        "update deals for Bitrix"
        logger.info("update deal:{id}".format(id=id))
        self.bx.callMethod(
            method="crm.deal.update",
            params={
                "id":id,
                "fields":{
                    "STAGE_ID":stage_id
                }
            }
        )