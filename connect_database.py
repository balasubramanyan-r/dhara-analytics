import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
"realestateanalytics-489603-2e82bee42942.json", scope)

client = gspread.authorize(creds)

sheet = client.open("RealEstate_Marketing_Data")

campaign_sheet = sheet.worksheet("Campaign_Data")

data = campaign_sheet.get_all_records()

df = pd.DataFrame(data)

print("Connected Successfully!")
print(df)
