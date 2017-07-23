var session_info = function() {
    var sessionHTTP = new XMLHttpRequest();
    sessionHTTP.open('GET', './context', false);
    sessionHTTP.send(null);
    return JSON.parse(sessionHTTP.responseText);
}();

if (session_info['user'] == true) {
    console.log('You have the user role');
    var newscript = document.createElement('script');
    newscript.src = '/user-static/user.js';
    document.getElementsByTagName('body')[0].appendChild(newscript);
}
if (session_info['admin'] == true) {
    console.log('You have the admin role');
    var newscript = document.createElement('script');
    newscript.src = '/admin-static/admin.js';
    document.getElementsByTagName('body')[0].appendChild(newscript);
}
