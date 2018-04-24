import pandas as pd
import sqlalchemy
import csv
import numpy as np
import MySQLdb
from pandas.io import sql

#import all the data into pandas dataframe
def read_crew():
    crew_rawdata = pd.read_csv(r'C:\Users\liuyu\Desktop\data\crewdata.csv',sep='\t',low_memory=False)
    crewdf = pd.DataFrame(crew_rawdata,columns =['tconst', 'directors', 'writers'])
    return crewdf

def read_title():
    title_rawdata = pd.read_csv(r'C:\Users\liuyu\Desktop\data\titledata.csv',sep='\t',low_memory=False)
    titledf = pd.DataFrame(title_rawdata,columns=['tconst','titleType','primaryTitle','originalTitle',
                                                  'isAdult','startYear','endYear','runtimeMinutes',
                                                  'genres'])
    return titledf

def read_rating():
    rating_rawdata = pd.read_csv(r'C:\Users\liuyu\Desktop\data\ratingdata.csv',sep='\t',low_memory=False)
    ratingdf = pd.DataFrame(rating_rawdata,columns=['tconst','averageRating','numVotes'])
    return ratingdf

def read_episode():
    episode_rawdata = pd.read_csv(r'C:\Users\liuyu\Desktop\data\episodedata.csv',sep='\t',low_memory=False)
    episodedf = pd.DataFrame(episode_rawdata,columns=['tconst','parentTconst',
                                                  'seasonNumber','episodeNumber'])
    return episodedf

def read_person():
    person_rawdata = pd.read_csv(r'C:\Users\liuyu\Desktop\data\persondata.csv',sep='\t',low_memory=False)
    persondf = pd.DataFrame(person_rawdata,columns=['nconst','primaryName','birthYear',
                                                  'deathYear','primaryProfession','knownForTitles'])
    return persondf

def read_principle():
    principle_rawdata = pd.read_csv(r'C:\Users\liuyu\Desktop\data\principledata.csv',sep='\t',low_memory=False)
    principledf = pd.DataFrame(principle_rawdata,columns=['tconst','ordering','nconst',
                                                      'category','job','characters'])
    return principledf

#connect with MySQL
def connect_with_mysql(database_username,database_password,database_ip,database_name):
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(database_username, database_password,
                                                database_ip, database_name))
    print('Finish connect with MySQL!')
    return database_connection

#First dataframe title_types
def create_title_types():
    titledf = read_title()
    titlecolumn = titledf[['titleType']]
    titletype1 = titlecolumn.drop_duplicates().reset_index(drop=True).reset_index()
    titletype = titletype1.rename(columns={'index':'id','titleType':'name'})
    return titletype

#Second dataframe titles
def create_titles():
    titletype = create_title_types()
    #replace all '\N' with 0 since endyear is int
    titledf = read_title().replace(r'\N','0')
    jointitle = titledf.set_index('titleType').join(titletype.set_index('name')).\
        reset_index(drop=True).reset_index(drop=False)
    titletable1 = jointitle[['index','tconst','primaryTitle','originalTitle','isAdult',
                            'startYear','endYear','runtimeMinutes','id']]
    titletable = titletable1.rename(columns={'index':'id','tconst':'imdb_id','primaryTitle':'primary_title',
                                    'originalTitle':'original_title','isAdult':'is_adult','startYear':'start_year',
                                    'endYear':'end_year','runtimeMinutes':'runtime','id':'type_id'})
    #titletable.to_csv(r'C:\Users\liuyu\Desktop\titletable.csv',index=False,sep='\t')
    return titletable

#Third dataframe genres
def create_genres():
    title = read_title()
    genresraw = title[['genres']].drop_duplicates()
    temp = genresraw['genres'].str.split(',').apply(pd.Series,1).stack()
    temp.index = temp.index.droplevel(-1)
    genres1 = pd.DataFrame({'genres':temp}).drop_duplicates().reset_index(drop=True).reset_index()
    genres = genres1.rename(columns={'index':'id','genres':'name'})
    return genres

