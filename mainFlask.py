#!/usr/local/bin/python3.4
from flask import Flask, g, request, render_template, url_for, session, flash,redirect, jsonify, abort
from mainCVB import cities_cvb, industries_cvb, check_cvb_follow, parse_for_cats_cvb
from mainCVO import cities_cvo, industries_cvo, cities_cvo_numbers, industries_cvo_numbers, check_cvo_follow, parse_for_cats_cvo
from router import recognize_dat_data_and_find_cvs, somejs, validate_logins
import urllib, datetime,os, json, re
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required, logout_user, current_user
from flask.ext.cache import Cache
from mainCatsone import cats_api



app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY="soseceret",
    DEBUG=True,
    #DATABASE=os.path.join(app.root_path, 'schema.db')
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(app.root_path, 'Database7.db')
))

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'



@app.route('/')
@login_required
def main():
    mainpage_html_data = {'experience_cvo': '', 'experience_cvb': '', 'cities_cvb':cities_cvb, 'cities_cvo':cities_cvo,'industries_cvb':industries_cvb,'industries_cvo':industries_cvo, 'Location':'Location ','Industry':'Industry ',
             'Database': 'Database ', 'More_options': 'More', 'Keywords': 'Keywords', 'cvold': '0',
             'Search':'Add query', 'results':'', 'noice_js':'', 'type':'submit', 'id':'search', 'disable':'', 'user': g.user.email}

    user = g.user
    queries_0 = Queries.query.filter_by(user_name=user.email).all()
    queries = []
    for x in queries_0:
        if x.search_data == '' and x.display == 1:
            queries.append(x)
    mainpage_html_data['queries'] = render_template('renderqueries.html', queries=queries)
    if user.cvb_usr == '' or user.cvo_usr == '':
        mainpage_html_data['warning'] = ''
        print('no settings')
    print('main before render')
    return render_template('mainpage.html', **mainpage_html_data)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user=g.user
    render_data = {'cvb_acc': user.cvb_usr, "cvb_pss": '', "cvo_acc": user.cvo_usr, "cvo_pss": '', 'cats_api_key': user.cats_key}
    if request.method == "GET":
        return jsonify({'data': render_template('settings.html', **render_data)})
    if request.method == "POST":
        data_0 = urllib.parse.unquote(request.get_json())
        data = dict(a.split('=') for a in data_0.split('&'))
        if 'cats' in data:
            cats = cats_api(data['cats'])
            response = cats.get_joborders(check_key=True)
        else:
            response = validate_logins(data['website'], data['username'], data['password'])
        if "True" in response and 'cvo' in response:
            print('cvo')
            user.cvo_usr = data['username']
            user.cvo_pss = data['password']
        elif "True" in response and 'cvb' in response:
            print('cvb:(')
            user.cvb_usr = data['username']
            user.cvb_pss = data['password']
        elif "True" in response and "Cats" in response:
            user.cats_key = data['cats']
        db.session.add(user)
        db.session.commit()
        return jsonify({'response': response[0]})


