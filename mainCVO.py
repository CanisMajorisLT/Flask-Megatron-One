__author__ = 'vyt'
import requests
import re
import datetime
import sqlite3
from bs4 import BeautifulSoup


from requests.auth import HTTPDigestAuth

industries_cvo = [[' Praktika', 'p41'], [' Sezoninis darbas', 'p43'], ['Administravimas / Sekretoriavimas', 'p1'], ['Apsauga / Gelbėjimo paslaugos', 'p27'], ['Bankai / Draudimas', 'p25'], ['Elektronika / Telekomunikacijos', 'p6'], ['Energetika', 'p7'], ['Finansai / Apskaita', 'p8'], ['Gamyba / Pramonė', 'p10'], ['Informacinės technologijos', 'p11'], ['Inžinerija', 'p15'], ['Kultūra / Menas', 'p5'], ['Organizavimas / Valdymas', 'p2'], ['Pardavimai', 'p16'], ['Paslaugos', 'p18'], ['Prekyba / pirkimai / tiekimas', 'p21'], ['Rinkodara / Reklama', 'p14'], ['Savanoriškas darbas', 'p35'], ['Statyba / Nekilnojamas turtas', 'p4'], ['Sveikatos apsauga / Socialinė rūpyba', 'p9'], ['Švietimas / Mokslas', 'p22'], ['Teisė', 'p13'], ['Transportas / Logistika', 'p23'], ['Turizmas / viešbučiai / viešasis maitinimas', 'p20'], ['Valstybinis ir viešasis administravimas', 'p19'], ['Žemės ūkis / Aplinkos inžinerija', 'p17'], ['Žiniasklaida / Viešieji ryšiai', 'p12'], ['Žmogiškieji ištekliai', 'p26']]
industries_cvo_numbers = ['p41', 'p43', 'p1', 'p27', 'p25', 'p6', 'p7', 'p8', 'p10', 'p11', 'p15', 'p5', 'p2', 'p16', 'p18', 'p21', 'p14', 'p35', 'p4', 'p9', 'p22', 'p13', 'p23', 'p20', 'p19', 'p17', 'p12', 'p26']

cities_cvo = [['-', 'c0'], ['Alytaus', 'c113'], ['Kauno', 'c114'], ['Klaipėdos', 'c115'], ['Marijampolės', 'c116'], ['Panevėžio', 'c117'], ['Šiaulių', 'c118'], ['Tauragės', 'c119'], ['Telšių', 'c120'], ['Utenos', 'c121'], ['Vilniaus', 'c112']]
cities_cvo_numbers = ['c0', 'c113', 'c114', 'c115', 'c116', 'c117', 'c118', 'c119', 'c120', 'c121', 'c112']
experience_cvo = [['Praktika', 'pat:41'], ['Sezoninis darbas', 'pat:43'], ['Administravimas / Sekretoriavimas', 'pat:1'], ['Apsauga / Gelbėjimo paslaugos', 'pat:27'], ['Bankai / Draudimas', 'pat:25'], ['Elektronika / Telekomunikacijos', 'pat:6'], ['Energetika', 'pat:7'], ['Finansai / Apskaita', 'pat:8'], ['Gamyba / Pramonė', 'pat:10'], ['Informacinės technologijos', 'pat:11'], ['Inžinerija', 'pat:15'], ['Kultūra / Menas', 'pat:5'], ['Organizavimas / Valdymas', 'pat:2'], ['Pardavimai', 'pat:16'], ['Paslaugos', 'pat:18'], ['Prekyba / pirkimai / tiekimas', 'pat:21'], ['Rinkodara / Reklama', 'pat:14'], ['Savanoriškas darbas', 'pat:35'], ['Statyba / Nekilnojamas turtas', 'pat:4'], ['Sveikatos apsauga / Socialinė rūpyba', 'pat:9'], ['Švietimas / Mokslas', 'pat:22'], ['Teisė', 'pat:13'], ['Transportas / Logistika', 'pat:23'], ['Turizmas / viešbučiai / viešasis maitinimas', 'pat:20'], ['Valstybinis ir viešasis administravimas', 'pat:19'], ['Žemės ūkis / Aplinkos inžinerija', 'pat:17'], ['Žiniasklaida / Viešieji ryšiai', 'pat:12'], ['Žmogiškieji ištekliai', 'pat:26']]


#######################################################################################################################

# make a formated date of today
date_today_0 = [int (x) for x in datetime.datetime.now().strftime("%Y-%m-%d").split('-')]
date_today_1 = datetime.date(date_today_0[0], date_today_0[1], date_today_0[2])








search_data_2 = {'vaja_tagasi':1, 'otsing[toggle_show]':1, 'otsing[search_id]':1, 'valitud_change':0, 'desired_change':0, 'view_change':0, 'passiivne_change':0,'aktiivne_change':0}
search_data_3 = {'CvList_id':0,'cvarv_cvlistis':200,'vaja_tagasi':1, 'otsing[search_id]':1, 'valitud_change':0, 'desired_change':0, 'view_change':0, 'passiivne_change':0,'aktiivne_change':0}