#4th dataframe has_genres
def create_has_genres_old():
    #take up too much memory
    titletable = pd.read_csv(r'C:\Users\liuyu\Desktop\data\titletable.csv',sep='\t',low_memory=False)
    titledf = pd.DataFrame(titletable,columns=['id','imdb_id','primary_title','original_title',
                                               'is_adult','start_year','end_year','runtime','type_id','genres'])
    #genres = create_genres()
    titletemp = titledf[['id','genres']]
    print('test')
    temp = titletemp['genres'].str.split(',').apply(pd.Series,1).stack()
    temp.index = temp.index.droplevel(-1)
    return temp

def create_has_genres_createfile():
    file = open(r'C:\Users\liuyu\Desktop\data\titletable.csv',encoding="utf8")
    file.readline()#for header
    writefile = open(r'C:\Users\liuyu\Desktop\data\has_genres.csv','w+')
    csv_reader = csv.reader(file, delimiter='\t')
    writefile.write('id'+'\t'+'genres'+'\n')
    for line in csv_reader:
        genres_list = [x.strip() for x in line[9].split(',')]
        for genres in genres_list:
            writefile.write(line[0]+'\t'+genres+'\n')

def create_has_genres():
    title_genres = pd.read_csv(r'C:\Users\liuyu\Desktop\data\has_genres.csv',sep='\t')
    title_genresdf = pd.DataFrame(title_genres,columns=['id','genres'])
    genresdf = create_genres()
    temp = title_genresdf.set_index('genres').join(genresdf.set_index('name'),\
                                                         lsuffix='title_id', rsuffix='genre_id').reset_index(drop=True)
    has_genres = temp.rename(columns={'idtitle_id':'title_id','idgenre_id':'genre_id'})
    has_genres.genre_id.astype(int)
    return has_genres

#5th dataframe episodes
def create_idimdb_file():
    file = open(r'C:\Users\liuyu\Desktop\data\titletable.csv',encoding="utf8")
    idimdb = open(r'C:\Users\liuyu\Desktop\data\idimdb.csv','w+')
    csv_reader = csv.reader(file,delimiter = '\t')
    for line in csv_reader:
        idimdb.write(line[0]+'\t'+line[1]+'\n')
    print('Finish create idimdb file!')

def create_episodes():
    episode_raw = read_episode()
    idimdb = pd.read_csv(r'C:\Users\liuyu\Desktop\data\idimdb.csv',sep='\t')
    idimdbdf = pd.DataFrame(idimdb,columns=['id','imdb_id'])
    jointemp = episode_raw.set_index('tconst').join(idimdbdf.set_index('imdb_id')).reset_index(drop=True)
    temp2 = jointemp.rename(columns={'id':'title_id'})
    jointemp2 = temp2.set_index('parentTconst').join(idimdbdf.set_index('imdb_id')).reset_index(drop=True)
    episodestemp = jointemp2.rename(columns = {'id':'parent_title_id','seasonNumber':'season','episodeNumber':'episode'})
    episodes = episodestemp.replace(r'\N','0') #replace all the '\N' with 0
    return episodes

#6th dataframe people
def create_people():
    peopleraw = read_person()
    peopleselect = peopleraw[['nconst','primaryName','birthYear','deathYear']].reset_index(drop=True).reset_index()
    people = peopleselect.replace(r'\N','0').rename(columns={'index':'id','nconst':'imdb_id',
                                                             'primaryName':'name','birthYear':'birth_year',
                                                             'deathYear':'death_year'})
    return people

#7th dataframe known_for
def create_peoplefile_withid():
    #create a csv file contain the id with all other information from persondata
    peopleraw = read_person()
    peopleselect = peopleraw[['nconst','primaryName','birthYear','deathYear',
                              'primaryProfession','knownForTitles']].reset_index(drop=True).reset_index()
    people = peopleselect.replace(r'\N','NULL').rename(columns={'index':'id','nconst':'imdb_id',
                                                             'primaryName':'name','birthYear':'birth_year',
                                                             'deathYear':'death_year','primaryProfession':'profession',
                                                             'knownForTitles':'titles'})
    people.to_csv(r'C:\Users\liuyu\Desktop\data\peoplewithid.csv',index=False,sep='\t')
    print('Finish create people information csv file!')
    return people

