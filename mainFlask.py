
from flask import Flask, g, request, render_template, url_for, session, flash,redirect, jsonify, abort
from mainCVB import cities, industries
from router import recognize_dat_data_and_find_cvs, somejs
import urllib, datetime,os, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc



app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY="soseceret",
    DEBUG=True,
    #DATABASE=os.path.join(app.root_path, 'schema.db')
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(app.root_path, 'Database4.db')
))


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'



@app.route('/')
@login_required
def main():
    mainpage_html_data = {'cities':cities,'industries':industries, 'Location':'Location ','Industry':'Industry ',
             'Database': 'Database ', 'More_options': 'More options ', 'Keywords': 'Keywords', 'cvold': '0',
             'Search':'Add query', 'results':'', 'noice_js':'', 'type':'submit', 'id':'search', 'disable':''}

    user = g.user
    queries = Queries.query.filter_by(user_name=user.email).all()
    mainpage_html_data['queries'] = queries

    return render_template('mainpage.html', **mainpage_html_data)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    mainpage_html_data = {'cities':cities,'industries':industries, 'Location':'Location ','Industry':'Industry ',
             'Database': 'Database ', 'More_options': 'More options ', 'Keywords': 'Keywords', 'cvold': '0',
             'Search':'Search', 'results':'', 'noice_js':'', 'type':'submit', 'id':'search'}
    if request.method == "GET":
        return jsonify({'data': render_template('search.html', **mainpage_html_data)})
    if request.method == "POST":
        n = urllib.parse.unquote(request.get_json())
        m = dict(a.split('=') for a in n.split('&'))
        print('search {}'.format(m))
        result = recognize_dat_data_and_find_cvs(m, query_data=False)
        return jsonify({'data': render_template('results.html', queries_data=result)})

@app.route('/displayquery',methods=['GET', 'POST'])
@login_required
def display():
    mainpage_html_data = {'cities':cities,'industries':industries, 'Location':'Location ','Industry':'Industry ',
             'Database': 'Database ', 'More_options': 'More options ', 'Keywords': 'Keywords', 'cvold': '0',
             'Search':'Add query', 'results':'', 'noice_js':'', 'type':'submit', 'id':'search', 'disable':''}

    user = g.user
    query_id= None
    is_first_query = False

    if request.get_json():
        query_id = request.get_json()
    elif request.args['query']:
        query_id = request.args['query']
        is_first_query = request.args['first']


    one_query = Queries.query.filter_by(user_name=user.email, id=query_id).first()

    def get_query(one_query):
        latest_query = one_query
        mainpage_html_data['Location'] = latest_query.city.replace(',', ', ')
        mainpage_html_data['Industry'] = latest_query.industry.replace(',', ', ')
        mainpage_html_data['Keywords'] = latest_query.kwrds
        mainpage_html_data['cvold'] = latest_query.cv_old
        mainpage_html_data['Search'] = 'Update'
        mainpage_html_data['noice_js'] = somejs
        mainpage_html_data['id'] = 'update'
        mainpage_html_data['type'] = 'button'
        mainpage_html_data['disable'] = 'disabled'

        #construct list for result template
        queries_data = Url_data.query.filter_by(cv_query_id=latest_query.id).all()

        queries_data_list_3 = []
        queries_data_list_2 = []
        queries_data_list_1 = []
        position = None

        for one_data in queries_data:
            info = json.loads(one_data.info)
            if position is None:
                queries_data_list_2.append(info)
                position = 0
            if queries_data_list_2[position] != info:
                queries_data_list_2.append(queries_data_list_1)
                queries_data_list_3.append(queries_data_list_2)
                queries_data_list_2 = []
                queries_data_list_1 = []
                queries_data_list_2.append(info)

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



            queries_data_list_1.append(one_url)

        queries_data_list_2.append(queries_data_list_1)
        queries_data_list_3.append(queries_data_list_2)

        mainpage_html_data['results'] = render_template('results.html', queries_data=queries_data_list_3, query_id=query_id)

    get_query(one_query)

    # when redirected on first search of the query..
    if is_first_query:
        return jsonify({'data': mainpage_html_data['results']})

    return jsonify({'data': render_template('search.html', **mainpage_html_data)})


