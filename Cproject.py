from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Chocolate, ChocoTypes, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
from functools import wraps
from login import login_required
import httplib2
import random
import string
import os
import datetime
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Royal_Chocolates"

engine = create_engine('sqlite:///chocolatemenu.db',
                       connect_args={'check_same_thread': False}, echo=True)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# creating login session
@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# creating connection with google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        ''' Upgrade the authorization code into a credentials object'''
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('''Failed to upgrade the
                                            authorization code.'''), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        ''' Check that the access token is valid.'''
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    ''' If there was an error in the access token info, abort.'''
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Verify that the access token is used for the intended user.'''
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("""Token's user ID doesn't
                                            match given user ID."""), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Verify that the access token is valid for this app.'''
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("""Token's client ID does
                                            not match app's."""), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user is
                                            already connected.'''), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    ''' Get user info'''
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # see if user exit,if not create new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '''<" style = "width: 300px;
                    height: 300px;
                    border-radius: 150px;
                    -webkit-border-radius: 150px;
                    -moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# creating new user
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# getting user info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# getting user ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# disconnect from connected user
@app.route("/GLogout")
def GDisconnect():
        access_token = login_session.get('access_token')
        if access_token is None:
            response = make_response(json.dumps('''Current user
                                                not connected.'''), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
               % access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] == '200':
            # Reset the user's sesson.
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            response = make_response(json.dumps('''Successfully
                                                logged out!.'''), 200)
            response.headers['Content-Type'] = 'application/json'
            flash('Successfully Logged Out!')
            return redirect(url_for('allChocolate'))
        else:
            # For whatever reason, the given token was invalid.
            response = make_response(json.dumps('''Failed to revoke token
                                                for given user.'''), 400)
            response.headers['Content-Type'] = 'application/json'
            return response


@app.route('/chocolates/<int:chocolate_id>/menu/JSON')
def chocolateMenuJSON(chocolate_id):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).one()
    ch = session.query(ChocoTypes).filter_by(chocolate_id=chocolate.id).all()
    chocolates = ch
    return jsonify(ChocoTypes=[i.serialize for i in chocolates])


@app.route('/chocolates/<int:chocolate_id>/menu/<int:menu_id>/JSON')
def MenuchocolateJSON(chocolate_id, menu_id):
    chocoTypes = session.query(ChocoTypes).filter_by(id=menu_id).one()
    return jsonify(ChocoTypes=chocoTypes.serialize)


@app.route('/')
@app.route('/chocolates')
def allChocolate():
    chocolate = session.query(Chocolate)
    if 'username' not in login_session:
        return render_template('showChocolate.html', chocolate=chocolate)
    else:
        return render_template('allChocolate.html', chocolate=chocolate)


@app.route('/chocolates/new', methods=['GET', 'POST'])
@login_required
def newChocolate():
    chocolate = session.query(Chocolate)
    if request.method == 'POST':
        newchocolate = Chocolate(name=request.form['name'],
                                 user_id=login_session['user_id'],
                                 picture=request.form['picture'])
        user_id = login_session['user_id']
        session.add(newchocolate)
        session.commit()
        flash("A new Chocolate brand is created!")
        return redirect(url_for('allChocolate'))
    else:
        return render_template('newChocolate.html', chocolate=chocolate)


@app.route('/chocolates/<int:chocolate_id>/edit', methods=['GET', 'POST'])
@login_required
def editChocolate(chocolate_id):
    editedchocolate = session.query(Chocolate).filter_by(id=chocolate_id).one()
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).one()
    vidya = getUserInfo(editedchocolate.user_id)
    if 'username' not in login_session:
        flash("premission denied as it belongs to %s" % vidya.name)
        return redirect(url_for('allChocolate'))
    else:
        if request.method == 'POST':
            if request.form['name']:
                editedchocolate.name = request.form['name']
            session.add(editedchocolate)
            session.commit()
            flash("A new Chocolate brand is edited!")
            return redirect(url_for('allChocolate'))
        elif vidya.id != login_session['user_id']:
            flash('premission denied as it belongs to %s' % vidya.name)
            return redirect(url_for('allChocolate'))
        else:
            return render_template('editChocolate.html',
                                   chocolate_id=chocolate_id,
                                   chocolate=editedchocolate)


