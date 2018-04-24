import os
from django.db import connection
from imdbpie import Imdb

# os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
#
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM titles WHERE primary_title like '%hamlet%'")
# rawdata = cursor.fetchall()
# for each in rawdata:
#     print(each)
# Create your tests here
imdb = Imdb()
info = imdb.get_name_videos('nm0000032')['videos'][0]['encodings'][0]['play']
print(info)
