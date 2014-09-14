import requests, pdfkit
from bs4 import BeautifulSoup


tran_code = 'fb28effc75c37f025e1a57fde616267b'

class cats_api:
    def __init__(self, key):
        self.key = key
        self.domain = 'talentlab'

    def get_joborders(self, check_key=False):
        joborders = []
        xml = requests.get('https://{}.catsone.com/api/get_joborders?transaction_code={}{}'.format(self.domain,
                                                                                                   self.key,
                                                                                                   '&rows_per_page=50'))
        if check_key:
            response = self.soup_response(xml.text)
            if response == 'invalid or incorrect transaction_code':
                return ['False', 'Cats']
            else:
                return ['True', 'Cats']
        soup = BeautifulSoup(xml.text, 'lxml')
        for x in soup.find_all('item'):
            joborders.append([str(x.title.string), str(x.item_id.string)])
        return joborders

    def get_lists(self):
        lists = []
        xml = requests.get('https://{}.catsone.com/api/get_lists?transaction_code={}{}'.format(self.domain,
                                                                                               self.key,
                                                                                               '&rows_per_page=50'))
        soup = BeautifulSoup(xml.text, 'lxml')
        for x in soup.find_all('item'):
            lists.append([str(x.find('name').string), str(x.item_id.string), str(x.num.string)])
        return lists

    def add_candidate(self, first_name, last_name, phone_cell, email, notes, job_id=False, list_id=False):
        resume = {'resume': open('cvtest.html', 'rb')}
        x = requests.post('https://{}.catsone.com/api/add_candidate?transaction_code={}{}{}{}{}{}'.format(
            self.domain, self.key, '&first_name={}'.format(first_name), '&last_name={}'.format(last_name),
            '&phone_cell={}'.format(phone_cell),'&email1={}'.format(email), '&notes={}'.format(notes)), files=resume)
        print(x.text)
        soup = BeautifulSoup(x.text)

        if soup.find('response').get('success') == 'false':
            return soup.error.text, 'cverror', 'cverror'

        candidate_id = soup.id.text
        info_job_id = None
        info_list = None
        if job_id:
            print('job id{}'.format(job_id))
            info_job_id = self.soup_response(self.add_to_pipeline(job_id, candidate_id))

        if list_id:
            print('list id{}'.format(list_id))
            info_list = self.soup_response(self.add_to_list(list_id, candidate_id))

        return self.soup_response(x.text), info_job_id, info_list

    def add_to_pipeline(self, job_id, candidate_id):
        x = requests.post('https://{}.catsone.com/api/add_pipeline?transaction_code={}{}{}'.format(
            self.domain, self.key, '&candidate_id={}'.format(candidate_id), '&joborder_id={}'.format(job_id)))
        return x.text

    def add_to_list(self, list_id, candidate_id):
        x = requests.post('https://{}.catsone.com/api/add_to_list?transaction_code={}{}{}'.format(
        self.domain, self.key, '&data_item_id={}'.format(candidate_id), '&list_id={}'.format(list_id)))
        return x.text


    def soup_response(self, text):
        soup = BeautifulSoup(text, 'lxml')
        response = soup.find('response').get('success')
        if response == 'false':
            return soup.error.text
        return response


