import csv
import xml.etree.ElementTree as ET
import urllib.request
import datetime as dt

import xlsxwriter



def xml_file_to_list():
    xml = urllib.request.urlopen("https://paikat.te-palvelut.fi/tpt-api/tyopaikat.rss?alueet=Kerava,Helsinki,Vantaa&ilmoitettuPvm=3&vuokrapaikka=---")
    tree = ET.parse(xml)
    root = tree.getroot()

    del_titles =["opettaja", "johtaja", "päällikkö", "kokki", "myyjä", "siivooja", "esimies", "rehtori", "lääkäri",
                 "lehtori", "lärare", "markkinointi", "myynti", "sosiaaliohjaaja", "asiakas", "putkiasentaja",
                 "kuljettaja", "sairaanhoitaja", "kätilö", "terapeutti", "hieroja", "tarjoilija",
                 "kampaaja", "lastenhoi", "varhaiskasvatu", "hammashoitaja", "henkilökohtainen avustaja", "lähihoitaja",
                 "kirvesmies", "asentaja", "hitsaaja"]

    time_cut = dt.datetime(2021, 2, 18, 14, 00, 00) #vvvv,kk,pp,hh,mm,ss
    list = []

    for channel in root:
        # print("channel: ", channel)
        for item in channel.findall("item"):
            data ={}
            title = item.find("title").text
            title_list = title.split(",")  # 0=Työn nimi, -1 = paikkakunta, kaikki välillä oleva on höttöä
            for x in del_titles:
                if x in title_list[0].lower():
                    break
            else: # Continue if the inner loop wasn't broken.
                url = item.find("link").text
                pub_date_text = item.find("pubDate").text
                if before_time_cut(time_cut, pub_date_text):
                    continue

                data["Otsikko"] = title_list[0]
                data["Linkki"] = url
                data["Lisätietoja"] = ",".join(title_list[1:-1])
                data["Paikkakunta"] = title_list[-1]
                data["Julkaistu"] = dt.datetime.strptime(pub_date_text, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y %m %d %H:%M:%S')
                list.append(data)

            continue # Inner loop was broken, continue the outer.

        return list

# def get_time_obj(text:str):
#     time_obj = dt.datetime.strptime(text, '%a, %d %b %Y %H:%M:%S %z')
#     return time_obj

def before_time_cut(time_cut,time:str):
    time_obj = dt.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
    # time_obj = dt.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y %m %d %H:%M:%S')
    # time_obj = dt.datetime.strptime(time_obj, '%Y %m %d %H:%M:%S')
    if time_obj < time_cut:
        return True
    return False


def list_to_csv(data:list):
    csv_file = "te_palvelut.csv"
    with open(csv_file, "w",newline="") as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter = ";")
        writer.writeheader()
        writer.writerows(data)


def list_to_excel(data:list):
    workbook = xlsxwriter.Workbook("te_palvelut_excel.xlsx")
    worksheet = workbook.add_worksheet()
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

if __name__ == '__main__':
    data = xml_file_to_list()
    # print(data)
    list_to_csv(data)
    list_to_excel(data)