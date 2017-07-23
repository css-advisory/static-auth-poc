from flask import Flask, request, render_template, session, url_for, Response, jsonify, redirect, abort, make_response
from random import randint
import requests
import os


""" Flask Setup """
app = Flask(__name__)
app.secret_key = os.urandom(36)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():

    """ If GET request, return login page """
    if request.method == 'GET':
        return render_template('login.html')
    else:

        """ Create Success Response Object  """
        success_response = make_response(redirect(url_for('index')))
        
        """ Validate User """
        if 'uname' not in request.form or 'pass' not in request.form:
            return render_template('login.html')

        """ Check for valid user credentials """
        if request.form['uname'] == 'user' and request.form['pass'] == 'user':
            print('Logged in as User')
            session['user_role'] = True

            """ Cache user static file cookie in session for integrity (and laziness) """
            session['user-static'] = str(randint(100000, 999999))

            """ Set cookie that will authorize for user static files """
            success_response.set_cookie('userstatic', session['user-static'])

            """ Touch file with cookie value for NginX to check """
            open("/var/www/userstatic/{}".format(session['user-static']), 'a').close()
            print('Created cookiefile at /var/www/userstatic/{}!'.format(session['user-static']))
            
            return success_response

        """ Check for valid admin credentials """
        if request.form['uname'] == 'admin' and request.form['pass'] == 'admin':
            print('Loggd in as Admin') 
            session['user_role'] = True
            session['admin_role'] = True
            
            """ Cache admin static file cookie in session for integrity (and laziness) """
            session['admin-static'] = str(randint(100000, 999999))
            session['user-static'] = str(randint(100000, 999999))

            """ Set cookie that will authorize for admin static files """
            success_response.set_cookie('adminstatic', session['admin-static'])
            success_response.set_cookie('userstatic', session['user-static'])

            """ Touch file with cookie value for NginX to check """
            open("/var/www/adminstatic/{}".format(session['admin-static']), 'a').close()
            open("/var/www/userstatic/{}".format(session['user-static']), 'a').close()
            print('Created cookiefile at /var/www/userstatic/{}!'.format(session['user-static']))
            print('Created cookiefile at /var/www/adminstatic/{}!'.format(session['admin-static']))
            
            return success_response

        
        """ For invalid creds, just return to login """
        return render_template('login.html')


@app.route('/logout')
def logout():

    resp = make_response(redirect(url_for('index')))

    """ Logout and return to index """
    if 'user_role' in session:
        os.remove('/var/www/userstatic/{}'.format(session['user-static']))
        print('Removed cookiefile at /var/www/userstatic/{}'.format(session['user-static']))
        resp.set_cookie('userstatic', '', expires=0)
        session.pop('user_role')
        session.pop('user-static')

    if 'admin_role' in session:
        os.remove('/var/www/adminstatic/{}'.format(session['admin-static']))
        print('Removed cookiefile at /var/www/adminstatic/{}'.format(session['admin-static']))
        resp.set_cookie('adminstatic', '', expires=0)
        session.pop('admin_role')
        session.pop('admin-static')
    
    print('Logged out')
    return redirect(url_for('index'))


@app.route('/context')
def context():

    """ Return information about the current session """
    data = {'user':False, 'admin':False}
    if 'user_role' in session and session['user_role'] == True:
        data['user'] = True
    if 'admin_role' in session and session['admin_role'] == True:
        data['admin'] = True
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
