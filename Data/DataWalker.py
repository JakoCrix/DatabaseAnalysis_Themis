# %% Admin
import os
import re
import pandas as pd
from datetime import datetime

# Tickers
def ExtractingTickers():
    TickerOfInterest= "20201208"

    # Extract the latest tickers from Tickers folder
    ExtractedTickers_List= os.listdir("Data\\Tickers\\ExtractedTickers_Folder")
    ExtractedTickers_List= [re.sub("ExtractedTickers |.csv","",i) for i in ExtractedTickers_List]
    ExtractedTickers_List= [datetime.strptime(date, "%Y%m%d_%H%M") for date in ExtractedTickers_List]
    FileName = "ExtractedTickers " + max(ExtractedTickers_List).strftime("%Y%m%d_%H%M") + ".csv"

    return pd.read_csv("Data\\Tickers\\ExtractedTickers_Folder\\{}".format(FileName))
