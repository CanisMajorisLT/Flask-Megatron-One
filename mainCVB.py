__author__ = 'vyt'

from bs4 import BeautifulSoup
import requests
import re, json
import datetime, pdfkit

#conn = sqlite3.connect('Database.db')

#######################################################################################################################

cities_cvb = ['Visa Lietuva', 'Vilnius', 'Kaunas', 'Klaipėda', 'Šiauliai', 'Panevėžys', 'Akmenė', 'Alytus', 'Anykščiai', 'Birštonas',
           'Biržai', 'Druskininkai', 'Elektrėnai', 'Gargždai', 'Ignalina', 'Jonava', 'Joniškis', 'Jurbarkas',
           'Kaišiadorys', 'Kalvarija', 'Kazlų Rūda', 'Kėdainiai', 'Kelmė', 'Kretinga', 'Kupiškis', 'Kuršėnai',
           'Lazdijai', 'Marijampolė', 'Mažeikiai', 'Molėtai', 'Naujoji Akmenė', 'Neringa', 'Pagėgiai', 'Pakruojis',
           'Palanga', 'Pasvalys', 'Plungė', 'Prienai', 'Radviliškis', 'Raseiniai', 'Rietavas', 'Rokiškis', 'Šakiai',
           'Šalčininkai', 'Šilalė', 'Šilutė', 'Širvintos', 'Skuodas', 'Švenčionys', 'Tauragė', 'Telšiai', 'Trakai',
           'Ukmergė', 'Utena', 'Varėna', 'Vilkaviškis', 'Visaginas', 'Zarasai', 'Užsienis']

industries_cvb = ['Visos sritys', 'Administravimas/sekretoriavimas', 'Apsauga', 'Apskaita/finansai/auditas', 'Dizainas/architektūra',
          'Draudimas', 'Eksportas', 'Elektronika/telekomunikacijos', 'Energetika', 'Inžinerija/mechanika',
          'Klientų aptarnavimas/paslaugos', 'Kompiuteriai/IT/internetas', 'Kultūra/kūryba', 'Logistika/transportas',
          'Maisto gamyba', 'Marketingas/reklama', 'Medicina/sveikatos apsauga/farmacija', 'Nekilnojamasis turtas',
          'Pardavimų vadyba', 'Personalo valdymas', 'Pirkimai/tiekimas', 'Pramonė/gamyba', 'Prekyba - konsultavimas',
          'Sandėliavimas', 'Statyba', 'Švietimas/mokymai', 'Teisė', 'Turizmas/viešbučiai', 'Vadovavimas/valdymas',
          'Valstybės tarnyba', 'Žemės ūkis/žuvininkystė', 'Žiniasklaida/viešieji ryšiai']

