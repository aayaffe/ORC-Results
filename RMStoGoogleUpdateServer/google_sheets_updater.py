"""
This file contains the functions used to update the google sheets file
Created by aayaffe
"""
import time

def add_date(wks, columns):
    wks.update_cell(1, len(columns)+3, "Updated:")
    wks.update_cell(1, len(columns) + 4, time.strftime("%d/%m/%y, %H:%M:%S"))

def addHeader(wks, columns):
    cells = wks.range('A1:K1') #TODO: find largest column
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


def addYachts(wks, data, columns):
    for t in columns:
        cell_list(wks,data,t)


def add_class(wks,data, cdls):
    values_list = wks.col_values(8)[1:]
    cell_list = wks.range('C2:C' + str(len(data.get('TMF-OF')) + 1))
    cdls = sorted(cdls,reverse=True)
    cdls.append(0.0)
    for cell, val in zip(cell_list, values_list):
        for idx,cdl in enumerate(cdls):
            if float(val)>=cdl:
                cell.value = "ORC"+str(idx+1)
                break
    wks.update_cells(cell_list)