@app.route('/result', methods=['POST'])
@login_required
def result():
    n = urllib.parse.unquote(request.get_json())
    m = dict(a.split('=') for a in n.split('&'))
    print('/result{}: '.format(m))
    result, city, industry, kwrds, cvold = recognize_dat_data_and_find_cvs(m, query_data=True)
    query_id = make_query_and_url_db_data(g.user, city, industry, kwrds, cvold, result, return_=True)
    #session['query_id'] = query_id
    return redirect(url_for('display', query=query_id, first=True))

    #return jsonify({'data': render_template('results.html', queries_data=result)})


@app.route('/update', methods=['POST'])
@login_required
def update():
    print('/update{} '.format(request.get_json()))
    data = request.get_json()
    if 'url' in data:
        url = Url_data.query.filter_by(id=data['id']).first()
        url.viewed = False if data['viewed'] == 'False' else True
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
        old_urls = Url_data.query.filter_by(cv_query_id=query_id).all()
        query_class = Queries.query.filter_by(id=query_id).first()
        today_urls = recognize_dat_data_and_find_cvs(make_query_dictionary(query_class))
        check_for_new_urls(old_urls, today_urls, query_class)
        return redirect(url_for('display', query=query_id, first=False))


################# login system ##################

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'GET':
        print('hi1')
        return render_template('login.html', error=error)

    usr = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
    #print(usr)
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

def make_query_and_url_db_data(user, city, industry, kwrds, cvold, urls, query_class=None, return_=False):

    if query_class:
        mk_qeury = query_class
    else:
        mk_qeury = Queries(city if len(city) > 0 else 'Location',
                           industry if len(industry) > 0 else 'Industry',
                           kwrds,cvold,user, datetime.datetime.now())

    for cv_packet in urls:
        info = json.dumps(cv_packet[0])
        for cv in cv_packet[1]:

            mk_url_data = Url_data(info, cv[0], str(cv[1]), cv[2], False, False, False, cv[3], mk_qeury)
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
    hot = db.Column(db.Boolean, default=False)

    cv_query = db.relationship('Queries', backref='url_data')


    def __init__(self, info, url, short_description, passive, viewed, save_to_cats, follow, hot, cv_query):
        self.info = info
        self.url = url
        self.viewed = viewed
        self.save_to_cats = save_to_cats
        self.follow = follow
        self.cv_query = cv_query
        self.short_description = short_description
        self.passive = passive
        self.hot = hot

############### Database#############################


############### Functions###########################

def make_query_dictionary(q_class):
    q_dictionary = {'kwrds': q_class.kwrds, 'CVold': str(q_class.cv_old)}
    cities = q_class.city
    if cities != 'Location':
        for city in cities.split(','):
            q_dictionary[city] = 'on'
    industries = q_class.industry
    if industries != 'Industry':
        for industry in industries.split(','):
            q_dictionary[industry] = 'on'
    return q_dictionary

def check_for_new_urls(old_urls, today_urls, query_class):
    old_links_passive = {}
    new_links = []
    for x in old_urls:
        old_links_passive[x.url] = [x.passive, x.id]
    for y in today_urls:
        for z in y[1]:
            if z[0] not in old_links_passive:
                z[3] = True
                new_links.append([y[0], [z]])              # [[[info][url, html, passive..]], [info][url. html, passive..]]]
            else:
                if z[2] != old_links_passive[z[0]][0]:      # jeigu ne be passive
                    print('sio neturi printint')
                    if z[2] is False:
                        url = Url_data.query.filter_by(url=old_links_passive[z[2][1]])
                        url.passive = False
                        url.hot = True
                        db.session.add(url)
                        db.session.commit()
                    else:
                        pass
    print(new_links)
    print(today_urls)
    make_query_and_url_db_data(User.query.filter_by(email=query_class.user_name),
                               None, None, None, None,
                               new_links,
                               query_class=query_class)




############### Functions###########################





if __name__ == '__main__':
    app.run(debug=True)



