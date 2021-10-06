import logging
from ldap3.utils.log import set_library_log_detail_level, PROTOCOL
logging.basicConfig(filename='log/client_application.log', level=logging.DEBUG)
set_library_log_detail_level(PROTOCOL)
from ldap3 import Server, Connection, SUBTREE, ALL
from ldap3.core.exceptions import LDAPBindError

AD_SERVER = 'kmf.local'
AD_SEARCH_TREE = 'dc=kmf,dc=local'


def connect_to_ad(user, pwd):
    user = 'kmf\\' + str(user)
    pwd = str(pwd)
    server = Server(AD_SERVER, get_info=ALL, use_ssl=True)
    try:
        conn = Connection(server, user=user, password=pwd, auto_bind=True)
        return conn
    except LDAPBindError:
        return


def user_search_ad(user, connection):
    USER_DN = ''
    SEARCHFILTER = '(&(|(sAMAccountname=' + str(user) + '))(objectClass=person))'
    if connection.search(search_base=AD_SEARCH_TREE, search_filter=SEARCHFILTER, search_scope=SUBTREE, attributes=['cn', 'givenName'], paged_size=5):
        for entry in connection.response:
            if entry.get("dn") and entry.get("attributes"):
                if entry.get("attributes").get("cn"):
                    USER_DN = entry.get("dn")
    return USER_DN


def reset_pass(user, connection):
    return connection.extend.microsoft.modify_password(user, '123qweASD')
