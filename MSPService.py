import clr
from os import path
from datetime import datetime, timedelta
import json
from schemas import Item, Account

# init the .net dll file and import the namespace
basepath = R"\\crm\commit"
if path.exists(basepath + R'\DBsys\CRMStop.ini'):
    print('RangerMSP is down for maintenance')
    raise SystemExit
dll = basepath + R'\ThirdParty\UserDev\CRMLib.dll'
clr.AddReference(dll)
import CRM

class MSPService:
    def __init__(self):
        self.MSPApp = CRM.Application
        self.Query = CRM.ObjectQuery
        self.MSPConfig = CRM.Config()
        self.MSPConfig.AppName = "CRMAgent"
        self.MSPConfig.DllFolder = basepath + R"\ThirdParty\UserDev"
        self.MSPConfig.DbFolder = basepath + R"\Db"

        self.connect()

    def is_connected(self):
        return self.MSPApp.instance().initialized_

    def connect(self):
        if not self.is_connected():
            print('Initializing MSP Database')
            self.MSPApp.Initialize(self.MSPConfig)
            print(f"Database initialized: {self.MSPApp.instance().initialized_}")

    def disconnect(self):
        if self.is_connected():
            self.MSPApp.Terminate()
            print(f"Database initialized: {self.MSPApp.instance().initialized_}")

    def get_items(self, ItemREC_ID='', ItemNo=''):
        item_search = self.Query[CRM.Item]()
        if ItemREC_ID:
            item_search.AddCriteria(CRM.Item.Fields.ItemREC_ID, CRM.OperatorEnum.opEqual, ItemREC_ID)
            return item_search.FetchObjects()[0]
        elif ItemNo:
            item_search.AddCriteria('FLDITMITEMNO', CRM.OperatorEnum.opEqual, ItemNo)
            return item_search.FetchObjects()[0]
        else:
            return item_search.FetchObjects()

    def get_ticket(self, TicketREC_ID):
        tckt_search = self.Query[CRM.Ticket]()
        tckt_search.AddCriteria(CRM.Ticket.Fields.TicketREC_ID, CRM.OperatorEnum.opEqual, TicketREC_ID)
        return tckt_search.FetchObjects()[0]

    def get_accounts(self, AccountREC_ID='', AccountNo=''):
        account_search = self.Query[CRM.Account]()
        if AccountREC_ID:
            account_search.AddCriteria(CRM.Account.Fields.AccountREC_ID, CRM.OperatorEnum.opEqual, AccountREC_ID)
            return account_search.FetchObjects()[0]
        elif AccountNo:
            account_search.AddCriteria('FLDCRDCARDID2', CRM.OperatorEnum.opEqual, AccountNo)
            return account_search.FetchObjects()[0]
        else:
            return account_search.FetchObjects()

    def ticket_completed(self, TicketREC_ID):
        # TicketREC_ID = json.loads(TicketREC_ID)
        if TicketREC_ID == '':
            return True
        ticket_search = self.Query[CRM.Ticket]()
        ticket_search.AddCriteria(CRM.Ticket.Fields.TicketREC_ID, CRM.OperatorEnum.opEqual, TicketREC_ID)
        tickets = ticket_search.FetchObjects()
        status = tickets[0].Status
        return status == 1000

    def get_billable_charges(self, ticket_closed=False,  AccountNo='', show_billed_charges=False, search_days=180):

        # Find charges that are "Billable" but not "Billed" and newer than Date
        # Sort by AccountREC_ID and Date
        charge_search = self.Query[CRM.Charge]()
        if AccountNo:
            acc = self.get_accounts(AccountNo=AccountNo).AccountREC_ID
            charge_search.AddCriteria(CRM.Charge.Fields.AccountREC_ID, CRM.OperatorEnum.opEqual, acc)
        charge_search.AddCriteria(CRM.Charge.Fields.Billable, CRM.OperatorEnum.opEqual, "B")
        if not show_billed_charges:
            charge_search.AddCriteria(CRM.Charge.Fields.Billed, CRM.OperatorEnum.opEqual, "D")
        charge_search.AddCriteria(CRM.Charge.Fields.Date, CRM.OperatorEnum.opGreaterThanOrEqual,
                                  (datetime.now() - timedelta(days=search_days)).strftime("%d/%m/%Y"))
        charge_search.AddSortExpression(CRM.Charge.Fields.AccountREC_ID, CRM.SortDirectionEnum.sortASC)
        charge_search.AddSortExpression(CRM.Charge.Fields.Date, CRM.SortDirectionEnum.sortASC)
        if ticket_closed:
            result = []
            for charge in charge_search.FetchObjects():
                if self.ticket_completed(charge.TicketREC_ID):
                    result.append(charge)
        else:
            result = charge_search.FetchObjects()
        return result

    def set_charge_billed(self, chrg_recid):
        charge_search = self.Query[CRM.Charge]()
        charge_search.AddCriteria(CRM.Charge.Fields.ChargeREC_ID, CRM.OperatorEnum.opEqual, chrg_recid)
        charge = charge_search.FetchObjects()
        charge[0].Billed = "B"
        charge[0].Save()

    def add_account(self, account: Account):
        account_search = self.Query[CRM.Account]()
        account_search.AddCriteria('FLDCRDCARDID2', CRM.OperatorEnum.opEqual, account.AccountNumber)
        msp_acc = account_search.FetchObjects()
        new_account = None
        # if account['updatedfromat']['$date'] == -62135596800000:
        #     account['updatedfromat']['$date'] = 0
        if len(msp_acc) == 0:
            print('create account')
            new_account = CRM.Account()
        elif len(msp_acc) == 1 and datetime.strptime(msp_acc[0].GetFieldValue('FLDCRDUPDATEDATE'), "%d/%m/%Y %H:%M") \
                < datetime.strptime(account.Updated, "%d/%m/%Y %H:%M"):
            print(f'update account {account.CompanyName}')
            new_account = CRM.Account(msp_acc[0].AccountREC_ID)
        if new_account:
            new_account.CompanyName = account.CompanyName
            new_account.Contact = account.Contact
            new_account.AccountNumber = account.AccountNumber
            new_account.EmailAddress1 = account.EmailAddress1
            new_account.AddressLine1 = account.AddressLine1
            new_account.AddressLine2 = account.AddressLine2
            new_account.AddressLine3 = account.AddressLine3
            new_account.Zip = account.Zip
            new_account.City = account.City
            new_account.Country = account.Country
            new_account.Status = account.Status
            # else:
            #     new_account.SetFieldValue('FLDCRDACCOUNTSTATUS', 'Active')
            new_account.Save()

    def add_item(self, itm: Item):
