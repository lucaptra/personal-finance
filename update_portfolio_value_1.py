#!/bin/usr/python
'''
Usage: python update_portfolio_value.py [file]

File containing portfolio data must not contain commas (e.g., in dollar amounts)!

More information about yahoofinancials scraping module: https://pypi.org/project/yahoofinancials/

Lucy Tran
June 13, 2019
'''

import datetime
import locale
import sys

from yahoofinancials import YahooFinancials

if __name__=="__main__":
	now = datetime.datetime.now()
	
	locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
	
	fname = sys.argv[1]
	file = open(fname, "r")
	text = file.readlines()
	file.close()
	
	curr_price_dict = {}
	
	text_list = ["%s,%s,%s" % (",".join(text[0].strip().split("\t")), "current_worth", "investment_change")]
	
	for line in text[1:]:
		ticker = line.strip().split("\t")[5]
		
		if ticker not in curr_price_dict.keys():
			print ("Fetching data for %s" % ticker)
			#scraped_data = parse(ticker)
			scraped_data = YahooFinancials(ticker)
			
			curr_price_dict[ticker] = scraped_data.get_current_price()
		
		num_shares = float(line.strip().split("\t")[1])
		current_invest = num_shares*curr_price_dict[ticker]
		
		orig_invest_val = line.strip().split("\t")[4]
		orig_invest = locale.atof(orig_invest_val.strip("$"))
		invest_change = current_invest-orig_invest
		
		out_line = "%s,%s,%s" % (",".join(line.strip().split("\t")), locale.currency(current_invest, grouping = False), locale.currency(invest_change, grouping = False))
		text_list.append(out_line)
	
	out = '\n'.join(text_list)
	#outfile = open("%s_updated_%s.csv" % (fname[:-4], scraped_data['Current Date']),'w')
	outfile = open("%s_updated_%s.csv" % (fname[:-4], now.strftime("%m-%d-%Y")),'w')
	outfile.write(out)