def create_known_for_splitfile():
    #create a csv file with id and split the knowfor cell to multiple rows
    peoplewithid = open(r'C:\Users\liuyu\Desktop\data\peoplewithid.csv',encoding='utf8')
    peopleknownfor_split = open(r'C:\Users\liuyu\Desktop\data\knowforsplit.csv','w+')
    csv_reader = csv.reader(peoplewithid,delimiter='\t')
    for line in csv_reader:
        knowfor_list = [x.strip() for x in line[6].split(',')]
        for each in knowfor_list:
            peopleknownfor_split.write(line[0]+'\t'+each+'\n')
    print('Finish create knownforsplit file!')
    return

def create_known_for():
    idimdb = pd.read_csv(r'C:\Users\liuyu\Desktop\data\idimdb.csv',sep='\t',low_memory=False)
    idimdbdf = pd.DataFrame(idimdb,columns=['id','imdb_id'])
    peopleknownfor = pd.read_csv(r'C:\Users\liuyu\Desktop\data\knowforsplit.csv',sep='\t',low_memory=False)
    peopleknownfordf = pd.DataFrame(peopleknownfor,columns=['id','titles'])
    jointemp = peopleknownfor.set_index('titles').join(idimdbdf.set_index('imdb_id'),how='inner',lsuffix='_people',
                                                       rsuffix='_title').reset_index(drop=True)
    known_for = jointemp.rename(columns={'id_people':'people_id','id_title':'title_id'})
    return known_for

#8th dataframe writes
def create_writes_splitfile():
    crewdata = open(r'C:\Users\liuyu\Desktop\data\crewdata.csv',encoding='utf8')
    writers_split = open(r'C:\Users\liuyu\Desktop\data\writerssplit.csv','w+')
    csv_reader = csv.reader(crewdata,delimiter='\t')
    for line in csv_reader:
        writers_list = [x.strip() for x in line[2].split(',')]
        for each in writers_list:
            writers_split.write(line[0]+'\t'+each+'\n')
    print('Finish create writes split file!')
    return

def create_writes():
    writersraw = pd.read_csv(r'C:\Users\liuyu\Desktop\data\writerssplit.csv',sep='\t',low_memory=False)
    writers = writersraw[['tconst','writers']]
    peopleraw = pd.read_csv(r'C:\Users\liuyu\Desktop\data\peoplewithid.csv',sep='\t',low_memory=False)
    people = peopleraw[['id','imdb_id']]
    idimdbraw = pd.read_csv(r'C:\Users\liuyu\Desktop\data\idimdb.csv',sep='\t',low_memory=False)
    jointemp = writers.set_index('writers').join(people.set_index('imdb_id'),how='inner').reset_index(drop=True).\
        rename(columns = {'id':'people_id'})
    writes = jointemp.set_index('tconst').join(idimdbraw.set_index('imdb_id'),how='inner').reset_index(drop=True).\
        rename(columns = {'id':'title_id'})
    return writes

#9th dataframe directs
def create_directs_splitfile():
    crewdata = open(r'C:\Users\liuyu\Desktop\data\crewdata.csv',encoding='utf8')
    directs_split = open(r'C:\Users\liuyu\Desktop\data\directssplit.csv','w+')
    csv_reader = csv.reader(crewdata,delimiter='\t')
    for line in csv_reader:
        writers_list = [x.strip() for x in line[1].split(',')]
        for each in writers_list:
            directs_split.write(line[0]+'\t'+each+'\n')
    print('Finish create directs split file!')
    return

def create_directs():
    directsraw = pd.read_csv(r'C:\Users\liuyu\Desktop\data\directssplit.csv',sep='\t',low_memory=False)
    writers = directsraw[['tconst','directors']]
    peopleraw = pd.read_csv(r'C:\Users\liuyu\Desktop\data\peoplewithid.csv',sep='\t',low_memory=False)
    people = peopleraw[['id','imdb_id']]
    idimdbraw = pd.read_csv(r'C:\Users\liuyu\Desktop\data\idimdb.csv',sep='\t',low_memory=False)
    jointemp = writers.set_index('directors').join(people.set_index('imdb_id'),how='inner').reset_index(drop=True).\
        rename(columns = {'id':'people_id'})
    directs = jointemp.set_index('tconst').join(idimdbraw.set_index('imdb_id'),how='inner').reset_index(drop=True).\
        rename(columns = {'id':'title_id'})
    return directs

