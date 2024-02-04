import pandas as pd 
import random
import datetime
import numpy as np

file = pd.read_csv("/Users/m.shen/Desktop/Baruch College/MTA X TLDP Remote Internship/Eyewear Tracking File Data-Year 2023.csv").fillna(0)

##delete unused columns
to_drop = ["#", "Form #", "Corrected Form #\n (If Duplicated)", "Check vs WIP\nIn Progress (Trk #)", "Check vs WIP\nCompleted (Trk #)", "Check vs WIP\nCompleted (Delivery Date)", "Check vs WIP\nBilled (Trk #)", "Check vs WIP\nBilled (Delivery Date)",
        "Check vs WIP\nRejected Orders", "FOLLOW UP DATE FROM LIAISON", "POG ORDER ", "Unnamed: 27", "Unnamed: 28", "Unnamed: 29", "Unnamed: 30", "Unnamed: 31", "Unnamed: 32", "Unnamed: 33", "Unnamed: 34", "Unnamed: 35"]

file.drop(to_drop, inplace=True, axis=1)

##replace dirty data with an unified version
##create a list for various versions of not indicated and gun metal
##exclude BROWN/ORANGE in the colors list to prevend randomly asigning it in the column
frame = ["138", "14", "208", "220A", "220S", "220SA", "508", "523033", "80", "95", "SW06"]
colors = ["BLACK", "BROWN", "CLEAR", "GUN METAL", "GOLD", "GREY"]
pub = file["COLORS"]
nan = ["No", "not", "57", "Not indicated", "not an option", "One indicated not an option", "Option indicated not part of selection", "Selection not part of options", "Written in not part of option"]
gm = ["GM", "GUN", "Gun Metal (not one of options)"]
remake = ["Re-make", "Re-male"]

##create a randomizer for delivery date
file["DATE SENT TO POG"] = pd.to_datetime(file["DATE SENT TO POG"])
file["TIME SENT TO POG"] = file["TIME SENT TO POG"].str.replace(' ', '')
def deldate(date_sent, duration):
    date_sent = date_sent.date()
    adddate = date_sent + datetime.timedelta(days=duration)
    deldatetime = pd.to_datetime(adddate)
    deldate = deldatetime.date()
    return deldate
test_date = datetime.datetime(2023, 1, 1)

##apply 
for x in range(len(file)):
    if file.iat[x, 0] == '7:396am': file.iat[x, 0] = '7:39am'
    if file.iat[x, 2] == '3/31/23:9:57am': file.iat[x, 2] = '3/31/23 9:57am'
    if file.iat[x, 2] == '5/23/23:12:02pm': file.iat[x, 2] = '5/23/23 12:02pm'
    if file.iat[x, 2] == '11/27/23-3:.36pm': file.iat[x, 2] = '11/27/23 3:36pm'
    file.iat[x, 2] = pd.to_datetime(file.iat[x, 2])
    if "2026" in str(file.iat[x, 2]): file.iat[x, 2] = file.iat[x, 2].replace(year=2023)
    if file.iat[x, 6] not in frame: file.iat[x, 6] = random.choice(frame)
    if (file.iat[x, 7] == 0) or (file.iat[x, 7] == "14"): file.iat[x, 7] = random.randint(50, 66) ##preserve space for outliers
    if file.iat[x, 8] == 0: file.iat[x, 8] = random.choice(colors)
    if file.iat[x, 6] == "SW06": file.iat[x, 8] = "BROWN/ORANGE"
    if file.iat[x, 8] == "BRN/OR": file.iat[x, 8] = "BROWN/ORANGE"
    if file.iat[x, 8] == "Bronx": file.iat[x, 8] = "BROWN"
    if file.iat[x, 8] == "Gold": file.iat[x, 8] = "GOLD"
    if file.iat[x, 8] == "Grey": file.iat[x, 8] = "GREY"
    if file.iat[x, 8] in gm: file.iat[x, 8] = "GUN METAL"
    if file.iat[x, 8] in nan: file.iat[x, 8] = "NOT INDICATED"
    if file.iat[x, 10] in remake: file.iat[x, 10] = "Remake"
    file.iat[x, 0] = datetime.datetime.strptime(file.iat[x, 0],'%I:%M%p').time()
    if file.iat[x, 2] < test_date: file.iat[x, 2] = file.iat[x, 1] + datetime.timedelta(days=random.randint(1, 5), hours=random.randint(0, 18), minutes=random.randint(0, 60),seconds=random.randint(0, 60))
    file.iat[x, -1] = deldate(file.iat[x, 2], random.randint(15, 60))

file["DATETIME SENT TO POG"] = pd.to_datetime(file["DATE SENT TO POG"].astype(str) + ' ' + file["TIME SENT TO POG"].astype(str))
file["POG CONFIRMATION RECEIPT OF ORDER\n(DATE & TIME)"] = pd.to_datetime(file["POG CONFIRMATION RECEIPT OF ORDER\n(DATE & TIME)"])
file["DATETIME SENT TO POG"] = pd.to_datetime(file["DATETIME SENT TO POG"])
file["Delivery Date"] = pd.to_datetime(file["Delivery Date"])
file["DAYS TO CONFIRM"] = (file["POG CONFIRMATION RECEIPT OF ORDER\n(DATE & TIME)"] - file["DATETIME SENT TO POG"]).dt.days
file["DAYS SHIPPED"] = (file["Delivery Date"] - file["POG CONFIRMATION RECEIPT OF ORDER\n(DATE & TIME)"]).dt.days

file.to_excel("/Users/m.shen/Desktop/Baruch College/MTA X TLDP Remote Internship/cleaned_Eyewear Tracking File Data-Year 2023.xlsx")
##use dataframe for data cleaning
##keep date & time, form# as ID
##delete columns X-AA as we have no access to the previous sheet
##delete unused columns
##leave duplicate tickets
##clean data - Not Found, 0, N/A...
##POG = company name
##(goggle) frame is not the same as color (except for SW06=B/O) = if()
##for blank cells & delivery date, use dummy data instead = random()