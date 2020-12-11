# %% Admin
import pandas as pd
import requests
import io
import re
from datetime import datetime

# %% Function
def NasdaqTickers_RawExtract(Exchange_OfInterest= "All"):
    # Exchange_OfInterest= "All"

    # Admin
    Temp_getheaders = {'authority': 'old.nasdaq.com', 'upgrade-insecure-requests': '1',
                       'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                       'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                       'sec-fetch-site': 'cross-site','sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1', 'sec-fetch-dest': 'document', 'accept-language': 'en-US,en;q=0.9',
                       'cookie': 'AKA_A2=A; NSC_W.TJUFEFGFOEFS.OBTEBR.443=ffffffffc3a0f70e45525d5f4f58455e445a4a42378b'}

    # Extraction
    UrlLinks= {"Nasdaq": "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
            "Amex":   "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download",
            "NYSE":   "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"}

    if   Exchange_OfInterest != "All" and Exchange_OfInterest not in list(UrlLinks.keys()):
        print("Invalid Exchange listed, please insert: {}".format(", ".join(list(UrlLinks.keys()))))
        pass

    elif Exchange_OfInterest != "All" and Exchange_OfInterest in list(UrlLinks.keys()) :
        print("Valid Exchange listed")
        print("- extracting {} tickers".format(Exchange_OfInterest))
        URLRaw = requests.get(UrlLinks[Exchange_OfInterest], headers=Temp_getheaders)
        URLRaw2 = io.StringIO(URLRaw.text)
        URLRaw_Final = pd.read_csv(URLRaw2, sep=",")

    else:
        URLRaw_Final = pd.DataFrame()
        print("Extracting from {}".format(", ".join(list(UrlLinks.keys()))))

        for Exchange in list(UrlLinks.keys()):
            print("- extracting {} tickers".format(Exchange))
            URLRaw = requests.get(UrlLinks[Exchange], headers=Temp_getheaders)
            URLRaw2 = io.StringIO(URLRaw.text)
            URLRaw_Temp = pd.read_csv(URLRaw2, sep=",")

            URLRaw_Final= URLRaw_Final.append(URLRaw_Temp)

    # Returning
    Tickers = URLRaw_Final[~URLRaw_Final['Symbol'].str.contains("\.|\^")]. \
        drop("Unnamed: 8", 1). \
        drop_duplicates(keep=False)
    Tickers_Final =Tickers. \
        sort_values("Symbol", ignore_index=True).\
        copy()
    Tickers_Final.columns=["Symbol", "Name", "LastSale", "MarketCap", "IPOyear", "Sector", "Industry", "SymbolURL"]

    return Tickers_Final

def NasdaqTickers_Process(NasdaqTickers_Df):
    pass

# Admin
NasdaqTickers_Df= NasdaqTickers_RawExtract(); Unnecessary_WordLimit= 100
NasdaqTickers_Df.dtypes

# Process1- Handling ETF's
NasdaqTickers1= NasdaqTickers_Df.copy()
NasdaqTickers1.loc[NasdaqTickers1["Sector"].isna(), "Sector"]= "ETF"

# Process2- Removing Punctuations
NasdaqTickers1["Name"]= [re.sub(r"[^\w\s]","", word) for word in NasdaqTickers1["Name"].tolist()]

# TODO: Continue writing Process 3.1 or 3.2
# %% Process3.1- Removing Unnecessary names
NasdaqTickers2= NasdaqTickers1.copy()
NasdaqTickers2["Name2"]= [re.sub(" ","_",SegmentedName) for SegmentedName in NasdaqTickers2["Name"]]

# _Identifying Unnecessary names
Allwords= [word for line in NasdaqTickers2["Name"].tolist() for word in line.split()]
WordDict = {}
for word in Allwords:
    WordDict[word] = WordDict.setdefault(word, 0) + 1

# Allsorted=sorted(WordDict.items(), key=lambda x:x[1], reverse=True); print(Allsorted[:100])
UnnecessaryWords= [k for (k,v) in WordDict.items() if v > Unnecessary_WordLimit]
UnnecessaryWords= [word for word in UnnecessaryWords if word not in ""]
UnnecessaryWords2= []
for Uword in UnnecessaryWords:
    UnnecessaryWords2.append("_{}".format(Uword))
    UnnecessaryWords2.append("{}_".format(Uword))
    UnnecessaryWords2.append("_{}_".format(Uword))
UnnecessaryWords3= "|".join(UnnecessaryWords2)

NasdaqTickers2["Name_StopExcluded"]= NasdaqTickers2["Name2"].str.replace(UnnecessaryWords3, '')
NasdaqTickers2["Name_StopExcluded"]= [Name.strip() for Name in NasdaqTickers2["Name_StopExcluded"]]


# %% Process3.2- Removing Unnecessary names
NasdaqTickers2= NasdaqTickers1.copy()

# _Identifying Unnecessary names
# Allsorted=sorted(WordDict.items(), key=lambda x:x[1], reverse=True); print(Allsorted[:100])
Allwords= [word for line in NasdaqTickers2["Name"].tolist() for word in line.split()]
WordDict = {}
for word in Allwords:
    WordDict[word] = WordDict.setdefault(word, 0) + 1

UnnecessaryWords= [k for (k,v) in WordDict.items() if v > Unnecessary_WordLimit]
UnnecessaryWords= [word for word in UnnecessaryWords if word not in ""]

# _Removing Unnecessary items
NasdaqTickers2["Name2"]= [SegmentedName.split(" ") for SegmentedName in NasdaqTickers2["Name"]]
# TODO: We need a way of removing all the unnecessary words from the list.
# Try writing a function here and then applying

x= [Name for FullName in Names_List for Name in FullName if Name not in UnnecessaryWords]
len(x)
x[:10]
NasdaqTickers2.iloc[:10]["Name2"]
len(NasdaqTickers2["Name2"])

