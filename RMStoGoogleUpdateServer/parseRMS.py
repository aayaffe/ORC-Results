"""
This file is used to parse RMS file and update a Google sheets file used in various scoring sheets.
Created by aayaffe
"""

import gspread
import pandas as pd
import time
from oauth2client.service_account import ServiceAccountCredentials
import os
import argparse
from google_sheets_updater import *


parser = argparse.ArgumentParser(description='Generate a table of current ORC rating in ISRAEL.')
parser.add_argument('cdr_splits', type=float, nargs='+',
                    help='The CDR split points for the ORC classes')
args = parser.parse_args()

class_split=args.cdr_splits

##### Makes it possible to run from any dir #####
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
################################################


columns = [('Sail nr.', 1, 'SAILNUMB', 'A'),('Name', 2, 'NAME', 'B'),('Class', 3, '', 'C'),
           ('Owner', 5, 'OWNER', 'D'), ('Type', 6, 'TYPE', 'E'),
           ('Year', 7, 'YEAR', 'F'), ('LOA', 8, 'LOA', 'G'),
           ('CDL', 9, 'CDL', 'H'), ('TxtInsh.', 10, 'TMF', 'I'),
           ('TxtOffsh.', 11, 'TMF-OF', 'J'),('Update.', 12, 'DD_MM_yyYY HH:MM:SS', 'K')]
#class_split = [0,8.5]



widths = [(17, 29), (29, 53), (53, 71), (107, 112), (148, 184), (292, 299), (346, 354), (1267, 1275), (1306, 1315), (272,292)]
data = pd.read_fwf("http://data.orc.org/public/WPub.dll?action=DownRMS&CountryId=ISR",
                   colspecs=widths, header='infer', encoding='utf_8')

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ORC-Results-6fc8dcf259fe.json', scope)
print("Openning google sheet.")
gc = gspread.authorize(credentials)

wks = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1S0zaKu3JjvFwz585dRicAc9pjVrE7ghI2wjSeAdrjSs/edit?usp=sharing').sheet1
print("Google sheet opened.")
addHeader(wks, columns)
print("Added headers.")
addYachts(wks, data, columns)
print("Added Yachts.")
add_class(wks,data, class_split)
print("Added classes with splits "+str(class_split)+ ".")
add_date(wks, columns)
print("Added update date.")
print("Done!\n" + time.strftime("%d/%m/%y, %H:%M:%S"))
