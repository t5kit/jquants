import jquants
from getpass import getpass
import os
import pandas as pd
from datetime import datetime, timedelta
import sys
import pytz

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

    if '-until' in sys.argv:
        until_index = sys.argv.index('-until') + 1
        until_date_str = sys.argv[until_index]

        try:
            until_date = datetime.strptime(until_date_str, '%Y%m%d')
            until_date_str = until_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please provide the date in YYYYMMDD format.")
            exit()

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

    # 日本のタイムゾーンを取得
    jst = pytz.timezone('Asia/Tokyo')
    yesterday = datetime.now(jst) - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    date_list = markets_trading_calendar[
        (markets_trading_calendar["Date"] >= until_date_str)&
        (markets_trading_calendar["Date"] <= yesterday_str)&
        (markets_trading_calendar["HolidayDivision"] != "0")]["Date"].values.tolist()

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
