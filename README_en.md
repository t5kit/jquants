[JP](README.md) / EN

# JQuants Python Client
This Python client serves as a wrapper for easy access to the [J-Quants API](https://jpx.gitbook.io/j-quants-en/), facilitating the retrieval, analysis of financial data, and the development of algorithmic trading strategies.

# Features
- Fetch financial data such as stock prices and corporate information.
- Handle user authentication and automatic token renewal.
- Provide access to a wide range of financial information endpoints.

# Prerequisites
To use this client, you'll need an account with J-Quants. Additionally, you must obtain an API key (Email and Password).

# Installation
The `requests` module is a prerequisite. Install it using the command below:

```bash
pip install requests
```

# Usage
1. Import the JQuants class.
2. Create a JQuants instance using your Email and Password.
3. Use the provided methods to retrieve the necessary financial data.

## sample code

```python
from jquants import JQuants

# Create a JQuants instance
email = "your_email@example.com"
password = "your_password"
jq = JQuants(email, password)

# Retrieve listing information for stocks
listed_info = jq.listed_info()

# Get daily quotes for a specific stock
daily_quotes = jq.prices_daily_quotes(code="9434", date_from="20240101", date_to="20240131")

print(listed_info)
print(daily_quotes)
```

# Retrieving All Data
The script `get_all_data.py` is provided to fetch all available data.

```bash
python get_all_data.py
```

There's a test mode that outputs the loop process only once at the beginning to check the structure of the output file.

```bash
python get_all_data.py -test
```

# Data Check Program
There have been cases where data was missing after uploading the acquired data to Google Drive or similar platforms, possibly due to the large number of files or the size of the data. A program to check the data is attached.

```bash
python data_checker.py path/to/directory
```

To perform a data check on the Google Drive side, please clone this repository in Google Colaboratory as follows and then proceed with the data check.

```bash
!git clone https://github.com/t5kit/jquants.git

!python /content/jquants/data_checker.py path/to/directory
```

# API Correspondence Table
| API | Endpoints | Methods |
|:--------|:--------:|--------:|
| [List of Listed Stocks](https://jpx.gitbook.io/j-quants-en/api-reference/listed_info) | /listed/info | listed_info |
| [Stock Prices (Open, High, Low, Close)](https://jpx.gitbook.io/j-quants-en/api-reference/daily_quotes) | /prices/daily_quotes | prices_daily_quotes |
| [Morning Session Prices (Open, High, Low, Close)](https://jpx.gitbook.io/j-quants-en/api-reference/prices_am) | /prices/prices_am | prices_prices_am |
| [Information by Investment Sector](https://jpx.gitbook.io/j-quants-en/api-reference/trades_spec) | /markets/trades_spec | markets_trades_spec |
| [Credit Transaction Weekend Balance](https://jpx.gitbook.io/j-quants-en/api-reference/weekly_margin_interest) | /markets/weekly_margin_interest | markets_weekly_margin_interest |
| [Short Selling Ratio by Industry](https://jpx.gitbook.io/j-quants-en/api-reference/short_selling) | /markets/short_selling | markets_short_selling |
| [Trading Breakdown Data](https://jpx.gitbook.io/j-quants-en/api-reference/breakdown) | /markets/breakdown | markets_breakdown |
| [Trading Calendar](https://jpx.gitbook.io/j-quants-en/api-reference/trading_calendar) | /markets/trading_calendar | markets_trading_calendar |
| [Index Prices (Open, High, Low, Close)](https://jpx.gitbook.io/j-quants-en/api-reference/indices) | /indices | indices |
| [TOPIX Index Prices (Open, High, Low, Close)](https://jpx.gitbook.io/j-quants-en/api-reference/topix) | /indices/topix | indices_topix |
| [Financial Information](https://jpx.gitbook.io/j-quants-en/api-reference/statements) | /fins/statements | fins_statements |
| [Financial Statements (Balance Sheet / Profit & Loss)](https://jpx.gitbook.io/j-quants-en/api-reference/statements-1) | /fins/fs_details | fins_fs_details |
| [Dividend Information](https://jpx.gitbook.io/j-quants-en/api-reference/dividend) | /fins/dividend | fins_dividend |
| [Scheduled Earnings Announcement Dates](https://jpx.gitbook.io/j-quants-en/api-reference/announcement) | /fins/announcement | fins_announcement |
| [Option Prices (Open, High, Low, Close)](https://jpx.gitbook.io/j-quants-en/api-reference/index_option) | /option/index_option | option_index_option |

# License
This project is released under the MIT License. For details, please see the [LICENSE](LICENSE) file.
