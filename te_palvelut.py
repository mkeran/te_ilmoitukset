import csv
import logging
import xml.etree.ElementTree as ET
import urllib.request
import datetime as dt
import openpyxl.worksheet.worksheet as ws
import openpyxl
import xlsxwriter
from openpyxl.styles import Font

###Versio, joka hakee tiedot usein ja lisää edelliseen tiedostoon uudet ilmoitukset

logger = logging.getLogger(__name__)


def xml_file_to_list(url1: str):
    xml = urllib.request.urlopen(url1)
    tree = ET.parse(xml)
    root = tree.getroot()

    del_titles = get_del_titles()

    last_time = get_last_time_on_file()
    time_before_latest = False
    list = []
    count_skipped_items = 0

    for channel in root:
        for item in channel.findall("item"):
            pub_date_text = item.find("pubDate").text
            if before_time_cut(last_time, pub_date_text):
                time_before_latest = True
                continue

            title: str = item.find("title").text
            if title.startswith("Lisää ilmoituksia"):
                continue
            title_list = title.split(",")  # 0=Työn nimi, -1 = paikkakunta, kaikki välillä oleva on höttöä
            for x in del_titles:
                if x in title_list[0].lower():
                    count_skipped_items += 1
                    break
            else: # Continue if the inner loop wasn't broken.
                url = item.find("link").text

                data = {}
                data["Otsikko"] = title_list[0]
                data["Linkki"] = url
                data["Lisätietoja"] = ",".join(title_list[1:-1])
                data["Paikkakunta"] = title_list[-1]
                data["Julkaistu"] = dt.datetime.strptime(pub_date_text, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y %m %d %H:%M:%S')
                list.append(data)

            continue # Inner loop was broken, continue the outer.

        if time_before_latest == False:
            print("Edellisestä latauksesta liian kauan")
            logger.info("Dataa haettu liian harvoin")
        newtime = channel.findall("item")[0].find("pubDate").text

        logger.info(f"Uusien lisättävien ilmoitusten määrä: {len(list)}")
        logger.info(f"Hylättyjen ilmoitusten määrä: {count_skipped_items}")
        print(f"Uusien lisättävien ilmoitusten määrä: {len(list)}")
        print(f"Hylättyjen ilmoitusten määrä:", count_skipped_items)
        return list, newtime


def get_last_time_on_file():
    with open("last_time_obj.txt") as f:
        time = f.read()
        # time_obj = dt.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
        return time


def set_last_time_on_file(time:str):
    with open("last_time_obj.txt", "w") as f:
        f.write(time)


def before_time_cut(time_cut:str, time:str):
    time_cut_obj = dt.datetime.strptime(time_cut, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
    time_obj = dt.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
    # time_obj = dt.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y %m %d %H:%M:%S')
    # time_obj = dt.datetime.strptime(time_obj, '%Y %m %d %H:%M:%S')
    if time_obj < time_cut_obj:
        return True
    return False


def get_del_titles():
    with open("del_titles.txt", encoding="UTF-8") as f:
        list = f.read().split("\n")
    return list


def list_to_csv(data:list):
    csv_file = "te_palvelut.csv"
    with open(csv_file, "w",newline="") as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter = ";")
        writer.writeheader()
        writer.writerows(data)


def list_to_new_excel(data:list, file:str):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet(name = "Sheet1")
    cell_format = workbook.add_format()
    cell_format.set_bold()

    worksheet.write_row(0, 0, data[0].keys(), cell_format=cell_format)

    row = 1
    for dicti in data:
        worksheet.write_row(row, 0, dicti.values())
        row += 1

    #muotoilu:
    worksheet.set_column(0, 2, 50)
    worksheet.set_column(3, 4, 30)

    workbook.close()


def add_list_to_old_excel(data: list, file: str):
    workbook = openpyxl.load_workbook(file)
    worksheet: ws.Worksheet = workbook["Sheet2"]
    row = worksheet.max_row + 1

    print("nrows: ", row)

    #luku loppuu, kirjoitus alkaa

    for dicti in data[::-1]:
        worksheet.append(list(dicti.values()))  #(row, 0, dicti.values())
        cell = worksheet.cell(row, 2)
        cell.hyperlink = cell.value
        cell.font = Font(underline='single', color='0563C1')
        row += 1
    workbook.save(file)
    workbook.close()


def clear_excel(file: str):
    workbook = openpyxl.load_workbook(file)
    worksheet: ws.Worksheet = workbook["Sheet2"]

    worksheet.delete_rows(2, worksheet.max_row) ##!!!!!!!HUOM muuta ensimmäinen parametri (190)-->2

    workbook.save(file)
    workbook.close()


def excel_too_full(file:str):
    workbook = openpyxl.load_workbook(file)
    worksheet: ws.Worksheet = workbook["Sheet2"]
    bool = False
    if worksheet.max_row > 2000:
        bool = True
    workbook.close()
    return bool


def kokeiluxy_main():
    pass
    # set_last_time_on_file("Fri, 21 Feb 2021 14:15:50 +0200")
    # url = "https://paikat.te-palvelut.fi/tpt-api/tyopaikat.rss?alueet=Helsinki,Vantaa,Kerava&ilmoitettuPvm=3&vuokrapaikka=---"
    # data = xml_file_to_list(url)
    # print("Datan koko:", len(data))
    # # print(data)
    # # list_to_csv(data)
    # excel_file = "te_palvelut_excel.xlsx"
    # # list_to_new_excel(excel_file)
    # clear_excel(excel_file)
    # add_list_to_old_excel(data, excel_file)


def main():
    # logger.info("ollaan mainissa")
    url = "https://paikat.te-palvelut.fi/tpt-api/tyopaikat.rss?alueet=Helsinki,Vantaa,Kerava&ilmoitettuPvm=3&vuokrapaikka=---"
    excel_file = "te_palvelut_excel.xlsx"
    # if excel_too_full(excel_file):
    #     clear_excel(excel_file)
    logger.info(f"haetaan tiedot {get_last_time_on_file()} lähtien")
    data, newtime = xml_file_to_list(url)
    try:
        add_list_to_old_excel(data, excel_file)
    except Exception:
        print("Tietojen vienti exceliin epäonnistui, aikaolio resetoitu")
        logger.info("Tietojen vienti exceliin epäonnistui")
    else:
        print("Uusi aika asetettu")
        set_last_time_on_file(newtime)


if __name__ == '__main__':
    # clear_excel("te_palvelut_excel.xlsx")
    main()