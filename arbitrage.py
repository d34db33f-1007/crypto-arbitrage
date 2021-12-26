#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

import sys, time, json
import traceback
import requests
import random

from colorama import Fore, init
from python_1inch import OneInchExchange

adr = '0x5bA348Dd4FcFA2D4B151Fa56b008E3BE6bb27505'
oinch = OneInchExchange(adr, chain='binance')
oinch.get_tokens()
init()

# Binance pairs: ~$ curl -X GET \
# https://www.binance.com/api/v1/exchangeInfo | jq
# 1Inch pairs: oinch.get_tokens()

# 1Inch API Python Wrapper: git://tudorelu/python_1inch

burl = 'https://api.binance.com/api/v3/ticker/price?symbol={}'
am = a[1] if len((a := sys.argv)) > 1 else float(300)
src = a[2] if len((a := sys.argv)) > 2 else 'stablecoins.txt'
st = ['USDT', 'BUSD', 'BIDR', 'BVND']

with open(src, 'r') as f:
	pairs = f.read().splitlines()
	random.shuffle(pairs)

def fore_green(msg:str):
	return Fore.GREEN + msg + Fore.RESET

def fore_yel(msg:str):
	return Fore.YELLOW + msg + Fore.RESET

def fore_red(msg:str):
	return Fore.RED + msg + Fore.RESET

def _bin(coin:str, pair: str='USDT'):
	global burl

	_res = requests.get(burl.format(coin), timeout=4)
	if _res.status_code == 200:
		return float(_res.json().get('price'))
	else:
#		print(fore_red(f'[Connection Error]: \
# {_res.text}  --  {coin}'))
#		time.sleep(0.7)
		return False

def inch(t, amount=1):
	_ = oinch.get_quote(t[0], t[1], amount)
	_ = oinch.c_dec(t[1], _.get('toTokenAmount'))
	return float(_)

def run():
	global oinch, pairs
	global am, st

	check = {
           'WBNB': 'BNB',
           'BTCB': 'BTC'
           # todo
           }

	for cur in pairs:
		b = cur.replace('/', '')
		inc = cur.split('/')
		for k, v in check.items():
			if k in b:
				b = b.replace(k, v)
			elif k in inc:
				_ = inc.index(k)
				inc[_] = v
		if oinch.tokens.get(f'{inc[0]}'):
			if oinch.tokens.get(f'{inc[1]}'):
				try:
					p1 = _bin(b)
					_b = _bin(f'{inc[0]}USDT')
					p1, _b != False
					p1 > 0
				except KeyboardInterrupt:
					sys.exit(0)
				except:
					continue
#				time.sleep(0.1)

				try:
					_x = inch(inc)
#					a = (p1 + _x) / 2.0
					fam = float(am) / p1 # / a
					_am = fam * _b
					while True:
						if _am <= float(am):
							fam = _am / _x
							break
						_am = _am / 1.01

					p2 = inch(inc, amount=fam)
					r = p1 / _x
					r = max(p1, _x) % r
					d = p2 - (p1 * fam)
				except:
#					traceback.print_exc()
					continue

				if d < -15 or d > 15:
					_c = fore_yel if d<0 else fore_green
					print(_c(f'Symbol: {cur} \tRatio: \
{str(r)[:5]} \tProfits: {int(d)}'))

if __name__ == '__main__':
	run()


