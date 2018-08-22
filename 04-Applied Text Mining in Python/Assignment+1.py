
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[2]:

import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head(10)


# In[500]:

import re
import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)
df = pd.Series(doc)


def date_sorter():
    # Your code here

    dateStr = "1; 111; 12; 12343; 10/28; 04/20/2009; 04/20/09; 4/20/09; 4/3/09; 6/2008; 12/2009; 2009; 2010"
    DATES_NUM = "(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}[/-]\d{4}|\d{4})"
    found = re.findall(r'' + DATES_NUM + '', dateStr)
    #print("Loaded: " + str(len(dateStr.split(";"))))
    #print("Found " + str(len(found)) + ": " + str(found))

    dateStr = "1; 111; 12; 12345; 10/28; Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009; 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009; Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009; Feb 2009; Sep 2009; Oct 2010"
    DATES_STR =  "(?:Jan[a-z]*|Feb[a-z]*|Mar[a-z]*|Apr[a-z]*|May[a-z]*|Jun[a-z]*|Jul[a-z]*|Aug[a-z]*|Sep[a-z]*|Oct[a-z]*|Nov[a-z]*|Dec[a-z]*|\d{1,2})?(?:st|nd|th)?(?:\/|\-|\,\s|\.\s|\s)?"    
    DATES_ALL = '' + DATES_STR + DATES_STR + '\d{4}'
    found = re.findall(r'' + DATES_ALL + '', dateStr)
    #print("Loaded: " + str(len(dateStr.split(";"))))
    #print("Found " + str(len(found)) + ": " + str(found))

    DATES_ALL = DATES_ALL + '|' + DATES_NUM

    # all
    dateStr = "1; 111; 12; 12345; 10/28; 04/20/2009; 04/20/09; 4/20/09; 4/3/09; 6/2008; 12/2009; 2009; 2010; Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009; 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009; Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009; Feb 2009; Sep 2009; Oct 2010"
    found = re.findall(r'' + DATES_ALL + '', dateStr)
    #print("Loaded: " + str(len(dateStr.split(";"))))
    #print("Found " + str(len(found)) + ": " + str(found))    
    
    # extracted dates
    #print("REAL")
    #print(df.str.findall(r''+ DATES_ALL +''))
    
    results = []
    i = 0
    for line in df.str.findall(r''+ DATES_ALL +''): 
        append = False
        for item in line:
            if not re.match("^\d{3,}[\-\/\,\.]", item):
                item_old = item
                item = item.strip().rstrip()
                item = re.sub("^[\-\.\, ]{,2}","",item)
                item = re.sub("^(st|nd|th) ","",item)
                item = re.sub("^\d+[\.\,]","",item)
                item = re.sub("^\d{3,} ","",item)            
                item = re.sub("-","/",item)      

                if "/" in item:
                    item = re.sub("^\d{3,} ","",item)

                if re.match("^\d+ \d", item):
                    item = re.sub("^\d+ ","",item)

                item = item.strip().rstrip()
                #print(str(i) + " => " + str(item))
                
                results.append(item)
                
                append = True
                
                break
        if not append:
            results.append("NaN")
        i=i+1
    
    dfr = pd.DataFrame(results, columns=["date"])
        
    dfr["date"] = dfr["date"].str.replace(r'[\s\,\.]', lambda x: "/")
    dfr["date"] = dfr["date"].str.replace(r'//', lambda x: "/")
    dfr["date"] = dfr["date"].str.replace(r'(/\d{2})$', lambda x: "/19" + str(x.groups()[0][1:]))    
    
    m_index=1
    for m in ["Jan[a-z]*","Feb[a-z]*","Mar[a-z]*","Apr[a-z]*","May[a-z]*","Jun[a-z]*","Jul[a-z]*","Aug[a-z]*","Sep[a-z]*","Oct[a-z]*","Nov[a-z]*","Dec[a-z]*"]:
        dfr["date"] = dfr["date"].str.replace(r'^(\d{1,2}/'+ m +'/\d{4})$', lambda x: str(m_index) +"/"+ str(str(x.groups()[0]).split("/")[0]) +"/"+str(str(x.groups()[0]).split("/")[2]))                
        dfr["date"] = dfr["date"].str.replace(r'('+ m +'/\d{4})$', lambda x: str(m_index) +"/01/"+str(str(x.groups()[0]).split("/")[1]))        
        m_index = m_index + 1

    dfr["date"] = dfr["date"].str.replace(r'^(\d{1,2}/\d{4})$', lambda x: str(str(x.groups()[0]).split("/")[0])+"/01/"+str(str(x.groups()[0]).split("/")[1]))
    dfr["date"] = dfr["date"].str.replace(r'^(\d{4})$', lambda x: "01/01/" + str(x.groups()[0]))    
        
    dfr['date'] = pd.to_datetime(dfr.date)            
    
    dfr = dfr.sort_values(by="date")
    dfr.reset_index(inplace=True) 
    dfr["rank"] = dfr.index
    dfr = dfr.set_index("rank").sort_index()
    
    return dfr["index"]
    
date_sorter()
#date_sorter()[10:150]
#df[9]


# In[ ]:



