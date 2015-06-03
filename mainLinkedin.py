__author__ = 'vyt'
import requests
import logging, time, json, random, re
from bs4 import BeautifulSoup


class linkedin_inbox_api():

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.url_inbox = "https://www.linkedin.com/inbox/sent?startRow={}1&subFilter=&keywords=&sortBy=&trk=inbox_sent-comm-left_nav-sent"

    def get_session(self):
        with requests.Session() as s:
            logging.info('Get session')
            return  s

    def log_in(self):
        data = {'session_password': self.password, 'session_key': self.login}
        s = self.get_session()
        get_csrf = s.get('https://www.linkedin.com')
        soup = BeautifulSoup(get_csrf.content)
        data['loginCsrfParam'] = soup.find(id="loginCsrfParam-login")['value']
        time.sleep(2)
        s.post("https://www.linkedin.com/uas/login-submit", data = data)
        time.sleep(1)
        return s

    def get_invitations(self):
        pass

    def get_inbox(self):
        "gets the whole inbox from scratch"
        print('getting_inbox')
        inbox_data = dict()
        session = self.log_in()
        number_of_pages = self.get_number_of_pages(session)
        return self.parse_inbox_pages(inbox_data, session, number_of_pages)


    def update_inbox(self, inbox):
        "looks if there are any new messages in the inbox"
        session = self.log_in()
        number_of_pages_in_inbox = self.get_number_of_pages(session)
        #with open('inbox_data.json', 'r') as data:
        #    inbox_data = json.loads(data.read())
        inbox_data = inbox
        number_of_pages_parsed = inbox_data['page'] if inbox_data['page'] is int else 10
        number_of_pages_to_parse = number_of_pages_in_inbox - number_of_pages_parsed
        print("Number of pages to update: {}".format(number_of_pages_to_parse))
        return self.parse_inbox_pages(inbox_data, session, number_of_pages_to_parse)


    def parse_one_message(self, one_item):
        "parses one message data and returns list where first member is name and second is list of data"

        subject = one_item.find('a', class_="detail-link").text.replace("\n",'')
        message_type = 'Invitation' if subject == "Join my network on LinkedIn" else "Message"
        invitation_status = 'Accepted' if one_item.find('span', class_="item-status item-status-accepted") else None
        time = one_item.find('span', class_="time-millis hidden").text
        name_of_receiver = one_item.find('span', class_="participants").text.split(':')[-1].replace("\n",'')[1:]
        message_preview = one_item.find('p', class_="preview not-empty").text.replace("\n", ' ')
        return [name_of_receiver, [message_type, invitation_status, time, message_preview, subject]]


    def get_number_of_pages(self, session):
        "returns number of pages in inbox"
        number_of_pages = int(BeautifulSoup(session.get(self.url_inbox.format('')).text).find('li', class_='page').text.split(' ')[-1])
        return number_of_pages

    def parse_inbox_pages(self, old_inbox_data, session, number_of_pages):
        "parses given number of inbox pages starting from the latest (newest)"
        current_newest_message, last_newest_message = None, None
        last_message_parsed = None
        is_first_parse = True
        finished_parse = "False"
        inbox_data = old_inbox_data
        keys_of_inbox_data = inbox_data.keys()
        if "newest_message" in keys_of_inbox_data:
            last_newest_message = inbox_data["newest_message"]
        if 'last_message_parsed' in keys_of_inbox_data:
            last_message_parsed = inbox_data['last_message_parsed']
        if "messages" not in inbox_data:
            inbox_data["messages"] = dict()

        for page_number in range(number_of_pages):
            if page_number == 0:
                page_number = ''
            one_page_of_inbox = session.get(self.url_inbox.format(page_number))
            one_page_of_inbox_soup = BeautifulSoup(one_page_of_inbox.text).find_all('li', class_=re.compile("inbox-item"))
            assert len(one_page_of_inbox_soup) == 10
            for one_item in one_page_of_inbox_soup:
                message_data = self.parse_one_message(one_item)
                print(message_data)
                if is_first_parse:
                    is_first_parse, inbox_data['newest_message'] = False, message_data
                if last_newest_message: # when updating if current message equals the newest message of last time return
                    if message_data == last_newest_message:
                        print("Last msg. parsed == This msg.:{}".format(message_data))
                        print("Newest msg. parsed == This msg.:{}".format(inbox_data['newest_message']))
                        return inbox_data
                if message_data[0] in inbox_data['messages']:
                    inbox_data['messages'][message_data[0]].append(message_data[1])
                else:
                    inbox_data['messages'][message_data[0]] = [message_data[1]]
                    last_message_parsed = message_data

                if page_number == number_of_pages -1:
                    finished_parse = "True"

            time.sleep(random.randint(3, 10))
            print('Page {}'.format(page_number))
            inbox_data['page'] = page_number
            inbox_data['last_message_parsed'], inbox_data['fully_finished_last_parse'] = last_message_parsed, finished_parse
            with open('inbox_data.json', 'w') as data:
                data.write(json.dumps(inbox_data))
        return inbox_data

#user = linkedin_inbox_api('vytenis.butkevicius@gmail.com','frankas39321')
#user.get_inbox()
