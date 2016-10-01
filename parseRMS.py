import gspread
# import gdata
import urllib
import pandas as pd
import time
from oauth2client.service_account import ServiceAccountCredentials

columns = [('Sail nr.', 1, 'SAILNUMB', 'A'),('Class', 2, '', 'B'), ('Name', 3, 'NAME', 'C'),
           ('Owner', 5, 'OWNER', 'D'), ('Type', 6, 'TYPE', 'E'),
           ('Year', 7, 'YEAR', 'F'), ('LOA', 8, 'LOA', 'G'),
           ('CDL', 9, 'CDL', 'H'), ('TxtInsh.', 10, 'TMF', 'I'),
           ('TxtOffsh.', 11, 'TMF-OF', 'J')]

def add_date(wks):
    wks.update_cell(1, len(columns)+3, "Updated:")
    wks.update_cell(1, len(columns) + 4, time.strftime("%d/%m/%y, %H:%M:%S"))

def addHeader(wks):
    cells = wks.range('A1:J1') #TODO: find largest column
    for cell,t in zip(cells,columns):
        cell.value = t[0]
    wks.update_cells(cells)


def cell_list(wks, data, tuple):
    if tuple[2]=='':
        return
    cells = wks.range(tuple[3]+'2:'+tuple[3] + str(len(data.get(tuple[2])) + 1))
    for cell, val in zip(cells, data.get(tuple[2])):
        cell.value = val
    wks.update_cells(cells)


def addYachts(wks, data):
    for t in columns:
        cell_list(wks,data,t)


def add_class(wks, cdl1, cdl2):
    values_list = wks.col_values(8)[1:]
    cell_list = wks.range('B2:B' + str(len(data.get('TMF-OF')) + 1))
    for cell, val in zip(cell_list, values_list):
        if (float(val) >= cdl2):
            cell.value = "ORC1"
        elif (float(val) >= cdl1 and float(val) < cdl2):
            cell.value = "ORC2"
        else:
            cell.value = "ORC3"
    wks.update_cells(cell_list)


widths = [(17, 29), (29, 53), (53, 71), (107, 112), (148, 184), (292, 299), (346, 354), (1267, 1275), (1306, 1315)]
data = pd.read_fwf("http://data.orc.org/public/WPub.dll?action=DownRMS&CountryId=ISR",
                   colspecs=widths, header='infer', encoding='utf_8')

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ORC-Results-6fc8dcf259fe.json', scope)
gc = gspread.authorize(credentials)

wks = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1S0zaKu3JjvFwz585dRicAc9pjVrE7ghI2wjSeAdrjSs/edit?usp=sharing').sheet1
addHeader(wks)
addYachts(wks, data)
add_class(wks, 8.5, 9.5)
add_date(wks)