__author__ = 'vyt'
import requests
import re
import datetime
import sqlite3
from bs4 import BeautifulSoup


from requests.auth import HTTPDigestAuth
#logdata = {'username':'hrm-talent-lab-laura', 'password':'dramblys1', 'module': 'login'}
#r = requests.post('http://www.cvonline.lt/login',data=logdata)
#print(r.status_code)
#print(BeautifulSoup(r.text, 'lxml'))

#######################################################################################################################

# make a formated date of today
date_today_0 = [int (x) for x in datetime.datetime.now().strftime("%Y-%m-%d").split('-')]
date_today_1 = datetime.date(date_today_0[0], date_today_0[1], date_today_0[2])






login_data = {'username':'hrm-talent-lab-laura', 'password':'dramblys1', 'module': 'login'}


search_data_2 = {'vaja_tagasi':1, 'otsing[toggle_show]':1, 'otsing[search_id]':1, 'valitud_change':0, 'desired_change':0, 'view_change':0, 'passiivne_change':0,'aktiivne_change':0}
search_data_3 = {'CvList_id':0,'cvarv_cvlistis':25,'vaja_tagasi':1, 'otsing[search_id]':1, 'valitud_change':0, 'desired_change':0, 'view_change':0, 'passiivne_change':0,'aktiivne_change':0}


def func01_cvo(query_string, login_data=login_data,  days_limit = 5, sritis=None, city=None):

    ### links ##
    link_login = 'http://www.cvonline.lt/login'
    link_search = 'http://www.cvonline.lt/iesko/adv_search.php?page=new'
    link_search_2 = 'http://www.cvonline.lt/iesko/adv_search.php'
    ############


    ## data ##
    search_data = {'otsing[par1]':'.net', 'otsing[par2]':'AND', 'otsing[search_id]':1, 'otsing[function_ok]':1, 'otsing[function_id]':'query'}
    search_data['otsing[par1]'] = query_string




    list_of_cv_links = []
    query_data = []

    def get_stuff_from_db(query_data):
        pass

    with requests.Session() as s:
        s.post(link_login, data=login_data)

        breakdashit = False

        # add industry, so it is appended into cookies  /// sritis - neveikia jei daugiau nei 1
        if sritis:
            sritis_data = {'otsing[search_id]':1, 'otsing[function_ok]':1,'otsing[function_id]':12}

            sritis_data['parmas1[]'] = sritis

            s.post(link_search, data=search_data)

        #add city.. /// daug pisalynes cia, jau veliau kai viskas veiks reiks ideti
        if city:
            pass


        # 1st step
        s.post(link_search, data=search_data)


        # 2nd step
        nav2 = s.post(link_search_2, data=search_data_2)
        soup2 = BeautifulSoup(nav2.text, 'lxml')

        # get CV-list_id, which acts as a summary of all queries on server side and is used for further navigation
        CvList_id= soup2.find('input', {'name': "CvList_id"}).get('value')
        search_data_3['CvList_id'] = CvList_id


        # 3rd step
        nav3 = s.post(link_search_2, data=search_data_3)

        # parse CV and return data
        cv_info, breakdashit = ad_parser(nav3, days_limit)

        for cv in cv_info:
            list_of_cv_links.append(cv)


        if not breakdashit:
            for page in range (2, 5):

                nav_page = s.get('http://www.cvonline.lt/iesko/adv_search.php?kartoteek=&id=&all_id=&CvList_id={}&otsitud_sona=&konto=&otsing[search_id]=1&ptutvustus=&lk={}'.format(CvList_id, page))
                cv_info_1, breakdashit = ad_parser(nav_page, days_limit)

                for cv_1 in cv_info_1:
                    list_of_cv_links.append(cv_1)

                #check if cv age limit has been reached
                if breakdashit:
                    break

    search_string = query_string
    query_data.append(['CVO', search_string])
    query_data.append(list_of_cv_links)
    return query_data

def ad_parser(obj, days_limit=20):

    breakdashit = False
    cv_info_list = []

    job_ads = BeautifulSoup(obj.text, 'lxml').find_all("tr", id=re.compile("cvrow_\d*"))
    for ad in job_ads:

        cv_passive = False
        #cv_has_previous_exp = False

        #check if CV is passive
        for element in ad.find_all('span', class_="textRed"):
            if element.text == "Pasyvusis":
                cv_passive = True

        #check if CV has info about previous experience
        #if 'Anksčiau užimtos pareigos' in str(ad.contents[3]):
        #    cv_has_previous_exp = True

        #find link to cv
        cv_link = 'http://www.cvonline.lt/' + ad.find_all('a')[-1].get('href')

        #find how old is cv
        date_1 = ad.find('div', class_="clear").next_element.next_element.text
        date_2 = [int(x) for x in date_1.split('.')]
        date_3 = datetime.date(date_2[0], date_2[1], date_2[2])
        days_after_edit = date_today_1 - date_3

        # variable giving int of how old is cv (days)
        how_old_is_cv = days_after_edit.days
        print(how_old_is_cv)

        # check if CV is not too old
        if how_old_is_cv > days_limit:
            breakdashit = True

        #previous work experience
        #if cv_has_previous_exp:
        #    if not cv_passive:
        #        experience = ad.find_all('b')[3].text
        #    else:
        #        experience =ad.find_all('b')[2].text
        #else:
        #    experience = "Not given"

        # all info in html
        html_info = ad.find('td', {'valign':"top", 'align':"left"})


        cv_info_list.append([cv_link, html_info, cv_passive, False])

        if breakdashit:
            break

    #print(cv_info_list)
    return cv_info_list, breakdashit




#print(func01_cvo('php'))




