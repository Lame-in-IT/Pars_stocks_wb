import time
import psycopg2
from config import config_wb as settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import requests
import logging
import json
import openpyxl
import schedule

from get_date import gey_list_date_365, gey_list_date_90, gey_list_date_30, get_list_date_7, gey_list_date_60, get_list_date_14

def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    return create_engine(url, pool_size=50, echo=False)

def get_engine_from_settings():  # sourcery skip: raise-specific-error
    keys = ["user", "password", "host", "port", "database"]
    if any(key not in keys for key in settings.keys()):
        raise Exception("Файл настроек не правельный")
    return get_engine(settings["user"],
                      settings["password"],
                      settings["host"],
                      settings["port"],
                      settings["database"])
    
def get_session():
    engine = get_engine_from_settings()
    return sessionmaker(bind=engine)() # type: ignore


def connect_bd():
    return psycopg2.connect(
        database=settings["database"],
        user=settings["user"],
        password=settings["password"],
        host=settings["host"],
        port=settings["port"],
    )

def get_api_user():
    try:
        table_api = pd.read_sql("SELECT statistic_api FROM api_users", con=get_engine_from_settings())
        return list(table_api["statistic_api"])
    except Exception as err:
        logging.exception(err)
        
def record_bd_stocks():
    try:
        connection = connect_bd()
        connection.autocommit = True
        cursor = connection.cursor()
        api_all_user = get_api_user()
        # date_365 = gey_list_date_365()
        for api_us in api_all_user:
            url_stocks = f"https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom={gey_list_date_365()}"
            req_stocks_wb = requests.get(url=url_stocks, headers={'Content-Type': 'application/json', 'Authorization': f'{api_us}'}).json() 
            # with open("Данные наличия остатков на складах.json", "w", encoding="utf_8") as file_create:
            #     json.dump(req_stocks_wb, file_create, indent=4, ensure_ascii=False)
            # Удаление записи
            sql_delete_query = """Delete from stocks_users where api_user = %s"""
            cursor.execute(sql_delete_query, (api_us,))
            for data_bd in req_stocks_wb: # заполняем бд данными об остатках
                cursor.execute("""INSERT INTO stocks_users(lastchangedate, warehousename, supplierarticle,
                            nmid, barcode, quantity, inwaytoclient, inwayfromclient, quantityfull,
                            category, subject, brand, techsize, price, discount, issupply,
                            isrealization, sccode, api_user)
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                [data_bd["lastChangeDate"].split("T")[0], data_bd["warehouseName"],
                                data_bd["supplierArticle"], data_bd["nmId"], data_bd["barcode"],
                                data_bd["quantity"], data_bd["inWayToClient"], data_bd["inWayFromClient"],
                                data_bd["quantityFull"], data_bd["category"], data_bd["subject"],
                                data_bd["brand"], data_bd["techSize"], data_bd["Price"], data_bd["Discount"],
                                data_bd["isSupply"], data_bd["isRealization"], data_bd["SCCode"],
                                api_us])
                print("Добавлено stocks_users")
            time.sleep(3)
        record_bd_sales()
    except Exception as err:
        logging.exception(err)
        
def record_bd_sales():
    try:
        connection = connect_bd()
        connection.autocommit = True
        cursor = connection.cursor()
        api_all_user = get_api_user()
        # lostpast_90_date = gey_list_date_90()
        for api_us in api_all_user:
            url_WB_prodaji = f"https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={gey_list_date_90()}"
            req_prodaji = requests.get(url=url_WB_prodaji, headers={'Content-Type': 'application/json', 'Authorization': f'{api_us}'}).json()
            # with open("Статистика продаж за неделю WB.json", "w", encoding="utf_8") as file_create:
            #     json.dump(req_prodaji, file_create, indent=4, ensure_ascii=False)
            table_df = pd.read_sql(
                f"SELECT * FROM sales_users WHERE api_user = '{api_us}'", con=get_engine_from_settings())
            list_srid = list(table_df["srid"])
            for data_bd in req_prodaji: # заполняем бд данными об продаж
                if data_bd["srid"] not in list_srid:
                    cursor.execute("""INSERT INTO sales_users(date, lastchangedate, supplierarticle, techsize,
                                barcode, totalprice, discountpercent, issupply, isrealization, promocodediscount,
                                warehousename, countryname, oblastokrugname, regionname, incomeid, saleid, saleid_mini,
                                odid, spp, forpay, finishedprice, pricewithdisc, nmid, subject, category,
                                brand, isstorno, gnumber, sticker, srid, api_user)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                    [data_bd["date"].split("T")[0], data_bd["lastChangeDate"].split("T")[0],
                                    data_bd["supplierArticle"], data_bd["techSize"], data_bd["barcode"],
                                    data_bd["totalPrice"], data_bd["discountPercent"], data_bd["isSupply"],
                                    data_bd["isRealization"], data_bd["promoCodeDiscount"], data_bd["warehouseName"],
                                    data_bd["countryName"], data_bd["oblastOkrugName"], data_bd["regionName"],
                                    data_bd["incomeID"], data_bd["saleID"], data_bd["saleID"][0], data_bd["odid"], data_bd["spp"],
                                    data_bd["forPay"], data_bd["finishedPrice"], data_bd["priceWithDisc"],
                                    data_bd["nmId"], data_bd["subject"], data_bd["category"], data_bd["brand"],
                                    data_bd["IsStorno"], data_bd["gNumber"], data_bd["sticker"], data_bd["srid"],
                                    api_us])
                    print("Добавлено sales_users")
            time.sleep(3)
        no_sales_for_7()
    except Exception as err:
        logging.exception(err)
        
