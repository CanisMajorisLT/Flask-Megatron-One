import requests
from bs4 import BeautifulSoup


tran_code = 'fb28effc75c37f025e1a57fde616267b'

class cats_api:
    def __init__(self, key):
        self.key = key
        self.domain = 'talentlab'

    def get_joborders(self):
        joborders = []
        xml = requests.get('https://{}.catsone.com/api/get_joborders?transaction_code={}{}'.format(self.domain,
                                                                                                   self.key,
                                                                                                   '&rows_per_page=50'))
        soup = BeautifulSoup(xml.text, 'lxml')
        for x in soup.find_all('item'):
            joborders.append([x.title.string, x.item_id.string])
        return joborders

    def add_candidate(self, first_name, last_name, phone_cell, notes):
        resume = {'resume': open('nice.pdf', 'rb')}
        x = requests.post('https://{}.catsone.com/api/add_candidate?transaction_code={}{}{}{}{}'.format(
            self.domain, self.key, '&first_name={}'.format(first_name), '&last_name={}'.format(last_name),
            '&phone_cell={}'.format(phone_cell), '&notes={}'.format(notes)), files=resume)
        return x.text

    def get_lists(self):
        lists = []
        xml = requests.get('https://{}.catsone.com/api/get_lists?transaction_code={}{}'.format(self.domain,
                                                                                               self.key,
                                                                                               '&rows_per_page=50'))
        soup = BeautifulSoup(xml.text, 'lxml')
        for x in soup.find_all('item'):
            lists.append([x.find('name').string, x.item_id.string, x.num.string])
        return lists