@app.route('/chocolates/<int:chocolate_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteChocolate(chocolate_id):
    chocoToDelete = session.query(Chocolate).filter_by(id=chocolate_id).one()
    vidya = getUserInfo(chocoToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    if 'username' not in login_session:
        flash("premission denied as it belongs to %s" % vidya.name)
        return redirect(url_for('allChocolate'))
    else:
        if request.method == 'POST':
            session.delete(chocoToDelete)
            session.commit()
            flash("A Chocolate brand is deleted!")
            return redirect(url_for('allChocolate'))
        elif vidya.id != login_session['user_id']:
            flash('premission denied as it belongs to %s' % vidya.name)
            return redirect(url_for('allChocolate'))
        else:
            return render_template('deleteChocolate.html',
                                   chocolate=chocoToDelete)


@app.route('/chocolate/<int:chocolate_id>/')
def chocolatemenu(chocolate_id):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).one()
    chocolates = session.query(ChocoTypes).filter_by(chocolate_id=chocolate.id)
    return render_template('showmenu.html',
                           chocolate=chocolate, chocolates=chocolates)


@app.route('/chocolates/<int:chocolate_id>/')
def chocolateMenu(chocolate_id):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).one()
    chocolates = session.query(ChocoTypes).filter_by(chocolate_id=chocolate.id)
    return render_template('menu.html',
                           chocolate=chocolate, chocolates=chocolates)


@app.route('/chocolates/<int:chocolate_id>/new', methods=['GET', 'POST'])
@login_required
def newChocoTypes(chocolate_id):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).one()
    vidya = getUserInfo(chocolate.user_id)
    user = getUserInfo(login_session['user_id'])
    if 'username' not in login_session:
        flash("premission denied as it belongs to %s" % vidya.name)
        return redirect(url_for('chocolatemenu', chocolate_id=chocolate_id))
    else:
        if request.method == 'POST':
            newChocolate = ChocoTypes(name=request.form['name'],
                                      description=request.form['description'],
                                      price=request.form['price'],
                                      picture=request.form['picture'],
                                      chocolate_id=chocolate_id,
                                      user_id=login_session['user_id'])
            user_id = login_session['user_id']
            session.add(newChocolate)
            session.commit()
            flash("A new menu chocolate is created!")
            return redirect(url_for('chocolateMenu',
                                    chocolate_id=chocolate_id))
        elif vidya.id != login_session['user_id']:
            flash('premission denied as it belongs to %s' % vidya.name)
            return redirect(url_for('chocolateMenu',
                                    chocolate_id=chocolate_id))
        else:
            return render_template('newmenuchocolate.html',
                                   chocolate_id=chocolate_id)


@app.route('/chocolates/<int:chocolate_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editChocoTypes(chocolate_id, menu_id):
    editedChocolate = session.query(ChocoTypes).filter_by(id=menu_id).one()
    vidya = getUserInfo(editedChocolate.user_id)
    user = getUserInfo(login_session['user_id'])
    if 'username' not in login_session:
        flash("premission denied as it belongs to %s" % vidya.name)
        return redirect(url_for('chocolatemenu',
                                chocolate_id=chocolate_id))
    else:
        if request.method == 'POST':
            if request.form['name']:
                editedChocolate.name = request.form['name']
                if request.form['description']:
                    editedChocolate.description = request.form['description']
                if request.form['price']:
                    editedChocolate.price = request.form['price']
                session.add(editedChocolate)
                session.commit()
                flash("A menu chocolate is edited!")
                return redirect(url_for('chocolateMenu',
                                        chocolate_id=chocolate_id))
        elif vidya.id != login_session['user_id']:
            flash('premission denied as it belongs to %s' % vidya.name)
            return redirect(url_for('chocolateMenu',
                                    chocolate_id=chocolate_id))
        else:
            return render_template('editmenuchocolate.html',
                                   chocolate_id=chocolate_id,
                                   menu_id=menu_id, chocolate=editedChocolate)


@app.route('/chocolates/<int:chocolate_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteChocoTypes(chocolate_id, menu_id):
    chocolateToDelete = session.query(ChocoTypes).filter_by(id=menu_id).one()
    vidya = getUserInfo(chocolateToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    if 'username' not in login_session:
        flash("premission denied as it belongs to %s" % vidya.name)
        return redirect(url_for('chocolatemenu', chocolate_id=chocolate_id))
    else:
        if request.method == 'POST':
            session.delete(chocolateToDelete)
            session.commit()
            flash("A menu chocolate is deleted!")
            return redirect(url_for('chocolateMenu',
                                    chocolate_id=chocolate_id))
        elif vidya.id != login_session['user_id']:
            flash('premission denied as it belongs to %s' % vidya.name)
            return redirect(url_for('chocolateMenu',
                                    chocolate_id=chocolate_id))
        else:
            return render_template('deletemenuchocolate.html',
                                   chocolate=chocolateToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5005)