@app.route('/modal', methods=['POST'])
@login_required
def modal():
    cats = cats_api(g.user.cats_key)
    data = request.get_json()
    if 'get' in data:
        job_orders, lists = get_lists_and_joborders(cats)
        return jsonify({'data': render_template('modal.html', joborders=job_orders, lists=lists, cv_id=data['get'])})
    else:
        data_dict = parse_json(data['form_data'])
        print(data_dict)
        cv_id = data['cv_id']
        cv = Url_data.query.filter_by(id=int(cv_id)).first()
        notes = data_dict['textarea']+'\n CV Link: {}'.format(cv.url)
        job_order = None
        list_id= None
        result_candidate = None
        for x in data_dict: #get job order id and list id
            reg_list = re.search('static:\d*', x)
            reg_job = re.search('\d{7}',x)
            if reg_list:
                list_id = reg_list.group(0)[7:]
            if reg_job:
                job_order = reg_job.group(0)
        if json.loads(cv.info)[0] == 'CVB':
            firstn, lastn, phone, email = parse_for_cats_cvb(g.user, cv.url)
        else:
            firstn, lastn, phone, email = parse_for_cats_cvo(g.user, cv.url)
        result_candidate, result_job, result_list = cats.add_candidate(firstn, lastn, phone, email, notes, job_id=job_order, list_id=list_id)
        print('candidate: {}, job_order: {}, list {}'.format(result_candidate, result_job, result_list))
        if result_candidate == 'true':
            cv.save_to_cats = True
            db.session.add(cv)
            db.session.commit()
        return jsonify({'a':4})


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    mainpage_html_data = {'experience_cvo': '', 'experience_cvb': '', 'cities_cvb':cities_cvb, 'cities_cvo':cities_cvo,'industries_cvb':industries_cvb,'industries_cvo':industries_cvo, 'Location':'Location ','Industry':'Industry ',
             'Database': 'Database ', 'More_options': 'More options ', 'Keywords': 'Keywords', 'cvold': '0',
             'Search':'Search', 'results':'', 'noice_js':'', 'type':'submit', 'id':'search'}
    if request.method == "GET":
        mainpage_html_data['justsearch'] = True
        return jsonify({'data': render_template('search.html', **mainpage_html_data)})
    if request.method == "POST":
        n = urllib.parse.unquote(request.get_json())
        m = dict(a.split('=') for a in n.split('&'))
        print('search {}'.format(m))
        result, city, industry, kwrds, cvold = recognize_dat_data_and_find_cvs(m, g.user, query_data=True)
        query_id = make_query_and_url_db_data(g.user, city, industry, kwrds, cvold, result, return_=True, search=True)
        queries_data_CVB = [['CVB']]
        queries_data_CVO = [['CVO']]
        queries_data_all = []
        queries_data_list_CVB = []
        queries_data_list_CVO = []
        for number, search_info in enumerate(result):
            search_data = search_info[1]
            if search_info[0][0] == 'CVB':
                for cv_data in search_data:
                    queries_data_list_CVB.append([cv_data[0], str(cv_data[1]), cv_data[2], False, False, number, False, False, cv_data[4].strftime("%Y-%m-%d")])
            elif search_info[0][0] == 'CVO':
                for cv_data in search_data:
                    queries_data_list_CVO.append([cv_data[0], str(cv_data[1]), cv_data[2], False, False, number, False, False, cv_data[4].strftime("%Y-%m-%d")])
        if len(queries_data_list_CVB) > 0:
                queries_data_CVB.append(queries_data_list_CVB)
                queries_data_all.append(queries_data_CVB)
        if len(queries_data_list_CVO) > 0:
                queries_data_CVO.append(queries_data_list_CVO)
                queries_data_all.append(queries_data_CVO)
        query = Queries.query.filter_by(id=query_id).first()
        query.search_data = json.dumps(queries_data_all)
        db.session.add(query)
        db.session.commit()
        print('query id {}, type {}'.format(query_id, type(query_id)))
        return redirect(url_for('display', query=query_id, first=False, search=True))

