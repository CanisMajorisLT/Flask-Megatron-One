__author__ = 'vyt'

from mainCVB import  func01_cvb, login_data, link_login, link_search, cities, industries
from mainCVO import func01_cvo

# takes a dict of submitted query and extracts data, pushes to db query
def recognize_dat_data_and_find_cvs(list, query_data=False):

    data_of_search_queries = []

    search_data_cvb = {'action':1,'miestas':'', 'patirt_sritis[]':'', 'search_string':''}
    city = []
    industry = []
    search_data_cvb['search_string'] = list['kwrds']
    days_limit = int(list['CVold']) if len(list['CVold']) >= 1 else 20
    for x in list.keys():
        if x in cities:
            city.append(x)
        if x in industries:
            industry.append(x) if x != 'Visos sritys' else industry.append('')

    #if no parameters selected
    if len(city) == 0:
        city.append('')
    if len(industry) == 0:
        industry.append('')


    # iterate though every city * industry query and collect CV links to list >>CVB<<
    for y in city:
        search_data_cvb['miestas'] = y
        for z in industry:                   # sita pakeisti, nes gali ieskot keliose srityse vienu metu
            search_data_cvb['patirt_sritis[]'] = z
            one_search_query = func01_cvb(login_data, search_data_cvb, link_login, link_search, days_limit)
            data_of_search_queries.append(one_search_query)


    # collect CV links to list >>CVO<<
    #data_of_search_queries.append(func01_cvo(list['kwrds'], days_limit=days_limit))

    if query_data:
        return data_of_search_queries, ','.join(city), ','.join(industry), list['kwrds'], days_limit
    else:
        return data_of_search_queries

#recognize_dat_data_and_find_cvs({'CVold': '50', 'kwrds': 'java'})


def update_table(query_id):

    pass


somejs = '''   $(document).ready(function() {
        $('#wrap').fadeIn()
        $('button[data-toggle="dropdown"]').attr('disabled', 'disabled');
        $(".form-control").attr('disabled', 'disabled');
   });'''