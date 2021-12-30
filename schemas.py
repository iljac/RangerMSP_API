from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    ItemCode: str
    ItemGroup: Optional[str] = 'P'
    ItemName: str
    Price: Optional[str] = '0'
    Cost: Optional[str] = ''
    Tax1: Optional[str] = ''
    Description: Optional[str] = ''
    Notes: Optional[str] = ''
    Updated: str = None

    class Config:
        schema_extra = {
            'Updated': '%d/%m/%Y %H:%M \n Compared with record to determine if data is newer\n Optional'
        }

class Account(BaseModel):
    AccountNumber: str
    CompanyName: str
    AddressLine1: str = ''
    AddressLine2: str = ''
    AddressLine3: str = ''
    City: str = ''
    Zip: str = ''
    Country: str = ''
    Contact: str = ''
    EmailAddress1: str = ''
    Status: str = 'Active'
    Updated: str = None

    class Config:
        schema_extra = {
            'Updated': '%d/%m/%Y %H:%M \n Compared with record to determine if data is newer\n Optional'
        }
