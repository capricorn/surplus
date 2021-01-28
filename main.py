from time import sleep

import requests
from bs4 import BeautifulSoup

def download_inventory():
    return requests.get('https://www.surplus.iastate.edu/sales/inventory').text

def inventory_updated(curr_hash, prev_hash):
    return set(curr_hash) != set(prev_hash)

def parse_inventory(raw_html):
    '''
    Return the sale inventory as a list of items 
    '''
    parser = BeautifulSoup(raw_html, 'html.parser')
    inventory = parser.find('div', attrs={'class':'wd-Grid-cell col-md-9'}).text.split('\n')[4:]
    inventory = [ item.strip().lower() for item in inventory ]
    return inventory


# Maybe just pass it a list of regex to match against
def alert(inventory):
    '''
    Callback whenever the sale inventory changes.
    inventory: list of strings representing the name of the item
    '''
    results = [ item for item in inventory if \
            any([ search_str in item for search_str in ('chalkboard', 'whiteboard')]) ]

    print(results)
    # Send some sort of text or email here..

def check_inventory(prev_inventory, callback):
    '''
    If the new inventory does not match the previous inventory,
    execute callback(new_inventory)
    '''
    inv_html = download_inventory()
    inventory = parse_inventory(inv_html)

    if inventory_updated(inventory, prev_inventory):
        callback(inventory)
    else:
        print('no change')

    return set(inventory)

'''
Any simple notification services..?
'''
# Some error handling necessary too
if __name__ == '__main__':
    prev_inventory = set()
    # Seconds to wait between checks
    timeout = 10

    try:
        while True:
            prev_inventory = check_inventory(prev_inventory, alert)
            # Worth saving prev inventory to disk so program can be started again
            sleep(timeout)
    except KeyboardInterrupt:
        ...
