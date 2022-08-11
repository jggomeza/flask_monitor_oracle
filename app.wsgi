import sys
arg = sys.argv
host = '10.156.80.210'
port = 5020
bug = True

sys.path.insert(0, "/var/www/html/webservice_flask_monitor")
from app import app as application