#        itm = json.loads(itm)
        item_search = self.Query[CRM.Item]()
        item_search.AddCriteria('FLDITMITEMNO', CRM.OperatorEnum.opEqual, itm.ItemCode)
        search_item = item_search.FetchObjects()
        item = None
#        if itm['updatedfromat']['$date'] == -62135596800000:
#            itm['updatedfromat']['$date'] = 0
#        else:
#            itm['updatedfromat']['$date'] = itm['updatedfromat']['$date'] / 1000

        if len(search_item) == 0 and itm.ItemGroup == 'P':
            print(f'create search_item {itm.ItemName}')
            item = CRM.Item()
        elif len(search_item) == 1:
                # and datetime.strptime(search_item[0].GetFieldValue('FLDITMUPDATEDATE'),
                #                                          "%d/%m/%Y %H:%M") < datetime.fromtimestamp(
            # itm['updatedfromat']['$date']):
            print(f'update search_item {itm.ItemName}')
            item = CRM.Item(search_item[0].ItemREC_ID)
        if item:
            item.ItemGroup = 'P'
            item.ItemCode = itm.ItemCode
            item.ItemName = itm.ItemName
            item.SetFieldValue("FLDITMUNITPRICE", str(itm.Price))
            item.SetFieldValue("FLDITMSTANDARDCOST", str(itm.Cost))
            item.Notes = itm.Notes
            if itm.Description != '':
                item.Description = itm.Description
            else:
                item.DescriptionByName = 'Y'
            item.Save()
            return f'Item {itm.ItemName} created or updated'
        else:
            return 'Error'

""" 
   def get_ticket_ext_invoice(self, TicketREC_ID):
        if TicketREC_ID == '':
            return True
        ticket_search = self.Query[CRM.Ticket]()
        ticket_search.AddCriteria(CRM.Ticket.Fields.TicketREC_ID, CRM.OperatorEnum.opEqual, TicketREC_ID)
        tickets = ticket_search.FetchObjects()
        inv_id = tickets[0].GetFieldValue('FLDTKTUSER1')
        if inv_id != '':
            return tickets[0].Description
        else:
            return True
"""
