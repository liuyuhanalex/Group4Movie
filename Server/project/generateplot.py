import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import mysql.connector
#Plot for total number of titles by genres
genres =['Drama','Comedy','Short','Documentary','Talk-Show','Romance',
    'Family','News','Animation','Reality-TV']
count =[1182740,1049316,670576,498955,452555,398556,339632,338763,255158,
    232580]
plt.clf()
fig = plt.figure()
list = plt.bar(genres,count)
fig.autofmt_xdate()
plt.savefig('static/image/bar2.png')
