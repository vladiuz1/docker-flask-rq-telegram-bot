import config
from flask import Flask, Response, request, jsonify, render_template
import json, re, requests, os, rq, atexit, urllib
from redis import Redis
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from web3 import Web3
from datetime import datetime

# init Redis
redis = Redis(host='fr-redis')
# init scheduler
scheduler = BackgroundScheduler()

# init rq queue
queue = rq.Queue(connection=Redis(host='fr-redis'))

def get_latest_block(default = False):
    if default:
        return 12471299
    latest_block = redis.get('latest_block')
    if not latest_block:
        latest_block = 12471299
    return int(latest_block)

def set_latest_block(block):
    redis.set('latest_block', block)

contract_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"tokenOwner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"until","type":"uint256"}],"name":"FreezeBalance","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"LockBalance","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"key","type":"string"},{"indexed":false,"internalType":"address","name":"value","type":"address"}],"name":"LogAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"key","type":"string"},{"indexed":false,"internalType":"string","name":"value","type":"string"}],"name":"LogString","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"key","type":"string"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"LogUint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"_to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"claimReserve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"conversionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"until","type":"uint256"}],"name":"freezeOwnTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"}],"name":"frozenBalanceOf","outputs":[{"internalType":"uint256","name":"frozenBalance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"}],"name":"frozenTimingOf","outputs":[{"internalType":"uint256","name":"until","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"_roleId","type":"uint256"}],"name":"getRoleAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"}],"name":"lockedBalanceOf","outputs":[{"internalType":"uint256","name":"lockedBalance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"newOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"pubSaleEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"pubSaleStart","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"restrictionEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"_newConversionRate","type":"uint256"}],"name":"setRate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"_roleId","type":"uint256"},{"internalType":"address","name":"_newAddress","type":"address"}],"name":"setRoleAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"_pubSaleStart","type":"uint256"},{"internalType":"uint256","name":"_pubSaleEnd","type":"uint256"},{"internalType":"uint256","name":"_restrictionEnd","type":"uint256"}],"name":"setTiming","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transferAnyERC20Token","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
qc = Web3().eth.contract('0x63120ccd7b415743e8753AfD167F5AD4A1732C43', abi = contract_abi)

def notifyTelegramGroupJob(message =  "this is a test message", parse_mode = 'markdown'):
    chat_id = config.Config.TELEGRAM_CHAT_ID
    api_key = config.Config.TELEGRAM_API_KEY
    url = f'https://api.telegram.org/bot{api_key}/sendMessage'
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': parse_mode}
    res = requests.post(url, data=data)
    return res.json()

def notify_and_update_block_count(msg, block):
    r = notifyTelegramGroupJob(msg)
    if r.get('ok') and block > get_latest_block():
        set_latest_block(block)

@scheduler.scheduled_job(name="Check Token Transfers", trigger="interval", seconds = 20)
def etherscan_get_token_transfers(address = '0x63120ccd7b415743e8753afd167f5ad4a1732c43', topic0 = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'):
    data = {
        'module': 'logs',
        'action': 'getLogs',
        'address': address,
        'fromBlock': get_latest_block() + 1,
        'topic0': topic0,
        'toBlock': 'latest',
        'sort': 'asc',
        'apikey': config.Config.ETHERSCAN_API_KEY
    }
    res = requests.get('https://api.etherscan.io/api?' + urllib.parse.urlencode(data))
    j = res.json()
    ret = []
    if j.get('message') == 'OK':
        for r in j.get('result', []):
            time = datetime.fromtimestamp(int(r.get('timeStamp'), 0)).strftime("%H:%M:%S")
            value = int(r.get('data','0x0'), 0)/10**18
            block = int(r.get('blockNumber','0x0'), 0)
            _from = hex(int(r.get('topics')[1],0))
            _to = hex(int(r.get('topics')[2],0))
            hash = r.get('transactionHash')
            fvalue = "{:,}".format(value)
            msg = f'QARK *{fvalue}*\n' \
                  f'@ {time} [ ](https://s2.coinmarketcap.com/static/img/coins/64x64/5858.png) \n' \
                  f'from: [{_from[:6]}..{_from[-4:]}](https://etherscan.io/address/{_from})\n' \
                  f'to: [{_to[:6]}..{_to[-4:]}](https://etherscan.io/address/{_to})\n' \
                  f'tx: [{hash[:6]}..{hash[-6:]}](https://etherscan.io/tx/{hash})\n'
            print(block, hash)
            queue.enqueue(notify_and_update_block_count, msg, block)
            ret.append((hash, time, block, _from, _to, "{:,}".format(value)))
    return ret

def etherscan_get_address_txs(address = '0x63120ccd7b415743e8753afd167f5ad4a1732c43'):
    data = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': get_latest_block() + 1,
        'endblock': 'latest',
        'sort': 'asc',
        'apikey': config.Config.ETHERSCAN_API_KEY
    }
    res = requests.get('https://api.etherscan.io/api?' + urllib.parse.urlencode(data))
    j = res.json()
    ret = []
    if j.get('message') == 'OK':
        for r in j.get('result', []):
            block = int(r.get('blockNumber',0))
            hash = r.get('hash')
            input = r.get('input')
            time = datetime.fromtimestamp(int(r.get('timeStamp'))).strftime("%H:%M:%S")
            if input:
                f = qc.decode_function_input(input)
                ret.append((block, hash, time, str(f[0]), f[1]))
    return ret

if "gunicorn" in os.environ.get("SERVER_SOFTWARE", "") or \
    os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    # Avoids running the schedule twice.
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

# init flask app
app = Flask(__name__)
# setup config
app.config.from_object("config.Config")

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/address')
def address_txs():
    return jsonify(etherscan_get_address_txs())

@app.route('/e')
def contract_evens():
    return jsonify(etherscan_get_token_transfers())

@app.route('/b')
def lb():
    return jsonify({'latest_block':get_latest_block()})

@app.route('/rb')
def rb():
    """
    reset latest block to defualt
    :return:
    """
    set_latest_block(get_latest_block(default=True))
    return jsonify({'latest_block':get_latest_block()})

@app.route('/msg')
def tm():
    r = notifyTelegramGroupJob('Another *test* message.')
    return jsonify(r)

@app.route('/sc/<string:command>')
@app.route('/sc/<string:command>/<string:job_id>')
def sched_control(command, job_id = None):
    """
    Little controller script
    :param command: the control command
    :param job_id: optional job id for job-related commands
    :return:
    """
    if command == 'pause':
        scheduler.pause()
    elif command == 'resume':
        scheduler.resume()
    elif command == 'start':
        scheduler.start()
    elif command == 'start_paused':
        scheduler.start(paused=True)
    elif command == 'jobs':
        return jsonify([( j.id, j.name, j.pending,) for j in scheduler.get_jobs()])
    elif command == 'pause_job':
        scheduler.pause_job(job_id)
    elif command == 'resume_job':
        scheduler.resume_job(job_id)
    elif command == 'remove_job':
        scheduler.remove_job(job_id)

if __name__ == '__main__':
    app.run()