#10th dataframe professions
def create_professions_files():
    peopleraw = read_person()
    people = peopleraw[['primaryProfession']]
    people.to_csv(r'C:\Users\liuyu\Desktop\data\protemp.csv',sep='\t')
    peoplefile =open(r'C:\Users\liuyu\Desktop\data\protemp.csv',encoding='utf8')
    protemp2 = open(r'C:\Users\liuyu\Desktop\data\protemp2.csv','w+')
    csv_reader = csv.reader(peoplefile,delimiter='\t')
    for line in csv_reader:
        prolist = [x.strip() for x in line[1].split(',')]
        for each in prolist:
            protemp2.write(line[0]+'\t'+each+'\n')
    return

def create_professions():
    allpro = pd.read_csv(r'C:\Users\liuyu\Desktop\data\protemp2.csv',sep='\t',low_memory=False)
    professions = allpro[['primaryProfession']].drop_duplicates().reset_index(drop=True).reset_index().\
        rename(columns={'index':'id','primaryProfession':'name'})
    return professions

#11th dataframe has_professions
def create_has_professions():
    allpro = pd.read_csv(r'C:\Users\liuyu\Desktop\data\protemp2.csv',sep='\t',low_memory=False)
    pro = allpro.rename(columns={'Unnamed: 0':'id'})
    professions = create_professions()
    join = pro.set_index('primaryProfession').join(professions.set_index('name'),lsuffix='_people',rsuffix='_profession').\
        reset_index(drop=True)
    has_professions = join.rename(columns={'id_people':'people_id','id_profession':'profession_id'})
    return has_professions

if __name__ == '__main__':
    #username,password,ip,databasename
    conn = connect_with_mysql('root','lyh680226','localhost','testdb')
######################################################################################################
    #create table title_types
    sql.execute('CREATE TABLE IF NOT EXISTS title_types\
    (id INT,name VARCHAR(255),PRIMARY KEY(id));',conn)
    title_type=create_title_types()
    title_type.to_sql(name='title_types',con=conn,if_exists='append',chunksize=100,index=False)
    print('1.title_types is finished!')
######################################################################################################
    #create table titles
    sql.execute('CREATE TABLE IF NOT EXISTS titles(\
    id INT,\
    imdb_id VARCHAR(32),\
    primary_title VARCHAR(512),\
    original_title VARCHAR(512),\
    is_adult INT,\
    start_year INT,\
    end_year INT,\
    runtime VARCHAR(32),\
    type_id INT,\
    PRIMARY KEY (id),\
    FOREIGN KEY (type_id) REFERENCES title_types(id));',con=conn)

    titles = create_titles()
    titledataframes = np.array_split(titles,10)
    for each in titledataframes:
        each.to_sql(name='titles',con=conn,if_exists='append',chunksize=10000,index=False)
    print('2.titles is finished!')
#######################################################################################################
    #create table genres
    sql.execute('CREATE TABLE IF NOT EXISTS genres (\
    id INT,\
    name VARCHAR(64),\
    PRIMARY KEY (id));',con=conn)

    genres = create_genres()
    genres.to_sql(name='genres',con=conn,if_exists='append',chunksize=100,index=False)
    print('3.genres is finished!')
#######################################################################################################
    #create table has_genre
    #extremely long time to import them into MySQL
    sql.execute('CREATE TABLE IF NOT EXISTS has_genre(\
    title_id INT,\
    genre_id INT,\
    PRIMARY KEY (title_id, genre_id),\
    FOREIGN KEY (title_id) REFERENCES titles(id),\
    FOREIGN KEY (genre_id) REFERENCES genres(id));',con=conn)
    has_genres = create_has_genres()
    list = np.array_split(has_genres,10)
    n=10
    for each in list:
        each.to_sql(name='has_genre',con=conn,if_exists='append',chunksize=10000,index=False)
        print('{}% of has_genre already finished!'.format(n))
        n=n+10
    print('4.has_genre is finished!')
