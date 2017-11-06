import os
import sys
 
path='/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/tb'

sys.path.append('/home/ashmit/Legion/myproject/newproject/spark/python')
sys.path.append('/home/ashmit/Legion/myproject/newproject/spark')
sys.path.append('/usr/local/hadoop-2.5.1-src/hadoop-dist/target/hadoop-2.5.1')
sys.path.append('/usr/lib/jvm/java-7-openjdk-amd64')
 
if path not in sys.path:
	sys.path.append(path)
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'tb.settings'
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()