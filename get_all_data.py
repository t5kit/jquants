import jquants
from getpass import getpass
import os
import pandas as pd
from datetime import datetime, timedelta
import sys
import shutil

SECTOR_33_CODES = {
    "0050": "水産・農林業",
    "1050": "鉱業",
    "2050": "建設業",
    "3050": "食料品",
    "3100": "繊維製品",
    "3150": "パルプ・紙",
    "3200": "化学",
    "3250": "医薬品",
    "3300": "石油・石炭製品",
    "3350": "ゴム製品",
    "3400": "ガラス・土石製品",
    "3450": "鉄鋼",
    "3500": "非鉄金属",
    "3550": "金属製品",
    "3600": "機械",
    "3650": "電気機器",
    "3700": "輸送用機器",
    "3750": "精密機器",
    "3800": "その他製品",
    "4050": "電気・ガス業",
    "5050": "陸運業",
    "5100": "海運業",
    "5150": "空運業",
    "5200": "倉庫・運輸関連業",
    "5250": "情報・通信業",
    "6050": "卸売業",
    "6100": "小売業",
    "7050": "銀行業",
    "7100": "証券・商品先物取引業",
    "7150": "保険業",
    "7200": "その他金融業",
    "8050": "不動産業",
    "9050": "サービス業",
    "9999": "その他",
}

INDEX_CODES = {
    "0000": "TOPIX指数",
    "0028": "TOPIX Core30 指数",
    "0029": "TOPIX Large70 指数",
    "002A": "TOPIX 100 指数",
    "002B": "TOPIX Mid400 指数",
    "002C": "TOPIX 500 指数",
    "002D": "TOPIX Small 指数",
    "002E": "TOPIX 1000 指数",
    "0070": "東証グロース市場250指数（旧：東証マザーズ指数）",
    "0075": "東証REIT指数",
}

def message(msg: str):
    log_message = f"[{datetime.now()}] {msg}"
    print(log_message)

    log_file_path = "./data/log.txt"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message + "\n")

def make_dir(path: str):
    os.makedirs(path, exist_ok=True)

