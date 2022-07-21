from lib.tiktok import Tiktok
from lib.cleaner import Cleaner

from tabulate import tabulate

import os

menu = [
    [':: ToolKit Downloader ::'],
    ['*', '[1]', 'To download videos on TikTok without watermark'],
    ['*', '[2]', 'Clear cache videos'],
    ['*', '[10]', 'Exit to program']
]

def cli_program():
    try:
        config_cache = Cleaner('./lib/__pycache__', 'Videos Saved TTK')
        while True:
            Tiktok.clean_terminal()
            print(tabulate(menu, headers='firstrow', tablefmt='fancy_grid'))
            user = input('Select a Tool: ')

            if(user == '1'):
                Tiktok.main()
                Tiktok.clean_terminal()
                config_cache.clean_cache()
                
            elif(user == '2'):
                config_cache.clean_cache_videos()
                config_cache.clean_cache()

            elif(user == '10'):
                Tiktok.spin_cursor(1, '[ Closing Program ]')
                Tiktok.clean_terminal()
                config_cache.clean_cache()
                
    
    except:
        Tiktok.spin_cursor(1, '[ Closing Program ]')
        Tiktok.clean_terminal()
        config_cache.clean_cache()
        exit()

cli_program()