def no_sales_for_7():
    try:
        connection = connect_bd()
        connection.autocommit = True
        cursor = connection.cursor()
        list_date_7 = get_list_date_7()
        api_all_user = get_api_user()
        sql_delete_query = """Delete from no_sales_for_7 where api_user = %s"""
        for api_user in api_all_user:
            cursor.execute(sql_delete_query, (api_user,))
            list_nmid = []
            table_df = pd.read_sql(
                    f"SELECT * FROM stocks_users WHERE api_user = '{api_user}'", con=get_engine_from_settings())
            for item_nmid in table_df["nmid"]:
                if item_nmid not in list_nmid:
                    list_nmid.append(item_nmid)
            for wb_sales in list_nmid:
                table_data = pd.read_sql(
                    f"SELECT * FROM stocks_users WHERE api_user = '{api_user}' AND nmid = '{wb_sales}'", con=get_engine_from_settings())
                table_wb_sales = pd.read_sql(
                    f"SELECT * FROM sales_users WHERE date IN('{list_date_7[0]}', '{list_date_7[1]}', '{list_date_7[2]}', '{list_date_7[3]}', '{list_date_7[4]}', '{list_date_7[5]}', '{list_date_7[6]}', '{list_date_7[7]}') AND (api_user = '{api_user}' AND nmid = {wb_sales}  AND saleid_mini = 'S')", con=get_engine_from_settings())
                cursor.execute("""INSERT INTO no_sales_for_7(nmId, supplierArticle, subject,
                               stocks_user, sales_user, link_site, api_user)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s)""", 
                                    [wb_sales, list(table_data["supplierarticle"])[0], list(table_data["subject"])[0],
                                     sum(list(table_data["quantity"])), len(list(table_wb_sales["saleid"])),
                                     f"https://www.wildberries.ru/catalog/{wb_sales}/detail.aspx", api_user])
                print("Добавлено no_sales_for_7")
            time.sleep(3)
        add_leftovers()
    except Exception as err:
        logging.exception(err)
        
