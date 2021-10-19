from pyjstat import pyjstat
from datetime import datetime
from DB import Database
import pandas as pd

'''
Reads Data from Central Statistics Office Database on Rainfall as Json
and writes to pandas dataframe
'''

URLS = {'Rainfall':'https://statbank.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/MTM01',
        'Temperature':'https://statbank.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/MTM02',
        'Sunshine':'https://statbank.cso.ie/StatbankServices/StatbankServices.svc/jsonservice/responseinstance/MTM03'}

def get_input(url):
    EXAMPLE_URL = url

    # read from json-stat
    dataset = pyjstat.Dataset.read(EXAMPLE_URL)

    # write to dataframe
    df = dataset.write('dataframe')
    return df

def df_clean_up(url):
        df = get_input(url[1])
        df['Month'] = df['Month'].apply(lambda x: datetime.strptime(x, '%YM%m'))
        #df.reset_index(inplace = True)
        df['Year'] = df['Month'].dt.year
        #handle na values i
        df = df.sort_values(['Year','Month'], ascending = False)
        df = df.groupby(['Statistic','Year','Meteorological Weather Station']).mean()
        return (url[0],df)

def main():
    db = Database()
    for url in URLS.items():
        name, df = df_clean_up(url)
        df = df.reset_index()
        #write copy of dataframe to db
        db.write_to_db(df,name)

if __name__ == "__main__":
    #db = Database()
    #main()
    #print(db.show_tables())
    pass
    