experience_cvb = [['Darbuotojo patirties sritis', 'pat:'], ['Administravimas/sekretoriavimas', 'pat:Administravimas/sekretoriavimas'], ['Apsauga', 'pat:Apsauga'], ['Apskaita/finansai/auditas', 'pat:Apskaita/finansai/auditas'], ['Dizainas/architektūra', 'pat:Dizainas/architektūra'], ['Draudimas', 'pat:Draudimas'], ['Eksportas', 'pat:Eksportas'], ['Elektronika/telekomunikacijos', 'pat:Elektronika/telekomunikacijos'], ['Energetika', 'pat:Energetika'], ['Inžinerija/mechanika', 'pat:Inžinerija/mechanika'], ['Klientų aptarnavimas/paslaugos', 'pat:Klientų aptarnavimas/paslaugos'], ['Kompiuteriai/IT/internetas', 'pat:Kompiuteriai/IT/internetas'], ['Kultūra/kūryba', 'pat:Kultūra/kūryba'], ['Logistika/transportas', 'pat:Logistika/transportas'], ['Maisto gamyba', 'pat:Maisto gamyba'], ['Marketingas/reklama', 'pat:Marketingas/reklama'], ['Medicina/sveikatos apsauga/farmacija', 'pat:Medicina/sveikatos apsauga/farmacija'], ['Nekilnojamasis turtas', 'pat:Nekilnojamasis turtas'], ['Pardavimų vadyba', 'pat:Pardavimų vadyba'], ['Personalo valdymas', 'pat:Personalo valdymas'], ['Pirkimai/tiekimas', 'pat:Pirkimai/tiekimas'], ['Pramonė/gamyba', 'pat:Pramonė/gamyba'], ['Prekyba - konsultavimas', 'pat:Prekyba - konsultavimas'], ['Sandėliavimas', 'pat:Sandėliavimas'], ['Statyba', 'pat:Statyba'], ['Švietimas/mokymai', 'pat:Švietimas/mokymai'], ['Teisė', 'pat:Teisė'], ['Turizmas/viešbučiai', 'pat:Turizmas/viešbučiai'], ['Vadovavimas/valdymas', 'pat:Vadovavimas/valdymas'], ['Valstybės tarnyba', 'pat:Valstybės tarnyba'], ['Žemės ūkis/žuvininkystė', 'pat:Žemės ūkis/žuvininkystė'], ['Žiniasklaida/viešieji ryšiai', 'pat:Žiniasklaida/viešieji ryšiai']]


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
        for page_number in range(1, 50):
            breakdashit = False
            date = None
            nav = s.post(query_link.format(page_number),data=query_info)
            print('Page number: {}'.format(page_number))
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
                        date = date_3

                        # variable giving int of how old is cv (days)
                        how_old_is_cv = days_after_edit.days
                        print(how_old_is_cv)

                        # check if CV is not too old
                        if how_old_is_cv > days_limit and not premium:
                            print('why')
                            breakdashit = True

                # find a link to CV
                cv_link = ad.find('a').get('href')

                # find some html data
                html_data = str(ad.find('div', class_="cv_list_description txt_list_2"))+'<br/>'+str(ad.find('div', class_="txt_list_1"))

                # is cv passive

                cv_passive = False


                list_of_cv_links.append([cv_link, html_data, cv_passive, False, date])

                # break loop when CVs get too old
                if breakdashit:
                    break
            if breakdashit:
                break

    info_city = query_info['miestas'] if query_info['miestas'] != '' else 'Visa Lietuva'
    info_industry = query_info['patirt_sritis[]'] if query_info['patirt_sritis[]'] != '' else 'Visos sritys'
    info_kwrd = query_info['search_string']
    info_cvold = days_limit
    query_data.append(['CVB', info_kwrd, info_city, info_industry, info_cvold])
    query_data.append(list_of_cv_links)
    return query_data



def validate_cvb_login(acc, pss):
    login_data = {'uname': acc, 'pass': pss}
    log = requests.post('http://www.cvbankas.lt/login.php', data=login_data)
    if log.url == 'http://www.cvbankas.lt/mano-skelbimu-sarasas.html':
        return "True"
    else:
        return "False"



def check_cvb_follow(user, cvs):
    """takes a list of cvs  and user object and checks if their cv update day has changed"""
    updated_cvs = []
    login_data = {'uname':user.cvb_usr, 'pass': user.cvb_pss}
    search_data_cvb = {'action':1,'miestas':'', 'patirt_sritis[]':'', 'search_string':''}
    login_link = 'http://www.cvbankas.lt/login.php'
    search_link = 'http://www.cvbankas.lt/darbuotoju-paieska#rezults_a'

    with requests.Session() as s:
        s.post(login_link, data=login_data)

        for cv in cvs:
            search_data_cvb['search_string'] = BeautifulSoup(cv.short_description, 'lxml').text[:29]
            print(BeautifulSoup(cv.short_description, 'lxml').text[:29])
            link = s.post(search_link, data=search_data_cvb)
            link_soup = BeautifulSoup(link.text, 'lxml')
            try:
                job_ad = link_soup.find('article', "list_article list_article_rememberable")
            except:
                continue
            date_1 = job_ad.find_all('div', 'txt_list_2')
            for y in date_1:
                reg = re.search("\d{4}\.\d{2}\.\d{2}", str(y))
                if reg:
                    date_2 = [int(x) for x in reg.group().split('.')]
                    date_3 = datetime.date(date_2[0], date_2[1], date_2[2])
                    if cv.date_edited < date_3:
                        updated_cvs.append([cv, date_3])
    print(updated_cvs)
    return updated_cvs

def parse_for_cats_cvb(user, url):
    login_data = {'uname':user.cvb_usr, 'pass': user.cvb_pss}
    login_link = 'http://www.cvbankas.lt/login.php'

    with requests.Session() as s:
        s.post(login_link, data=login_data)
        cv = s.get(url)
        soup = BeautifulSoup(cv.text, 'lxml')
        personal_data = soup.find(id="cv_myinfo_values").find_all('li')
        names = personal_data[0].text.split(' ')
        firstname, lastname = names[0], names[1]
        phone = ''
        email = ''
        for x in personal_data:
            regular_phone = re.search('\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d', x.text)
            regular_email = re.search('.*@.*', x.text)
            if regular_phone:
                phone = x.text
            if regular_email:
                email = x.text

        with open('cvtest.html', 'wb') as j:
            j.write(cv.content)
        return firstname, lastname, phone, email