def add_leftovers():
    try:
        list_date_7 = get_list_date_14()
        list_date_30 = gey_list_date_60()
        connection = connect_bd()
        connection.autocommit = True
        cursor = connection.cursor()
        api_all_user = get_api_user()
        sql_delete_query = """Delete from add_leftovers_wb_user where api_user = %s"""
        for api_user in api_all_user:
            cursor.execute(sql_delete_query, (api_user,))
            table_warehouse = pd.read_sql(
                    f"SELECT * FROM stocks_users WHERE api_user = '{api_user}'", con=get_engine_from_settings())
            for index_warehouse, item_warehouse in enumerate(table_warehouse["warehousename"]):
                table_sales_7 = pd.read_sql(
                        f"SELECT * FROM sales_users WHERE date IN('{list_date_7[0]}', '{list_date_7[1]}', '{list_date_7[2]}', '{list_date_7[3]}', '{list_date_7[4]}', '{list_date_7[5]}', '{list_date_7[6]}', '{list_date_7[7]}', '{list_date_7[8]}', '{list_date_7[9]}', '{list_date_7[10]}', '{list_date_7[11]}', '{list_date_7[12]}', '{list_date_7[13]}', '{list_date_7[14]}') AND (api_user = '{api_user}' AND nmid = {table_warehouse['nmid'][index_warehouse]}  AND saleid_mini = 'S' AND techsize = '{table_warehouse['techsize'][index_warehouse]}' AND warehousename = '{item_warehouse}')", con=get_engine_from_settings())
                table_sales_30 = pd.read_sql(
                        f"SELECT * FROM sales_users WHERE date IN('{list_date_30[0]}', '{list_date_30[1]}', '{list_date_30[2]}', '{list_date_30[3]}', '{list_date_30[4]}', '{list_date_30[5]}', '{list_date_30[6]}', '{list_date_30[7]}', '{list_date_30[8]}', '{list_date_30[9]}', '{list_date_30[10]}', '{list_date_30[11]}', '{list_date_30[12]}', '{list_date_30[13]}', '{list_date_30[14]}', '{list_date_30[15]}', '{list_date_30[16]}', '{list_date_30[17]}', '{list_date_30[18]}', '{list_date_30[19]}', '{list_date_30[20]}', '{list_date_30[21]}', '{list_date_30[22]}', '{list_date_30[23]}', '{list_date_30[24]}', '{list_date_30[25]}', '{list_date_30[26]}', '{list_date_30[27]}', '{list_date_30[28]}', '{list_date_30[29]}', '{list_date_30[30]}', '{list_date_30[31]}', '{list_date_30[32]}', '{list_date_30[33]}', '{list_date_30[34]}', '{list_date_30[35]}', '{list_date_30[36]}', '{list_date_30[37]}', '{list_date_30[38]}', '{list_date_30[39]}', '{list_date_30[40]}', '{list_date_30[41]}', '{list_date_30[42]}', '{list_date_30[43]}', '{list_date_30[44]}', '{list_date_30[45]}', '{list_date_30[46]}', '{list_date_30[47]}', '{list_date_30[48]}', '{list_date_30[49]}', '{list_date_30[50]}', '{list_date_30[51]}', '{list_date_30[52]}', '{list_date_30[53]}', '{list_date_30[54]}', '{list_date_30[55]}', '{list_date_30[56]}', '{list_date_30[57]}', '{list_date_30[58]}', '{list_date_30[59]}', '{list_date_30[60]}') AND (api_user = '{api_user}' AND nmid = {table_warehouse['nmid'][index_warehouse]}  AND saleid_mini = 'S' AND techsize = '{table_warehouse['techsize'][index_warehouse]}' AND warehousename = '{item_warehouse}')", con=get_engine_from_settings())
                cursor.execute("""INSERT INTO add_leftovers_wb_user(nmid, supplierarticle, subject,
                               techsize, warehousename, stocks_in_warehouse, sales_in_week,
                               sales_in_month, add_stocks_for_warehouse_in_7, 
                               add_stocks_for_warehouse_in_30, api_user)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                    [int(table_warehouse["nmid"][index_warehouse]), table_warehouse["supplierarticle"][index_warehouse],
                                     table_warehouse["subject"][index_warehouse], table_warehouse["techsize"][index_warehouse],
                                     item_warehouse, int(table_warehouse["quantity"][index_warehouse]),
                                     len(list(table_sales_7["saleid"])), len(list(table_sales_30["saleid"])),
                                     int(table_warehouse["quantity"][index_warehouse] - len(list(table_sales_7["saleid"]))),
                                     int(table_warehouse["quantity"][index_warehouse] - len(list(table_sales_30["saleid"]))),
                                     api_user])
            time.sleep(3)
    except Exception as err:
        logging.exception(err)
        
def main():
    schedule.every().day.at("06:00").do(record_bd_stocks)
    schedule.every().day.at("18:00").do(record_bd_stocks)
    while True:
        schedule.run_pending()
        
if __name__ == "__main__":
    main()