if __name__ == "__main__":
    test = False
    if '-test' in sys.argv:
        test = True

    email = os.getenv("JQUANTS_EMAIL")
    password = os.getenv("JQUANTS_PASSWORD")
    if not email:
        email = input("Enter your email address: ")
    if not password:
        password = getpass("Enter your password: ")

    jq = jquants.JQuants(email, password)

    make_dir("./data")

    message("markets_trading_calendar")
    ret = jq.markets_trading_calendar()
    markets_trading_calendar = pd.DataFrame(ret["trading_calendar"])
    markets_trading_calendar.to_csv(f"./data/markets_trading_calendar.csv", index=False)

    date_list = markets_trading_calendar[markets_trading_calendar["HolidayDivision"] != "0"]["Date"].values.tolist()
    # 昨日の日付を取得
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    # 昨日の日付がリスト内にあるか確認してインデックスを取得
    try:
        yesterday_index = date_list.index(yesterday_str)
        # 昨日までの日付リストに切り取る
        date_list = date_list[:yesterday_index]
    except ValueError:
        print("yesterday not in date_list.")

    message("listed_info")
    ret = jq.listed_info()
    listed_info = pd.DataFrame(ret["info"])
    listed_info.to_csv("./data/listed_info.csv", index=False)

    make_dir("./data/prices_daily_quotes")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"prices_daily_quotes date={date}")
        pagination_key = None
        
        output_path = f"./data/prices_daily_quotes/prices_daily_quotes_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'prices_daily_quotes_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.prices_daily_quotes(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.prices_daily_quotes(date=date)

                prices_daily_quotes = pd.DataFrame(ret["daily_quotes"])
                if not prices_daily_quotes.empty:
                    prices_daily_quotes.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break

    message("markets_trades_spec")
    pagination_key = None
    while True:
        try:
            if pagination_key:
                ret = jq.markets_trades_spec(pagination_key=pagination_key)
            else:
                ret = jq.markets_trades_spec()

            markets_trades_spec = pd.DataFrame(ret["trades_spec"])
            if not markets_trades_spec.empty:
                markets_trades_spec.to_csv(f"./data/markets_trades_spec.csv", mode='a', header=pagination_key is None, index=False)

            pagination_key = ret.get("pagination_key")
            if not pagination_key:
                break
        except Exception as e:
            message(e)
            break

    make_dir("./data/markets_weekly_margin_interest")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"markets_weekly_margin_interest date={date}")
        pagination_key = None

        output_path = f"./data/markets_weekly_margin_interest/markets_weekly_margin_interest_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'markets_weekly_margin_interest_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.markets_weekly_margin_interest(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.markets_weekly_margin_interest(date=date)

                markets_weekly_margin_interest = pd.DataFrame(ret["weekly_margin_interest"])
                if not markets_weekly_margin_interest.empty:
                    markets_weekly_margin_interest.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break

    make_dir("./data/markets_short_selling")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"markets_short_selling date={date}")
        pagination_key = None

        output_path = f"./data/markets_short_selling/markets_short_selling_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'markets_short_selling_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.markets_short_selling(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.markets_short_selling(date=date)

                markets_short_selling = pd.DataFrame(ret["short_selling"])
                if not markets_short_selling.empty:
                    markets_short_selling.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break

    make_dir("./data/markets_breakdown")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"markets_breakdown date={date}")
        pagination_key = None

        output_path = f"./data/markets_breakdown/markets_breakdown_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'markets_breakdown_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.markets_breakdown(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.markets_breakdown(date=date)

                markets_breakdown = pd.DataFrame(ret["breakdown"])
                if not markets_breakdown.empty:
                    markets_breakdown.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break

    make_dir("./data/indices")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"indices date={date}")
        pagination_key = None

        output_path = f"./data/indices/indices_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'indices_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.indices(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.indices(date=date)

                indices = pd.DataFrame(ret["indices"])
                if not indices.empty:
                    indices.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break
    
    message("indices_topix")
    pagination_key = None 
    while True:
        try:
            if pagination_key:
                ret = jq.indices_topix(pagination_key=pagination_key)
            else:
                ret = jq.indices_topix()

            indices_topix = pd.DataFrame(ret["topix"])
            if not indices_topix.empty:
                if pagination_key is None:
                    indices_topix.to_csv(f"./data/indices_topix.csv", index=False)
                else:
                    indices_topix.to_csv(f"./data/indices_topix.csv", mode='a', header=False, index=False)

            pagination_key = ret.get("pagination_key")
            if not pagination_key:
                break
        except Exception as e:
            message(e)
            break
        
    make_dir("./data/fins_statements")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"fins_statements date={date}")
        pagination_key = None

        output_path = f"./data/fins_statements/fins_statements_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'fins_statements_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.fins_statements(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.fins_statements(date=date)

                fins_statements = pd.DataFrame(ret["statements"])
                message(f"len= {len(fins_statements)}")
                if len(fins_statements) > 0:
                    fins_statements.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break

    make_dir("./data/fins_fs_details")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"fins_fs_details date={date}")
        pagination_key = None

        output_path = f"./data/fins_fs_details/fins_fs_details_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'fins_fs_details_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.fins_fs_details(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.fins_fs_details(date=date)

                fins_fs_details = pd.DataFrame(ret["fs_details"])
                message(f"len= {len(fins_fs_details)}")
                if len(fins_fs_details) > 0:
                    fins_fs_details.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break

    make_dir("./data/fins_dividend")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"fins_dividend date={date}")
        pagination_key = None

        output_path = f"./data/fins_dividend/fins_dividend_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'fins_dividend_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.fins_dividend(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.fins_dividend(date=date)

                fins_dividend = pd.DataFrame(ret["dividend"])
                message(f"len= {len(fins_dividend)}")
                if len(fins_dividend) > 0:
                    fins_dividend.to_csv(output_path, mode='a', header=pagination_key is None, index=False)
                    
                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break
            
    message("fins_announcement")
    pagination_key = None 
    while True:
        try:
            if pagination_key:
                ret = jq.fins_announcement(pagination_key=pagination_key)
            else:
                ret = jq.fins_announcement()
            
            fins_announcement = pd.DataFrame(ret["announcement"])
            fins_announcement.to_csv(f"./data/fins_announcement.csv", mode='a', header=pagination_key is None, index=False)

            pagination_key = ret.get("pagination_key")
            if not pagination_key:
                break
        except Exception as e:
            message(e)
            break

    make_dir("./data/option_index_option")
    break_for_loop = False
    for date in reversed(date_list):
        message(f"option_index_option date={date}")
        pagination_key = None

        output_path = f"./data/option_index_option/option_index_option_{date}.csv"
        if os.path.exists(output_path):
            message(f"file 'fins_dividend_{date}.csv' is exists.")
            break

        while True:
            try:
                if pagination_key:
                    ret = jq.option_index_option(date=date, pagination_key=pagination_key)
                else:
                    ret = jq.option_index_option(date=date)
                
                option_index_option = pd.DataFrame(ret["index_option"])
                option_index_option.to_csv(output_path, mode='a', header=pagination_key is None, index=False)

                pagination_key = ret.get("pagination_key")
                if not pagination_key:
                    break
            except Exception as e:
                message(e)
                if "This API is not available on your subscription." in str(e):
                    break_for_loop = True
                    break
        if break_for_loop:
            break
        if test:
            break
    exit()