@app.route('/displayquery', methods=['GET', 'POST'])
@login_required
def display():
    mainpage_html_data = {'experience_cvo': '', 'experience_cvb': '', 'cities_cvb':cities_cvb, 'cities_cvo':cities_cvo,'industries_cvb':industries_cvb,'industries_cvo':industries_cvo, 'Location':'Location ','Industry':'Industry ',
             'Database': 'Database ', 'More_options': 'More options ', 'Keywords': 'Keywords', 'cvold': '0',
             'Search':'Add query', 'results':'', 'noice_js':'', 'type':'submit', 'id':'search', 'selected_cities':'', 'selected_industries':''}
    print('this is display!!')

    user = g.user
    query_id= None
    is_first_query = False

    if request.get_json():
        query_id = request.get_json()
    elif request.args['query']:
        query_id = request.args['query']
        is_first_query = False if request.args['first'] == 'False' else True

    is_search = True if "search" in request.args else False
    print('is search {}'.format(is_search))
    one_query = Queries.query.filter_by(user_name=user.email, id=query_id).first()

    def get_query(one_query):
        latest_query = one_query
        mainpage_html_data['selected_cities'] = latest_query.city.split(',')
        mainpage_html_data['selected_industries'] = latest_query.industry.split(',')
        mainpage_html_data['Keywords'] = latest_query.kwrds
        mainpage_html_data['cvold'] = latest_query.cv_old
        mainpage_html_data['Search'] = 'Update'
        mainpage_html_data['noice_js'] = somejs
        mainpage_html_data['id'] = 'update'
        mainpage_html_data['type'] = 'submit'

        #construct list for result template
        queries_data = Url_data.query.filter_by(cv_query_id=latest_query.id).all()

        queries_data_CVB = [['CVB']]
        queries_data_CVO = [['CVO']]
        queries_data_all = []
        queries_data_list_CVB = []
        queries_data_list_CVO = []

        for one_data in queries_data:
            info = json.loads(one_data.info)

            # url data container
            one_url = []
            one_url.append(one_data.url)
            one_url.append(one_data.short_description)
            one_url.append(one_data.passive)
            one_url.append(one_data.viewed)
            one_url.append(one_data.follow)
            one_url.append(one_data.id)
            one_url.append(one_data.save_to_cats)
            one_url.append(one_data.hot)
            one_url.append(one_data.date_edited)


            #make HOT CVs appear at the top
            if one_url[7] is True:
                if info[0] == 'CVB':
                    queries_data_list_CVB.insert(0, one_url)
                elif info[0] == 'CVO':
                    queries_data_list_CVO.insert(0, one_url)
            else:
                if info[0] == 'CVB':
                    queries_data_list_CVB.append(one_url)
                elif info[0] == 'CVO':
                    queries_data_list_CVO.append(one_url)

        if len(queries_data_list_CVB) > 0:
                queries_data_CVB.append(queries_data_list_CVB)
                queries_data_all.append(queries_data_CVB)
        if len(queries_data_list_CVO) > 0:
                queries_data_CVO.append(queries_data_list_CVO)
                queries_data_all.append(queries_data_CVO)


        mainpage_html_data['results'] = render_template('results.html', queries_data=queries_data_all,
                                                        query_id=query_id)
    if not is_search:
        print('not search')
        get_query(one_query)
    else:
        print('yes search')
        mainpage_html_data['results'] = json.loads(Queries.query.filter_by(id=query_id).first().search_data)
        return jsonify({'data': render_template('results.html', queries_data=mainpage_html_data['results'],
                                                        query_id=query_id, search=True)})


    # when redirected on first search of the query..
    if is_first_query:
        print('Adding new query to menu')
        queries = render_template('renderqueries.html', queries=Queries.query.filter_by(user_name=user.email).all())
        return jsonify({'data': mainpage_html_data['results'], 'queries': queries})

    print('search.html<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    return jsonify({'data': render_template('search.html', **mainpage_html_data)})


@app.route('/result', methods=['POST'])
@login_required
def result():
    n = urllib.parse.unquote(request.get_json())
    m = dict(a.split('=') for a in n.split('&'))
    print('/result{}: '.format(m))
    result, city, industry, kwrds, cvold = recognize_dat_data_and_find_cvs(m, g.user, query_data=True)
    query_id = make_query_and_url_db_data(g.user, city, industry, kwrds, cvold, result, return_=True)
    return redirect(url_for('display', query=query_id, first=True))


@app.route('/update', methods=['POST'])
@login_required
def update():
    print('/update{} '.format(request.get_json()))
    data = request.get_json()
    if 'url' in data:
        url = Url_data.query.filter_by(id=data['id']).first()
        url.viewed = False if data['viewed'] == 'False' else True
        url.date_viewed = datetime.date.today()
        if url.hot is True and data['viewed'] == 'True':
            url.hot = False
        db.session.add(url)
        db.session.commit()
        return jsonify({'data':''})

    elif 'follow' in data:
        url = Url_data.query.filter_by(id=data['id']).first()
        url.follow = False if data['follow'] == 'False' else True
        db.session.add(url)
        db.session.commit()
        return jsonify({'data':''})

    elif 'query_id' in data:
        query_id = data['query_id']
        updated_info = parse_json(data['data'])
        user = g.user
        old_urls = Url_data.query.filter_by(cv_query_id=query_id).all()
        query_class = Queries.query.filter_by(id=query_id).first()
        today_urls = recognize_dat_data_and_find_cvs(make_query_dictionary(query_class, updated_info, query_id), user)
        check_for_new_urls(old_urls, today_urls, query_class)
        return redirect(url_for('display', query=query_id, first=False))
    elif 'display' in data:
        query = Queries.query.filter_by(id=data['display']).first()
        query.display = False
        db.session.add(query)
        db.session.commit()
        return jsonify({'data':''})

@app.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    if request.method == 'GET':
        user = g.user
        hours_since_follow_check = datetime.datetime.now() - user.date_follow_check
        if hours_since_follow_check.seconds >= 43200:
            update_followed_cvs(user)
            user.date_follow_check = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
        return jsonify({'data':render_template('followed.html', data=take_followed_cvs_from_db(user))})


################# login system ##################
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    print(data)
    old_usr = User.query.filter_by(email=data['email']).first()
    if old_usr is None:
        new_user = User(data['email'], data['password'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('main'))
    print('disss')
    return render_template('login.html', error="Username taken")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print('login')
    if request.method == 'GET':
        return render_template('login.html', error=error)

    usr = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
    if usr is None:
        print('hi2')
        error = 'Invalid username or password'
        return render_template('login.html', error=error)
    login_user(usr, remember=True)
    print('hi3')
    return redirect(url_for('main'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

################# login system ##################


@app.route('/test')
@login_required
def test():
    return render_template('test.html')


################ Database ##################

db = SQLAlchemy(app)

def make_query_and_url_db_data(user, city, industry, kwrds, cvold, urls, query_class=None, return_=False, search=False):

    if query_class:
        mk_qeury = query_class
    else:
        mk_qeury = Queries(city,
                           industry,
                           kwrds,cvold,user, datetime.datetime.now())

    if not search:
        for cv_packet in urls:
            info = json.dumps(cv_packet[0])
            for cv in cv_packet[1]:

                mk_url_data = Url_data(info, cv[0], str(cv[1]), cv[2], False, False, False, cv[3], cv[4], mk_qeury)
                db.session.add(mk_url_data)

    db.session.add(mk_qeury)
    db.session.commit()

    if return_:
        return mk_qeury.id

def update_query(new_cv_old):
    pass

def update_url_data():
    pass

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String(120), unique=True)
    cats_key = db.Column(db.String, default='')

    cvo_usr = db.Column(db.String, default='')
    cvo_pss = db.Column(db.String, default='')

    cvb_usr = db.Column(db.String, default='')
    cvb_pss = db.Column(db.String, default='')

    date_follow_check = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)


class Queries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    industry = db.Column(db.String)
    kwrds = db.Column(db.String)
    cv_old = db.Column(db.Integer)
    user_name = db.Column(db.String, db.ForeignKey('user.email'))
    search_data = db.Column(db.String, default='')
    display = db.Column(db.Boolean, default=True)

    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_parsed = db.Column(db.DateTime)

    user = db.relationship('User', backref='queries')

    def __init__(self, city, industry, kwrds, cv_old, user, date_parsed):
        self.city = city
        self.industry = industry
        self.kwrds = kwrds
        self.cv_old = cv_old
        self.user = user
        self.date_parsed = date_parsed

class Url_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String)
    url = db.Column(db.String)
    viewed = db.Column(db.Boolean, default=False)
    save_to_cats = db.Column(db.Boolean, default=False)
    follow = db.Column(db.Boolean, default=False)
    short_description = db.Column(db.String)
    passive = db.Column(db.Boolean, default=False)
    cv_query_id = db.Column(db.Integer, db.ForeignKey('queries.id'))
    date_parsed = db.Column(db.DateTime, default=datetime.datetime.now())
    date_viewed = db.Column(db.Date, default=datetime.date.today())
    hot = db.Column(db.Boolean, default=False)
    date_edited = db.Column(db.Date)

    cv_query = db.relationship('Queries', backref='url_data')


    def __init__(self, info, url, short_description, passive, viewed, save_to_cats, follow, hot, date_edited, cv_query):
        self.info = info
        self.url = url
        self.viewed = viewed
        self.save_to_cats = save_to_cats
        self.follow = follow
        self.cv_query = cv_query
        self.short_description = short_description
        self.passive = passive
        self.hot = hot
        self.date_edited = date_edited

############### Database#############################


############### Functions###########################

def parse_json(data):
    data_0 = urllib.parse.unquote(data)
    return dict(a.split('=') for a in data_0.split('&'))

@cache.cached(timeout=280,key_prefix='wtfnigga')
def get_lists_and_joborders(cats):
    job_orders = cats.get_joborders()
    lists = cats.get_lists()
    return job_orders, lists


def make_query_dictionary(q_class, updated, q_id):
    q_dictionary = {'kwrds': q_class.kwrds, 'CVold': str(q_class.cv_old)}
    cities = q_class.city
    if cities != '':
        for city in cities.split(','):
            q_dictionary[city] = 'on'
    industries = q_class.industry
    if industries != '':
        for industry in industries.split(','):
            q_dictionary[industry] = 'on'

    ### look for new updated query data ###
    if updated['CVold'] != '':
        if int(updated['CVold']) > int(q_dictionary['CVold']):
            q_dictionary['CVold'] = updated['CVold']
            q = Queries.query.filter_by(id=q_id).first()
            q.cv_old = q_dictionary['CVold']
            db.session.add(q)
            db.session.commit()

    keys_old, keys_new = q_dictionary.keys(), updated.keys()
    for key in keys_new:
        if key not in keys_old:
            q_dictionary[key] = updated[key]
            q = Queries.query.filter_by(id=q_id).first()
            if key in cities_cvb or key in cities_cvo_numbers:
                q.city = q.city + ',' + q_dictionary[key]
            elif key in industries_cvb or key in industries_cvo_numbers:
                q.industry = q.industry + ',' + q_dictionary[key]
            db.session.add(q)
            db.session.commit()
    ### look for new updated query data ###
    print('updatinimo dic: {}'.format(q_dictionary))

    return q_dictionary

def check_for_new_urls(old_urls, today_urls, query_class):
    old_links_andpassive = {}
    old_links_cvo_ids = {}
    new_links = []
    for x in old_urls:
        old_links_andpassive[x.url] = [x.passive, x.id]
        reg = re.search('CVC\/\d{5,}', x.url)
        if reg:
            old_links_cvo_ids[reg.group(0)] = x.id
    print(old_links_cvo_ids)
    for y in today_urls:
        for z in y[1]:
            if z[0] not in old_links_andpassive:
                reg = re.search('CVC\/\d{5,}', z[0]) # ar cvo linkas
                if reg:
                    if reg.group(0) in old_links_cvo_ids:
                        url = Url_data.query.filter_by(id=old_links_cvo_ids[reg.group(0)]).first()
                        if url.follow is True:
                            url.date_edited = z[4]
                            if z[4] > url.date_viewed:
                                url.hot = True
                            db.session.add(url)
                            db.session.commit()
                        print('senas: {}'.format(z[0]))
                        continue
                z[3] = True
                new_links.append([y[0], [z]])              # [[[info][url, html, passive..]], [info][url. html, passive..]]]
            else:
                url = Url_data.query.filter_by(id=old_links_andpassive[z[0]][1]).first()
                if z[2] != old_links_andpassive[z[0]][0]:      # jeigu ne be passive
                    print('sio neturi printint')
                    if z[2] is False:
                        url.passive = False
                        url.hot = True

                    else:
                        pass
                if url.follow is True:         #if follow check if cv update date has changed
                    url.date_edited = z[4]
                    if z[4] > url.date_viewed: #if cv updated sooner than last view, make cv hot
                        url.hot = True
                    db.session.add(url)
                    db.session.commit()

    make_query_and_url_db_data(User.query.filter_by(email=query_class.user_name),
                               None, None, None, None,
                               new_links,
                               query_class=query_class)


def update_followed_cvs(user):
    cvs = take_followed_cvs_from_db(user)
    cvb=[]
    cvo=[]
    for cv in cvs:
        cv_db = cv[1][0]
        if cv_db == 'CVB':
            cvb.append(cv[0])
        else:
            cvo.append(cv[0])
    for updated_cv in check_cvo_follow(user, cvo):
        updated_cv[0].date_edited = updated_cv[1]
        updated_cv[0].hot = True
        db.session.add(updated_cv[0])
    for updated_cv in check_cvb_follow(user, cvb):
        updated_cv[0].date_edited = updated_cv[1]
        updated_cv[0].hot = True
        db.session.add(updated_cv[0])
    db.session.commit()

def take_followed_cvs_from_db(user):
        folowed_cvs = Url_data.query.filter_by(follow=True).all()
        user_queries = Queries.query.filter_by(user_name=user.email).all()
        user_queries_ids = [x.id for x in user_queries]
        followed_user_cvs = []
        for x in folowed_cvs:
            if x.cv_query_id in user_queries_ids:
                followed_user_cvs.append([x,json.loads(x.info)])
        return followed_user_cvs


############### Functions###########################




if __name__ == '__main__':
    app.run(debug=True)



