# %% Admin
from Tickers_Function import *

# %% Extraction and Insertion
Tickers_Raw= NasdaqTickers_RawExtract()
Tickers_Raw.to_csv("C:\\Users\\Andrew\\Documents\\GitHub\\DatabaseAnalysis_Themis\\Data\\Tickers\\ExtractedTickers_Folder\\"+\
                   "ExtractedTickers "+datetime.now().strftime("%Y%m%d_%H%M")+".csv",
                   index=False)