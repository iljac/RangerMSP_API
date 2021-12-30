from fastapi import FastAPI, Query, HTTPException
from MSPService import MSPService
from serializers import charge_to_dict, account_to_dict, item_to_dict, ticket_to_dict
from schemas import Item, Account

msp = MSPService()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "RangerMSP API"}


@app.get("/get_charges")
async def get_charges(ticket_closed: bool, AccountNo='', show_billed_charges=False, search_days=180):
    result = []
    for charge in msp.get_billable_charges(ticket_closed=ticket_closed, AccountNo=AccountNo,
                                           show_billed_charges=show_billed_charges, search_days=search_days):
        result.append(charge_to_dict(charge))
    return result

@app.post('/set_charge_billed')
async def set_charge_billed(ChargeREC_ID: str):
    msp.set_charge_billed(ChargeREC_ID)
    return {'Billed': ChargeREC_ID}

@app.get('/accounts')
async def get_accounts(AccountREC_ID: str = Query(None), AccountNo: str = Query(None)):
    if AccountREC_ID:
        result = account_to_dict(msp.get_accounts(AccountREC_ID=AccountREC_ID))
    elif AccountNo:
        result = account_to_dict(msp.get_accounts(AccountNo=AccountNo))
    else:
        result = []
        for account in msp.get_accounts():
            result.append(account_to_dict(account))
    return result

@app.post('/accounts')
async def post_accounts(account: Account):
    try:
        msp.add_account(account)
    except:
        return HTTPException(status_code=422, detail='wrong data')

@app.get('/items')
async def get_items(ItemREC_ID: str = Query(None), ItemNo: str = Query(None)):
    if ItemREC_ID:
        result = item_to_dict(msp.get_items(ItemREC_ID=ItemREC_ID))
    elif ItemNo:
        result = item_to_dict(msp.get_items(ItemNo=ItemNo))
    else:
        result = []
        for item in msp.get_items():
            if item_to_dict(item)['ItemREC_ID'] != "":
                result.append(item_to_dict(item))
    return result


@app.post('/items')
async def post_items(item: Item):
    return msp.add_item(item)


@app.get('/ticket')
async def get_ticket(TicketRec_ID: str):
    return ticket_to_dict(msp.get_ticket(TicketRec_ID))


@app.on_event("shutdown") # Doesn't work
def shutdown_event():
    msp.disconnect()
    print('Shutdown')

