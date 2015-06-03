__author__ = 'vyt'

from mainCVB import  func01_cvb, cities_cvb, industries_cvb, validate_cvb_login
from mainCVO import func01_cvo, validate_cvo_login, industries_cvo_numbers, cities_cvo_numbers
import json

# takes a dict of submitted query and extracts data, pushes to db query
def recognize_dat_data_and_find_cvs(list, user, query_data=False):

    data_of_search_queries = []
    city_cvo = []
    industry_cvo = []

    #which database to search in?
    database = ''
    if 'CVB' in list and 'CVO' in list:
        database = 'All'
    elif 'CVB' in list and 'CVO' not in list:
        database = 'CVB'
    elif 'CVB' not in list and 'CVO'  in list:
        database = 'CVO'
    else:
        database = 'All'

    search_data_cvb = {'action':1,'miestas':'', 'patirt_sritis[]':'', 'search_string':''}
    city_cvb = []
    industry_cvb = []
    search_data_cvb['search_string'] = list['kwrds']
    days_limit = int(list['CVold']) if len(list['CVold']) >= 1 else 20
    for x in list.keys():
        if x in cities_cvb:
            city_cvb.append(x)
        elif x in industries_cvb:
            industry_cvb.append(x) if x != 'Visos sritys' else industry_cvb.append('')
        elif x in industries_cvo_numbers:
            industry_cvo.append(x)
        elif x in cities_cvo_numbers:
            city_cvo.append(x)

    #if no parameters selected
    if len(city_cvb) == 0:
        city_cvb.append('')
    if len(industry_cvb) == 0:
        industry_cvb.append('')
    if len(city_cvo) == 0:
        city_cvo.append('')
    if len(industry_cvo) == 0:
        industry_cvo.append('')

    print('citycvo{}'.format(city_cvo))

    # iterate though every city * industry_cvb query and collect CV links to list >>CVB<<
    if database == 'CVB' or database == 'All':
        for y in city_cvb:
            search_data_cvb['miestas'] = y
            for z in industry_cvb:                   # sita pakeisti, nes gali ieskot keliose srityse vienu metu
                search_data_cvb['patirt_sritis[]'] = z
                one_search_query = func01_cvb(search_data_cvb, user, days_limit=days_limit)
                data_of_search_queries.append(one_search_query)


    # collect CV links to list >>CVO<<
    if database == 'CVO' or database == 'All':
        if len(city_cvo[0]) == 0:
            data_of_search_queries.append(func01_cvo(list['kwrds'], user, industry=industry_cvo if len(industry_cvo[0]) > 0 else None, days_limit=days_limit, city=None))
        else:
            for city in city_cvo:
                data_of_search_queries.append(func01_cvo(list['kwrds'], user, industry=industry_cvo if len(industry_cvo[0]) > 0 else None, days_limit=days_limit, city=city))


    if query_data:
        return data_of_search_queries, join_by_commas(city_cvb, city_cvo), join_by_commas(industry_cvb, industry_cvo), list['kwrds'], days_limit, database
    else:
        return data_of_search_queries

#recognize_dat_data_and_find_cvs({'CVold': '50', 'kwrds': 'java'})


def validate_logins(site, acc, pss):
    if site == 'cvbankas':
        return [validate_cvb_login(acc, pss), 'cvb']
    elif site == 'cvonline':
        return [validate_cvo_login(acc, pss), 'cvo']



somejs = '''   $(document).ready(function() {
        $('#wrap').fadeIn()
        $("#kwrds").not('.moda').attr('disabled', 'disabled');
   });'''

def join_by_commas(cvb, cvo):
    a = ','.join(cvb)
    b = ','.join(cvo)
    if len(a) > 0:
        if len(b) > 0:
            return a+','+b
        else:
            return a
    if len(b) > 0:
        if len(a) > 0:
            return a+','+b
        else:
            return b
    return ''