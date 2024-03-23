import requests
import json
from getpass import getpass
from datetime import datetime, timedelta
import os

class JQuants:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.refresh_token_info = self._load_token("refresh_token.json")
        self.id_token_info = self._load_token("id_token.json")

    def _load_token(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                token_info = json.load(f)
                if token_info["expiration_time"]:
                    token_info["expiration_time"] = datetime.fromisoformat(token_info["expiration_time"])
                return token_info
        else:
            return {"token": None, "expiration_time": None}

    def _save_token(self, token_info, filename):
        save_token_info = token_info.copy()
        if save_token_info["expiration_time"]:
            save_token_info["expiration_time"] = save_token_info["expiration_time"].isoformat()
        with open(filename, "w") as f:
            json.dump(save_token_info, f)

    def _request(self, endpoint, data=None, params=None):
        url = f"https://api.jquants.com/v1/{endpoint}"

        if endpoint == "token/auth_user":
            response = requests.post(url, data=json.dumps(data))
        elif endpoint.startswith("token/auth_refresh"):
            response = requests.post(url)
        else:
            if not self.refresh_token_info["token"] or self._token_expired(self.refresh_token_info["expiration_time"]):
                self._get_refresh_token()
            if not self.id_token_info["token"] or self._token_expired(self.id_token_info["expiration_time"]):
                self._get_id_token()

            headers = {'Authorization': f'Bearer {self.id_token_info["token"]}'}
            response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise ValueError(f"Failed to execute request: {response.text}")

        return response.json()

    def _get_refresh_token(self):
        data = {"mailaddress": self.email, "password": self.password}
        response_data = self._request("token/auth_user", data)
        self.refresh_token_info["token"] = response_data.get("refreshToken")
        self.refresh_token_info["expiration_time"] = datetime.now() + timedelta(weeks=1)  # 1 Week
        self._save_token(self.refresh_token_info, "refresh_token.json")

    def _get_id_token(self):
        self.id_token_info["expiration_time"] = datetime.now() + timedelta(hours=24)  # 24 Hours
        self._get_refresh_token()
        response_data = self._request(f"token/auth_refresh?refreshtoken={self.refresh_token_info['token']}")
        self.id_token_info["token"] = response_data.get("idToken")
        self._save_token(self.id_token_info, "id_token.json")

    def _token_expired(self, expiration_time):
        return expiration_time and datetime.now() > expiration_time

    def listed_info(self, code=None, date=None):
        params={}
        params["code"] = code
        params["date"] = date
        return self._request("listed/info", params=params)
    
    def prices_daily_quotes(self, code=None, date=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("prices/daily_quotes", params=params)
    
    def prices_prices_am(self, code=None, pagination_key=None):
        params={}
        params["code"] = code
        params["pagination_key"] = pagination_key
        return self._request("prices/prices_am", params=params)
    
    def markets_trades_spec(self, section=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["section"] = section
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("markets/trades_spec", params=params)
    
    def markets_weekly_margin_interest(self, code=None, date=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("markets/weekly_margin_interest", params=params)

    def markets_short_selling(self, sector33code=None, date=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["sector33code"] = sector33code
        params["date"] = date
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("markets/short_selling", params=params)

    def markets_breakdown(self, code=None, date=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("markets/breakdown", params=params)

    def markets_trading_calendar(self, holidaydivision=None, date_from=None, date_to=None):
        params={}
        params["holidaydivision"] = holidaydivision
        params["from"] = date_from
        params["to"] = date_to
        return self._request("markets/trading_calendar", params=params)
    
    def indices(self, code=None, date=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("indices", params=params)

    def indices_topix(self, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("indices/topix", params=params)

    def fins_statements(self, code=None, date=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["pagination_key"] = pagination_key
        return self._request("fins/statements", params=params)
    
    def fins_fs_details(self, code=None, date=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["pagination_key"] = pagination_key
        return self._request("fins/fs_details", params=params)
    
    def fins_dividend(self, code=None, date=None, date_from=None, date_to=None, pagination_key=None):
        params={}
        params["code"] = code
        params["date"] = date
        params["from"] = date_from
        params["to"] = date_to
        params["pagination_key"] = pagination_key
        return self._request("fins/dividend", params=params)
    
    def fins_announcement(self, pagination_key=None):
        params={}
        params["pagination_key"] = pagination_key
        return self._request("fins/announcement", params=params)
    
    def option_index_option(self, date=None, pagination_key=None):
        params={}
        params["date"] = date
        params["pagination_key"] = pagination_key
        return self._request("option/index_option", params=params)
    
if __name__ == "__main__":
    email = os.getenv("JQUANTS_EMAIL")
    password = os.getenv("JQUANTS_PASSWORD")
    if not email:
        email = input("Enter your email address: ")
    if not password:
        password = getpass("Enter your password: ")

    jquants = JQuants(email, password)

    # print("listed_info() ", jquants.listed_info())
    # print("listed_info(code=9434) ", jquants.listed_info())
    # print("listed_info(date=20240314) ", jquants.listed_info(date=20240314))
    # print("listed_info(date=20240314, code=9434) ", jquants.listed_info(date=20240314, code=9434))

    # print("prices_daily_quotes(date=20240314) ", jquants.prices_daily_quotes(date=20240314))
    # print("prices_daily_quotes(date_from=20240310, date_to=20240314) ", jquants.prices_daily_quotes(date_from=20240310, date_to=20240314))
    # print("prices_daily_quotes(date=20240314, pagination_key='Code.93080.Date.2024-03-14.') ", jquants.prices_daily_quotes(date=20240314, pagination_key="Code.93080.Date.2024-03-14."))
    # print("prices_prices_am() ", jquants.prices_prices_am())
    # print("prices_prices_am(code=9434) ", jquants.prices_prices_am(code=9434))

    # print("markets_trades_spec() ", jquants.markets_trades_spec())
    # print("markets_trades_spec(date_from=20240310, date_to=20240314) ", jquants.markets_trades_spec(date_from=20240310, date_to=20240314))
    # print("markets_trades_spec(section='TSEPrime', date_from=20240310, date_to=20240314) ", jquants.markets_trades_spec(section="TSEPrime", date_from=20240310, date_to=20240314))

    # print("markets_weekly_margin_interest(code=9434) ", jquants.markets_weekly_margin_interest(code=9434))
    # print("markets_weekly_margin_interest(date=20240308) ", jquants.markets_weekly_margin_interest(date=20240308))
    # print("markets_weekly_margin_interest(code=9434, date_from=20240301, date_to=20240314) ", jquants.markets_weekly_margin_interest(code=9434, date_from=20240301, date_to=20240314))

    # print("markets_short_selling(date=20240308) ", jquants.markets_short_selling(date=20240308))
    # print("markets_short_selling(sector33code='0050') ", jquants.markets_short_selling(sector33code="0050"))
    # print("markets_short_selling(sector33code='0050', date=20240308) ", jquants.markets_short_selling(sector33code="0050", date=20240308))
    # print("markets_short_selling(sector33code='0050', date_from=20240301, date_to=20240314) ", jquants.markets_short_selling(sector33code="0050", date_from=20240301, date_to=20240314))

    # print("markets_breakdown(code=9434) ", jquants.markets_breakdown(code=9434))
    # print("markets_breakdown(code=9434, date_from=20240301, date_to=20240314) ", jquants.markets_breakdown(code=9434, date_from=20240301, date_to=20240314))
    # print("markets_breakdown(date=20240314) ", jquants.markets_breakdown(date=20240314))

    # print("markets_trading_calendar(holidaydivision=1) ", jquants.markets_trading_calendar(holidaydivision=1))
    # print("markets_trading_calendar(holidaydivision=1, date_from=20240301, date_to=20240314) ", jquants.markets_trading_calendar(holidaydivision=1, date_from=20240301, date_to=20240314))
    # print("markets_trading_calendar(date_from=20240301, date_to=20240314) ", jquants.markets_trading_calendar(date_from=20240301, date_to=20240314))
    # print("markets_trading_calendar() ", jquants.markets_trading_calendar())

    # print("indices(code='0000') ", jquants.indices(code="0000"))
    # print("indices(code='0000', date_from=20240301, date_to=20240314) ", jquants.indices(code="0000", date_from=20240301, date_to=20240314))
    # print("indices(date=20240314) ", jquants.indices(date=20240314))

    # print("indices_topix() ", jquants.indices_topix())
    # print("indices_topix(date_from=20240301, date_to=20240314) ", jquants.indices_topix(date_from=20240301, date_to=20240314))

    # print("fins_statements(code=9434) ", jquants.fins_statements(code=9434))
    # print("fins_statements(date=20240314) ", jquants.fins_statements(date=20240314))
    # print("fins_statements(code=1444, date=20240314) ", jquants.fins_statements(code=1444, date=20240314))

    # print("fins_fs_details(code=1444, date=20240314) ", jquants.fins_fs_details(code=1444, date=20240314))

    # print("fins_dividend(code=1444, date=20240314) ", jquants.fins_dividend(code=1444, date=20240314))

    # print("fins_announcement() ", jquants.fins_announcement())

    # print("option_index_option(date=20240314) ", jquants.option_index_option(date=20240314))