########################################################################################################
    #create table episodes
    sql.execute('CREATE TABLE IF NOT EXISTS episodes (\
    title_id INT,\
    parent_title_id INT,\
    season INT,\
    episode INT,\
    PRIMARY KEY (title_id),\
    FOREIGN KEY (title_id) REFERENCES titles(id),\
    FOREIGN KEY (parent_title_id) REFERENCES titles(id));',con=conn)
    episodes = create_episodes()
    episodes.to_sql(name='episodes',con=conn,if_exists='append',chunksize=10000,index=False)
    print('5.episodes is finished!')
########################################################################################################
    #create table people
    sql.execute('CREATE TABLE IF NOT EXISTS people (\
    id INT,\
    imdb_id VARCHAR(32),\
    name VARCHAR(255),\
    birth_year INT,\
    death_year INT,\
    PRIMARY KEY (id));',con=conn)
    people = create_people()
    people.to_sql(name='people',con=conn,if_exists='append',chunksize=10000,index=False)
    print('6.people is finished!')
########################################################################################################
    #create table known_for
    #extremely long time to import them into MySQL
    sql.execute('CREATE TABLE IF NOT EXISTS known_for (\
    people_id INT,\
    title_id INT,\
    PRIMARY KEY (people_id, title_id),\
    FOREIGN KEY (people_id) REFERENCES people(id),\
    FOREIGN KEY (title_id) REFERENCES titles(id));',con=conn)
    known_for = create_known_for()
    known_for_list = np.array_split(known_for,100)
    m=1
    for each in known_for_list:
        each.to_sql(name='known_for',con=conn,if_exists='append',chunksize=10000,index=False)
        print('{}% of known_for is finished!'.format(m))
        m=m+1
    print('7.known_for is finished!')
#########################################################################################################
    #create table writes
    sql.execute('CREATE TABLE IF NOT EXISTS writes (\
    people_id INT,\
    title_id INT,\
    PRIMARY KEY (people_id, title_id),\
    FOREIGN KEY (people_id) REFERENCES people(id),\
    FOREIGN KEY (title_id) REFERENCES titles(id));',con=conn)
    writes = create_writes()
    chunk = np.array_split(writes,10)
    p=10
    for each in chunk:
        each.to_sql(name='writes',con=conn,if_exists='append',chunksize = 10000,index = False)
        print('{}% of the writes is finished!'.format(p))
        p= p+10
    print('8.writes is finished!')
##########################################################################################################
    #create table directs
    sql.execute('CREATE TABLE IF NOT EXISTS directs (\
    people_id INT,\
    title_id INT,\
    PRIMARY KEY (people_id, title_id),\
    FOREIGN KEY (people_id) REFERENCES people(id),\
    FOREIGN KEY (title_id) REFERENCES titles(id));',con=conn)
    directs = create_directs()
    directs.to_sql(name='directs',con=conn,if_exists='append',chunksize=10000,index=False)
    print('9.directs is finished!')
##########################################################################################################
    #create table professions
    sql.execute('CREATE TABLE IF NOT EXISTS professions (\
    id INT,\
    name VARCHAR(255),\
    PRIMARY KEY (id));',con=conn)
    professions=create_professions()
    professions.to_sql(name='profession',con=conn,if_exists='append',chunksize=10000,index=False)
    print('10.professions is finished!')
##########################################################################################################
    #create table has_professions
    sql.execute('CREATE TABLE IF NOT EXISTS has_profession (\
    people_id INT,\
    profession_id INT,\
    PRIMARY KEY (people_id, profession_id),\
    FOREIGN KEY (people_id) REFERENCES people(id),\
    FOREIGN KEY (profession_id) REFERENCES professions(id));',con=conn)
    has_professions = create_has_professions()
    has_professions.to_sql(name='has_profession',con=conn,if_exists='append',chunksize=10000,index=False)
    print('11.has_profession is finished!')
