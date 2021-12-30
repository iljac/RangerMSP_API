def charge_to_dict(chrg):
    return {'ChargeREC_ID': chrg.ChargeREC_ID, 'AccountREC_ID': chrg.AccountREC_ID, 'EmployeeREC_ID': chrg.EmployeeREC_ID,
            'ChargedItem': chrg.ChargedItem, 'ContractREC_ID': chrg.ContractREC_ID, 'TicketREC_ID': chrg.TicketREC_ID,
            'Date': f'{chrg.Date.Day}/{chrg.Date.Month}', 'Description': chrg.Description, 'Units_Hours': chrg.Units_Hours/100,
            'HourlyBased': chrg.HourlyBased, 'AdjustAmount': chrg.AdjustAmount, 'AdjustPercent': chrg.AdjustPercent,
            'FromTime': chrg.FromTime, 'ToTime': chrg.ToTime, 'Price_Rate': chrg.Price_Rate/100,
            'Billable': chrg.Billable, 'Billed': chrg.Billed, 'Field1': chrg.Field1, 'CreateUser': chrg.CreateUser}


def account_to_dict(acc):
    return {'AccountREC_ID': acc.AccountREC_ID, 'AccountManager': acc.AccountManager, 'CompanyName': acc.CompanyName,
            'Contact': acc.Contact, 'Status': acc.Status, 'Assistant': acc.Assistant,
            'AccountNumber': acc.AccountNumber, 'ID': acc.ID,
            'PopupMessage': acc.PopupMessage, 'AddressLine1': acc.AddressLine1, 'AddressLine2': acc.AddressLine2,
            'AddressLine3': acc.AddressLine3, 'City': acc.City, 'Country': acc.Country, 'State': acc.State,
            'Zip': acc.Zip, 'CreationDate': str(acc.CreationDate), 'CreatedByUser': acc.CreatedByUser, 'Dear': acc.Dear,
            'Department': acc.Department, 'DocumentsStoreDirectory': acc.DocumentsStoreDirectory,
            'EmailAddress1': acc.EmailAddress1, 'EmailAddress2': acc.EmailAddress2, 'AccountType': acc.AccountType,
            'FaxNumber': acc.FaxNumber, 'FaxNumberExt': acc.FaxNumberExt, 'FileAs': acc.FileAs, 'Type': acc.Type,
            'LastName': acc.LastName, 'Notes': acc.Notes, 'Field': acc.Field, 'Phone1Ext': acc.Phone1Ext,
            'Phone2Ext': acc.Phone2Ext, 'Phone3Ext': acc.Phone3Ext, 'Phone4Ext': acc.Phone4Ext, 'Phone1': acc.Phone1,
            'Phone2': acc.Phone2, 'Phone3': acc.Phone3, 'Phone4': acc.Phone4, 'Region': acc.Region,
            'PopupMessageDisplayIndication': acc.PopupMessageDisplayIndication, 'SubContractCode': acc.SubContractCode,
            'Salutation': acc.Salutation, 'Tax1': acc.Tax1, 'Tax2': acc.Tax2, 'Title': acc.Title,
            'LastUpdatedBy': acc.LastUpdatedBy, 'WebAddress1': acc.WebAddress1, 'WebAddress2': acc.WebAddress2,
            'Status': acc.Status, 'Field1': acc.Field1, 'Field2': acc.Field2, 'Field3': acc.Field3, 'Field4': acc.Field4}
# 'ContractREC_ID': acc.ContractREC_ID,


def item_to_dict(itm):
    return {'ItemREC_ID': itm.ItemREC_ID, 'ItemGroup': itm.ItemGroup, 'ItemCode': itm.ItemCode,
            'ItemName': itm.ItemName, 'PriceSource': itm.PriceSource, 'PricePerHour_Unit': itm. PricePerHour_Unit,
            'Price': itm.Price/100, 'Cost': itm.Cost/100, 'Tax1': itm.Tax1, 'Tax2': itm.Tax2, 'Tax3': itm.Tax3,
            'DescriptionByName': itm.DescriptionByName, 'Description': itm.Description, 'Suspend': itm.Suspend,
            'Notes': itm.Notes, 'Field1': itm.Field1, 'CreateUser': itm.CreateUser}


def ticket_to_dict(tckt):
    return {'TicketREC_ID': tckt.TicketREC_ID, 'AccountREC_ID': tckt.AccountREC_ID, 'AssetREC_ID': tckt.AssetREC_ID,
            'ContactREC_ID': tckt.ContactREC_ID, 'ContractREC_ID': tckt.ContractREC_ID,
            'EmployeeREC_ID': tckt.EmployeeREC_ID, 'TicketPriority': tckt.TicketPriority,
            'TicketNumber': tckt.TicketNumber, 'Description': tckt.Description, 'TicketType': tckt.TicketType,
            'Source': tckt.Source, 'EstimatedDurationTime': tckt.EstimatedDurationTime,
            'ShowTicketInDispatcher': tckt.ShowTicketInDispatcher, 'Status': tckt.Status,
            'CreatedByUser': tckt.CreatedByUser, 'DueDate': str(tckt.DueDate), 'Resolution': tckt.Resolution,
            'UpdateDate': str(tckt.UpdateDate)}
