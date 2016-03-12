import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import requests
from bs4 import BeautifulSoup as bs
import scraperwiki
from datetime import datetime
import re
import time


start_url = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={}'
ua = {'User-agent': 'Mozilla/5.0'}


def connect(start_url, search_term):
    search_page = requests.get(start_url.format(search_term), headers=ua)
    soup = bs(search_page.text, 'lxml')
    title = soup.title.text
    while 'Robot Check' in title:
        search_page = requests.get(start_url.format(search_term), headers=ua)
        soup = bs(search_page.text, 'lxml')
        title = soup.title.text
    if soup:
        pass
    else:
        connect(start_url, search_term)
    return soup


def parse(search_term, search_tag, p):
    soup = connect(start_url, search_term)
    print p
    search_tag = '='+'"'+search_tag+'"'
    search_rows = soup.find_all('li', 's-result-item celwidget')
    for search_row in search_rows:
        search_term = search_term
        search_tag = search_tag
        try:
            title = search_row.find('h2', 'a-size-medium a-color-null s-inline s-access-title a-text-normal').text.strip()
            asin = search_row.find('a', 'a-link-normal s-access-detail-page  a-text-normal')['href'].split('dp/')[-1].split('/')[0]
            #asin = '='+'"'+search_row.find('a', 'a-link-normal s-access-detail-page  a-text-normal')['href'].split('dp/')[-1].split('/')[0]+'"'
        except: continue
        #print(title)
        pubdate = ''
        try:
            pubdate = search_row.find('div', 'a-row a-spacing-small').find('span', 'a-size-small a-color-secondary').text.strip().replace('by', '')
        except:
            pass
        author = ''
        try:
            author = search_row.find('div', 'a-row a-spacing-small').find('div', 'a-row a-spacing-none').text.strip().split('by')[-1].strip()
        except:
            pass
        item_format = ''
        try:
            item_format = search_row.find('h3', 'a-size-small a-color-null s-inline  a-text-normal').text.strip()
        except:
            pass
        rentprice = ''
        try:
            rentprice = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find(text=re.compile('to rent')).find_previous('span', 'a-size-base a-color-price s-price a-text-bold').text
        except:
            pass
        amazon_new_s = ''
        try:
            amazon_new_s = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find(text=re.compile('to buy')).find_previous('span', 'a-size-base a-color-price s-price a-text-bold').text
        except:
            try:
                amazon_new_s = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('span', 'a-size-small a-color-secondary a-text-strike').find_previous('span', 'a-size-base a-color-price s-price a-text-bold').text
            except:
                pass
        lowall_0_s = ''
        try:
            lowall_0_s = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find(text=re.compile('used & new')).find_previous('span', 'a-size-base a-color-price a-text-bold').text
        except:
            pass
        totaloffercount = ''
        try:
            totaloffercount = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find(text=re.compile('offers')).replace('(', '').replace(')','')
        except:
            pass
        other1format = ''
        try:
            other1format = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find('hr', 'a-divider-normal s-result-divider').find_next('a').text
        except:
            pass
        if other1format:
            other1asin = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find('hr', 'a-divider-normal s-result-divider').find_next('a')['href'].split('dp/')[-1].split('/')[0]
            #other1asin = '='+'"'+search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find('hr', 'a-divider-normal s-result-divider').find_next('a')['href'].split('dp/')[-1].split('/')[0]+'"'
        else:
            other1asin = ''
        other2format = ''
        try:
            other2format = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a').text
        except:
            pass
        if other2format:
            other2asin = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a')['href'].split('dp/')[-1].split('/')[0]
            #other2asin = '='+'"'+search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a')['href'].split('dp/')[-1].split('/')[0]+'"'
        else:
            other2asin = ''
        if other1format == other2format:
            other1format = ''
            other1asin = ''
        comma = ''
        try:
            comma = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a').find_next('span', 'a-size-small a-color-secondary').text
        except:
            pass
        other3format = ''
        if ',' in comma:
            other3format = ''
            try:
                other3format = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a').find_next('a').text
            except:
                pass
        if other3format:
            other3asin = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a').find_next('a')['href'].split('dp/')[-1].split('/')[0]
            #other3asin = '='+'"'+search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find(text=re.compile('Other Format')).find_next('a').find_next('a')['href'].split('dp/')[-1].split('/')[0]+'"'
        else:
            other3asin = ''
        newer = ''
        try:
            newer = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find('div', 'a-column a-span7').find('a', text=re.compile('See newer edition of this book'))
        except:
            pass
        if newer:
            newer = '='+'"'+newer['href'].split('dp/')[-1].split('/')[0]+'"'
        tradeinprice = ''
        try:
            tradeinprice = search_row.find('div', 'a-fixed-left-grid-col a-col-right').find(text=re.compile('Trade in yours for')).find_next('span', 'a-color-price').text
        except:
            pass
        new_stock_count_s = new_stock_status_s = new_restock_date_s = ''
        try:
            new_stock_count = search_row.find('span', text=re.compile('left in stock - order soon')).text.strip()
        except:
            try:
                new_stock_count = search_row.find(text=re.compile('Get it by')).parent.text
            except:
                try:
                    new_stock_count = search_row.find('span', text=re.compile('Temporarily out of stock')).text.strip()
                except:
                    try:
                        new_stock_count = search_row.find('span', text=re.compile('Currently unavailable')).text.strip()
                    except:
                        try:
                            new_stock_count = search_row.find('span', text=re.compile('may require an extra')).text.strip()
                        except:
                            try:
                                new_stock_count = search_row.find('span', text=re.compile('Available for Pre-order')).text.strip()
                            except:
                                try:
                                    new_stock_count = search_row.find('span', text=re.compile('In stock on')).text.strip()
                                except:
                                    pass
        if 'left in stock - order soon' in new_stock_count:
            new_stock_count_s = new_stock_count.split('left')[0].split('Only')[-1].strip()
            new_stock_status_s = 'limited'
            new_restock_date_s = 'na'
        elif 'Get it by' in new_stock_count:
            new_stock_count_s = 999
            new_stock_status_s = 'in stock'
            new_restock_date_s = None
        elif 'Temporarily out of stock' in new_stock_count:
            new_stock_count_s = 0
            new_stock_status_s = 'Temporarily out'
            new_restock_date_s = 'temp'
        elif 'Currently unavailable' in new_stock_count:
            new_stock_count_s = 0
            new_stock_status_s = 'unavailable'
            new_restock_date_s = 'unknown'
        elif 'may require an extra' in new_stock_count:
            new_restock_date_s = new_stock_count.split('an')[-1].strip().split('to')[0].strip()
            new_stock_count_s = 0
            new_stock_status_s = 'extra processing'
        elif 'Available for Pre-order' in new_stock_count:
            new_restock_date_s = new_stock_count.split('on')[-1].strip()
            new_stock_count_s = 0
            new_stock_status_s = 'pre-order'
        elif 'In stock on' in new_stock_count:
            new_restock_date_s = new_stock_count.split('on')[-1].strip()
            new_stock_count_s = 0
            new_stock_status_s = 'replenishing'
        elif not new_stock_count:
            new_stock_status_s = 'in stock'



        # print new_stock_count, new_stock_status, new_restock_date
        # print title, asin, pubdate, author, item_format, price_rent, price, low_price, offer_count, other1format, other1asin, other2format, other2asin, other3format, other3asin, newer, tradein
        today_date = str(datetime.now())
        scraperwiki.sqlite.save(unique_keys=['Date'], data={'SearchString': unicode(search_term), 'Search Tag': search_tag, 'Title': unicode(title), 'ASIN': asin, 'PubDate': pubdate, 'Author': unicode(author), 'Format': unicode(item_format), 'PriceRent': rentprice, 'Price': amazon_new_s, 'PriceLow': lowall_0_s, 'OfferCount': totaloffercount, 'Other1Format': unicode(other1format), 'Other1ASIN': other1asin, 'Other2Format': unicode(other2format), 'Other2ASIN': other2asin, 'Other3Format': unicode(other3format), 'Other3ASIN': other3asin, 'Newer_Edition': newer, 'TradeIn': unicode(tradeinprice), 'NewStockCount': new_stock_count_s, 'NewStockStatus': new_stock_status_s, 'NewRestockDate': new_restock_date_s, 'Date': today_date})


if __name__ == '__main__':
        file1 = open('amazon.txt', 'r')
        p = 1
        for line in file1:
            search_term = line.split('%')[-1].replace('&', '%26')
            search_tag = line.split('%')[0]
            search_term = '+'.join(search_term.split(' '))
            parse(search_term, search_tag, p)
            p +=1
