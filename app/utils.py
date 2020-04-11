from flask import url_for, current_app as app
import urllib.parse

def inProduction():
    """ returns a bool determining if the app is in production mode"""
    return app.config['FLASK_ENV'] == "production"

def url_for_secure(endpoint, **values):
    """ same as flask.url_for but sets up _external and _scheme for us"""
    if not inProduction():
        return url_for(endpoint, **values)
    values['_external'] = True
    values['_scheme'] = "https"
    url = url_for(endpoint, **values)
    if not inProduction():
        return url
    parsed = urllib.parse.urlparse(url_for('main.home',_external=True, _scheme='https'))
    replaced = parsed._replace(netloc=app.config['DOMAIN'])
    return replaced.geturl()