import schedule, time, os, json, requests
from dotenv import load_dotenv
from datetime import datetime
from Naked.toolshed.shell import execute_js

load_dotenv()
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
DATAPULL_INTERVAL_MINUTES = 1
DEBUG = False

# Get Account's Opensea Collection Data
def getAccountData(address=WALLET_ADDRESS):
    url = f"https://api.opensea.io/api/v1/collections?asset_owner={address}&offset=0&limit=300"
    data = requests.request("GET", url).json()
    return data

# Isolate important asset data for each inventory item
def getAssetsData(account_data):
    assets_data = []
    for item in account_data:
        asset = {}

        # Get important asset data
        try:
            address = item['primary_asset_contracts'][0]['address']
        except:
            address = 'Contract not found'
            a_name = None
            a_desc = None
            a_link = None

        if address != 'Contract not found':
            url = f"https://api.opensea.io/api/v1/asset/{address}/1/"
            response = requests.request("GET", url)
            asset_data = response.json()
            a_name = asset_data['name']
            a_desc = asset_data['description']
            a_link = url

        # Get important collection data
        c_name = item['name']
        c_desc = item['description']

        # Get asset average value
        stats = item['stats']
        if stats.get('one_day_average_price'): value = item['stats']['one_day_average_price']
        elif stats.get('seven_day_average_price'): value = item['stats']['seven_day_average_price']
        elif stats.get('average_price'): value = item['stats']['average_price']
        else: value = 0

        asset['name'] = a_name or c_name
        asset['avg_value'] = value
        asset['contract_link'] = a_link
        asset['collection_name'] = c_name
        asset['collection_description'] = c_desc
        assets_data.append(asset)
    return assets_data

# Calculate total value of assets (in ETH)
def getTotalAssetsValue(assets_data):
    total_assets_value = 0
    for asset in assets_data:
        total_assets_value += asset['avg_value']
    return total_assets_value

# Get user ETH balance
def getEthBalance(address=WALLET_ADDRESS):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}'
    bal_eth = int(requests.request("GET", url).json()['result'])
    bal_eth = bal_eth / (10 ** 18)
    return bal_eth

# Get current price of ETH
def getEthPrice():
    token_url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
    price_eth = json.loads(requests.request("GET", token_url).text)['ethereum']['usd']
    return price_eth

# Pull all important account data
def getPortfolioData():
    account_data = getAccountData()
    assets_data = getAssetsData(account_data)
    assets_value = getTotalAssetsValue(assets_data)
    eth_balance = getEthBalance()
    eth_price = getEthPrice()

    portfolio = {
        'unix_timestamp': time.mktime(datetime.now().timetuple()),
        'account_data': account_data,
        'assets_data': {
            'assets': assets_data,
            'total_average_value': assets_value,
        },
        'eth_balance': {
            'bal': eth_balance,
            'price': eth_price
        }
    }
    return portfolio

# Write over portfolio json
def overwritePortfolioJson(portfolio={}, path='data.json'):
    with open(f'{path}', 'w') as f: json.dump(portfolio, f)

# Push portfolio json to Streamr blockchain via js sdk
def pushToStreamr():
    try:
        portfolio = getPortfolioData()
        overwritePortfolioJson(portfolio)
        if DEBUG: print(portfolio)
        execute_js('node/app.js')
    except Exception as e:
        print(e)


schedule.every(DATAPULL_INTERVAL_MINUTES).minutes.do(pushToStreamr)
while True: schedule.run_pending()
