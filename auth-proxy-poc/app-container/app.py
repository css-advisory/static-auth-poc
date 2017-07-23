from flask import Flask, request, render_template, session, url_for, Response, jsonify, redirect, abort
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
        
        """ Validate User """
        if 'uname' not in request.form or 'pass' not in request.form:
            return render_template('login.html')

        """ Check for valid user credentials """
        if request.form['uname'] == 'user' and request.form['pass'] == 'user':
            session['user_role'] = True
            print('Logged in as User')
            return redirect(url_for('index'))

        """ Check for valid admin credentials """
        if request.form['uname'] == 'admin' and request.form['pass'] == 'admin':
            session['user_role'] = True
            session['admin_role'] = True
            print('Logged in as admin')
            return redirect(url_for('index'))

        """ For invalid creds, just return to login """
        return render_template('login.html')


@app.route('/context')
def context():

    """ Return information about the current session """
    data = {'user':False, 'admin':False}
    if 'user_role' in session and session['user_role'] == True:
        data['user'] = True
    if 'admin_role' in session and session['admin_role'] == True:
        data['admin'] = True
    return jsonify(data)


@app.route('/logout')
def logout():

    """ Logout and return to index """
    if 'user_role' in session:
        session.pop('user_role')
    if 'admin_role' in session:
        session.pop('admin_role')
    print('Logged out')
    return redirect(url_for('index'))


@app.route('/global-static/<path>')
def global_static(path):
    
    """ Create URL for internal global static server """
    """ Don't forget to actually sanitize your inputs in real life """
    static_file_url = "http://statics/global-statics/{}".format(path)

    """ Create stream for proxied file and return it to the client """
    proxy = requests.get(static_file_url, stream=True)
    print('Proxying Global Static')
    headers = dict(proxy.headers)
    def generate():
        for chunk in proxy.iter_content(1024):
            yield chunk
    return Response(generate(), headers=headers)


@app.route('/user-static/<path>')
def user_static(path):

    """ Check for user role """
    if 'user_role' not in session:
        abort(403)

    """ Create URL for internal user-only static server """
    """ Don't forget to actually sanitize your inputs in real life """
    static_file_url = "http://statics/user-statics/{}".format(path)

    """ Create stream for proxied file and return it to the client """
    proxy = requests.get(static_file_url, stream=True)
    print('Proxying User-Only Static')
    headers = dict(proxy.headers)
    def generate():
        for chunk in proxy.iter_content(1024):
            yield chunk
    return Response(generate(), headers=headers)


@app.route('/admin-static/<path>')
def admin_static(path):

    """ Check for admin role """
    if 'admin_role' not in session:
        abort(403)

    """ Create URL for internal admin-only static server """
    """ Don't forget to actually sanitize your inputs and use TLS in real life """
    static_file_url = "http://statics/admin-statics/{}".format(path)

    """ Create stream for proxied file and return it to the client """
    proxy = requests.get(static_file_url, stream=True)
    print('Proxying Admin-Only Static')
    headers = dict(proxy.headers)
    def generate():
        for chunk in proxy.iter_content(1024):
            yield chunk
    return Response(generate(), headers=headers)


@app.errorhandler(403)
def unauthorized(error):
    return Response('Not Authorized', 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
