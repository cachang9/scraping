import pandas as pd
import requests
from bs4 import BeautifulSoup
import helper as helper
import numpy as np
from lxml import etree

# setting up parameters
data = pd.DataFrame(columns=['number', 'prov_num', 'date', 'sex', 'age', 'city', 'prov', 'source', 'detail'])
url = 'https://virihealth.com/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# number of confirmed cases
for j in range(2, 2036):
    entry = []
    result = soup.findAll('tr', {'id': 'igsv-12-1C59nxtgcnwGyo6lgypsgN18duxmwWigjeVdKY58t0mU-row-' + str(j)})
    temp = str(result).split('">')
    for i in range(2, len(temp)):
        temp_new = temp[i].split('</td')
        entry.append(temp_new[0])
    data.loc[len(data)] = entry[:9]

# form the dataframe into request data formate
age_9 = []
age_19 = []
age_29 = []
age_39 = []
age_49 = []
age_59 = []
age_69 = []
age_79 = []
age_89 = []
age_90 = []
age_not_define = []

for i in range(len(data['age'])):
    age = str(data['age'][i])
    age_split = age.split('s')
    if len(age_split) < 2:
        helper.update_age_undefined(age_9, age_19, age_29, age_39, age_49, age_59, age_69, age_79, age_89, age_90, age_not_define)
    else:
        age_temp = [int(s) for s in age_split[0] if s.isdigit()]
        age_type = age_temp[0]*10
        helper.update_age(age_type, age_9, age_19, age_29, age_39, age_49, age_59, age_69, age_79, age_89, age_90, age_not_define)

data['age_0_9'] = age_9
data['age_10_19'] = age_19
data['age_20_29'] = age_29
data['age_30_39'] = age_39
data['age_40_49'] = age_49
data['age_50_59'] = age_59
data['age_60_69'] = age_69
data['age_70_79'] = age_79
data['age_80_89'] = age_89
data['age_90_plus'] = age_90
data['age_undefined'] = age_not_define
data['dd_lat'] = np.nan
data['dd_lon'] = np.nan

tree = etree.HTML(str(r.text))
date = tree.xpath('/html/body/main/article/div[1]/div/table[1]/thead/tr/th[2]/div')
data['update'] = date[0].text

data.to_csv('output.csv')
