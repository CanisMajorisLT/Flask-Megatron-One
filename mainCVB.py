__author__ = 'vyt'

from bs4 import BeautifulSoup
import requests
import re
import datetime
import sqlite3

#conn = sqlite3.connect('Database.db')

#######################################################################################################################

cities = ['Visa Lietuva', 'Vilnius', 'Kaunas', 'Klaipėda', 'Šiauliai', 'Panevėžys', 'Akmenė', 'Alytus', 'Anykščiai', 'Birštonas',
           'Biržai', 'Druskininkai', 'Elektrėnai', 'Gargždai', 'Ignalina', 'Jonava', 'Joniškis', 'Jurbarkas',
           'Kaišiadorys', 'Kalvarija', 'Kazlų Rūda', 'Kėdainiai', 'Kelmė', 'Kretinga', 'Kupiškis', 'Kuršėnai',
           'Lazdijai', 'Marijampolė', 'Mažeikiai', 'Molėtai', 'Naujoji Akmenė', 'Neringa', 'Pagėgiai', 'Pakruojis',
           'Palanga', 'Pasvalys', 'Plungė', 'Prienai', 'Radviliškis', 'Raseiniai', 'Rietavas', 'Rokiškis', 'Šakiai',
           'Šalčininkai', 'Šilalė', 'Šilutė', 'Širvintos', 'Skuodas', 'Švenčionys', 'Tauragė', 'Telšiai', 'Trakai',
           'Ukmergė', 'Utena', 'Varėna', 'Vilkaviškis', 'Visaginas', 'Zarasai', 'Užsienis']

industries = ['Visos sritys', 'Administravimas/sekretoriavimas', 'Apsauga', 'Apskaita/finansai/auditas', 'Dizainas/architektūra',
          'Draudimas', 'Eksportas', 'Elektronika/telekomunikacijos', 'Energetika', 'Inžinerija/mechanika',
          'Klientų aptarnavimas/paslaugos', 'Kompiuteriai/IT/internetas', 'Kultūra/kūryba', 'Logistika/transportas',
          'Maisto gamyba', 'Marketingas/reklama', 'Medicina/sveikatos apsauga/farmacija', 'Nekilnojamasis turtas',
          'Pardavimų vadyba', 'Personalo valdymas', 'Pirkimai/tiekimas', 'Pramonė/gamyba', 'Prekyba - konsultavimas',
          'Sandėliavimas', 'Statyba', 'Švietimas/mokymai', 'Teisė', 'Turizmas/viešbučiai', 'Vadovavimas/valdymas',
          'Valstybės tarnyba', 'Žemės ūkis/žuvininkystė', 'Žiniasklaida/viešieji ryšiai']

#######################################################################################################################

#### make a formatted date of today ###
date_today_0 = [int (x) for x in datetime.datetime.now().strftime("%Y-%m-%d").split('-')]
date_today_1 = datetime.date(date_today_0[0], date_today_0[1], date_today_0[2])
#### make a formatted date of today ###


def func01_cvb(query_info, user, days_limit = 19):

    login_link = 'http://www.cvbankas.lt/login.php'
    query_link = 'http://www.cvbankas.lt/darbuotoju-paieska?page={}#rezults_a'

    login_data = {'uname':user.cvb_usr, 'pass': user.cvb_pss}

    list_of_cv_links = []
    query_data = []

    with requests.Session() as s:
        s.post(login_link, data=login_data)
        for page_number in range(1, 100):
            breakdashit = False

            nav = s.post(query_link.format(page_number),data=query_info)
            soup = BeautifulSoup(nav.text, 'lxml')
            job_ads = soup.find_all('article', "list_article list_article_rememberable")

            for ad in job_ads:

                # checks if CV is premium
                premium = ad.find('div', "cv_level_icon")

                # find how many days have passed since CV was updated
                date_1 = ad.find_all('div', 'txt_list_2')
                for y in date_1:
                    reg = re.search("\d{4}\.\d{2}\.\d{2}", str(y))
                    if reg:
                        date_2 = [int(x) for x in reg.group().split('.')]
                        date_3 = datetime.date(date_2[0], date_2[1], date_2[2])
                        days_after_edit = date_today_1 - date_3

                        # variable giving int of how old is cv (days)
                        how_old_is_cv = days_after_edit.days
                        #print(days_after_edit.days)

                        # check if CV is not too old
                        if how_old_is_cv > days_limit and not premium:
                            breakdashit = True

                # find a link to CV
                cv_link = ad.find('a').get('href')

                # find some html data
                html_data = str(ad.find('div', class_="cv_list_description txt_list_2"))+'<br/>'+str(ad.find('div', class_="txt_list_1"))

                # is cv passive

                cv_passive = False


                list_of_cv_links.append([cv_link, html_data, cv_passive, False])

                # break loop when CVs get too old
                if breakdashit:
                    break
            if breakdashit:
                break

    info_city = query_info['miestas'] if query_info['miestas'] != '' else 'Visa Lietuva'
    info_industry = query_info['patirt_sritis[]'] if query_info['patirt_sritis[]'] != '' else 'Visos sritys'
    info_kwrd = query_info['search_string']
    info_cvold = 'Up to {} days since upload/edit'.format(days_limit)
    query_data.append(['CVB', info_city, info_industry, info_cvold, info_kwrd])
    query_data.append(list_of_cv_links)
    return query_data



def validate_cvb_login(acc, pss):
    login_data = {'uname': acc, 'pass': pss}
    log = requests.post('http://www.cvbankas.lt/login.php', data=login_data)
    if log.url == 'http://www.cvbankas.lt/mano-skelbimu-sarasas.html':
        return "True"
    else:
        return "False"