def func01_cvo(query_string, user,  days_limit = 5, industry=None, city=None):

    ### links ##
    link_login = 'http://www.cvonline.lt/login'
    link_search = 'http://www.cvonline.lt/iesko/adv_search.php?page=new'
    link_search_2 = 'http://www.cvonline.lt/iesko/adv_search.php'
    ############


    ## data ##
    search_data = {'otsing[par1]':'.net', 'otsing[par2]':'AND', 'otsing[search_id]':1, 'otsing[function_ok]':1, 'otsing[function_id]':'query'}
    search_data['otsing[par1]'] = query_string
    login_data = {'username': user.cvo_usr, 'password': user.cvo_pss, 'module': 'login'}




    list_of_cv_links = []
    query_data = []


    with requests.Session() as s:
        s.post(link_login, data=login_data)


        breakdashit = False




        #add city.. ///
        if city:
            city_data = {'andmed[country_id]':92, 'andmed[county_id]':city[1:], 'andmed[town_id]':0, 'otsing[search_id]':1,
                         'otsing[function_ok]':1, 'otsing[function_id]':40}
            s.post(link_search_2, data=city_data)


        # add industry, so it is appended into cookies  ///
        if industry:
            sritis_data = "otsing[search_id]=1&otsing[function_ok]=1&otsing[function_id]=12"
            sritis_data_n = {'parmas1[]':str(industry[0][1:]),'otsing[search_id]':1,'otsing[function_ok]':1,'otsing[function_id]':12}
            for srt in industry:
                sritis_data = 'parmas1[]='+str(srt[1:])+'&'+sritis_data
            s.post(link_search_2+'?'+sritis_data)


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
            for page in range (2, 50):

                nav_page = s.get('http://www.cvonline.lt/iesko/adv_search.php?kartoteek=&id=&all_id=&CvList_id={}&otsitud_sona=&konto=&otsing[search_id]=1&ptutvustus=&lk={}'.format(CvList_id, page))
                cv_info_1, breakdashit = ad_parser(nav_page, days_limit)

                for cv_1 in cv_info_1:
                    list_of_cv_links.append(cv_1)

                #check if cv age limit has been reached
                if breakdashit:
                    break

    search_string = query_string
    search_city = find_dareal_name(city) if city else 'Visa Lietuva'
    search_industry = find_dareal_name(industry) if industry else 'Visos sritys'
    query_data.append(['CVO', search_string, search_city, search_industry, days_limit])
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


        # all info in html
        html_info = ad.find('td', {'valign':"top", 'align':"left"})


        cv_info_list.append([cv_link, html_info, cv_passive, False, date_3])

        if breakdashit:
            break

    #print(cv_info_list)
    return cv_info_list, breakdashit



def validate_cvo_login(acc, pss):
    login_data = {'username': acc, 'password': pss, 'module': 'login'}
    print("Validanting CVB login {}".format(login_data))
    log = requests.post('http://www.cvonline.lt/login', data=login_data)
    if log.url == 'http://www.cvonline.lt/login':

        return "False"
    else:
        return "True"

def find_dareal_name(x):
    indust = ''
    if x[0] == 'c':
        for y in cities_cvo:
            if y[1] == x:
                return y[0]
    else:
        for z in x:
            for y in industries_cvo:
                if z == y[1]:
                    indust = indust+', '+y[0]
        return indust


def check_cvo_follow(user, cvs):
    """takes a list of cvs  and user object and checks if their cv update day has changed"""

  ### links ##
    link_login = 'http://www.cvonline.lt/login'
  ### links ##

    ## data ##
    login_data = {'username': user.cvo_usr, 'password': user.cvo_pss, 'module': 'login'}
    months = {'kovo': 3, 'gegužės': 5, 'rugsėjo': 9, 'lapkričio': 11, 'sausio': 1, 'spalio': 10, 'birželio': 6, 'rugpjūčio': 8, 'liepos': 7, 'balandžio': 4, 'gruodžio': 12, 'vasario': 2, 'April': 4, 'February': 2, 'June': 6, 'July': 7, 'May': 5, 'August': 8, 'January': 1, 'November': 11, 'March': 3, 'December': 12, 'September': 9, 'October': 10}
    updated_cvs = []

    ## data ##

    with requests.Session() as s:
        s.post(link_login, data=login_data)

        for cv in cvs:

            link = s.get(cv.url)
            link_soup = BeautifulSoup(link.text, 'lxml')
            date_1 = link_soup.find('table', class_="top_inf").find('td', align="center").next.text.split(':')[1].split(' ')
            date_2 = datetime.date(int(date_1[3]), months[date_1[2]], int(date_1[1][:2]))
            if date_2 > cv.date_edited:
                updated_cvs.append([cv, date_2])
    print("Updated CV CVO: {}".format(updated_cvs))
    return updated_cvs

def parse_for_cats_cvo(user, url):
    link_login = 'http://www.cvonline.lt/login'
    login_data = {'username': user.cvo_usr, 'password': user.cvo_pss, 'module': 'login'}
    with requests.Session() as s:
        s.post(link_login, data=login_data)
        link = s.get(url)
        soup = BeautifulSoup(link.text, 'lxml')
        personal_data = soup.find('table', class_="CvVormTable")
        personal_data_list = [x.text for x in personal_data.find_all('td')]
        first_name, last_name, phone, email = "Vardas", "Pavarde", "123456789", "mail@mail.com"
        for y, x in enumerate(personal_data_list):
            if x == "Vardas:" or x == "Name:":
                try:
                    first_name, last_name = personal_data_list[y+1].split(' ')[0], personal_data_list[y+1].split(' ')[1]
                except Exception as e:
                    print(e)
            if x == "El. paštas:" or x == "E-mail:":
                email = personal_data_list[y+1]
            if x == "Kontaktinis telefonas:" or x == 'Contact telephone:':
                phone = personal_data_list[y+1]
        with open('cvtest.html', 'wb') as j:
            j.write(link.content)
        return first_name, last_name, phone, email
