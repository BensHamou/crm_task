from .models import Setting
from xmlrpc import client


def connect_odoo():

    url = Setting.objects.get(name='url_odoo').value
    db = Setting.objects.get(name='db_odoo').value
    username = Setting.objects.get(name='username_odoo').value
    password = Setting.objects.get(name='password_odoo').value

    common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return db, uid, models, password