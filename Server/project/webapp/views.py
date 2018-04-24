from django.shortcuts import render
from webapp.models import (
    Users,
    Titles,
    People,
    Genres,
    Rates,
    Writes,
    Directs,
    Stats,
    TopTitles,
    Professions
)
from webapp.forms import Register,Search,Login,Rating
from . import forms
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from imdbpie import Imdb
from django.db import connection

def stats():
    cursor = connection.cursor()
    form = Search()

    stats = Stats.objects.all()[0]
    total_titles = stats.title_count
    total_people = stats.people_count
    total_user = stats.user_count
    total_ratings = stats.rating_count

    #(1)Overview of the database
    number = [total_titles,total_people,total_user,total_ratings]
    plt.clf()
    barlist = plt.bar(['titles','people','users','ratings'],number)
    barlist[0].set_color('#33691E')
    barlist[1].set_color('#FDD835')
    barlist[2].set_color('#E65100')
    barlist[3].set_color('#FFA500')
    plt.savefig('static/image/bar1.png')

    #(2)Total title number by Genres:
    # It's better to generate a new table to do that
    genrelist = Genres.objects.filter().order_by('-num_titles')
    genre_ratings = Genres.objects.order_by('-num_ratings')[:10]
    genre_titles = genrelist[:10]

    number = [g.num_titles for g in genre_titles]
    plt.clf()
    fig = plt.figure()
    barlist = plt.bar([g.name for g in genre_titles], number)
    fig.autofmt_xdate()
    plt.savefig('static/image/bar2.png', bbox_inches='tight')

    number = [g.num_ratings for g in genre_ratings]
    plt.clf()
    fig = plt.figure()
    barlist = plt.bar([g.name for g in genre_ratings], number)
    fig.autofmt_xdate()
    plt.savefig('static/image/bar3.png', bbox_inches='tight')

    #(3)Top ranking movie
    top_titles = Titles.objects.raw(
        "SELECT t.* "
        "FROM titles t JOIN top_titles tt ON t.id = tt.title_id "
        "ORDER BY tt.rank"
    )

    return {
        'form': form,
        'total_titles': total_titles,
        'total_people': total_people,
        'total_user': total_user,
        'total_ratings': total_ratings,
        'genrelist': genrelist,
        'top_titles': top_titles,
    }


def Homepage(request):
    return render(request, 'webapp/Homepage.html', stats())


def find(request):
    if request.method == 'GET':
        form = forms.Search(request.GET)
        if form.is_valid():
            search_genre = form.cleaned_data['search_genre']
            search_content = form.cleaned_data['search_content']
            movie_result=[]
            user_result = []
            people_result=[]
            predicate = '%{}%'.format(search_content)
            if search_genre == 'movie':
                movie_result = Titles.objects.raw(
                    "SELECT * "
                    "FROM titles "
                    "WHERE primary_title LIKE %s "
                    "ORDER BY (num_ratings * avg_rating) DESC "
                    "LIMIT 50",
                    [predicate]
                )
            elif search_genre == 'people':
                #Just for test the detail page, since the raw query with join cost long time
                people_result = People.objects.filter(
                    name__icontains = search_content
                )[:50]
                # people_result = Titles.objects.raw(
                #     "SELECT p.* "
                #     "FROM people p "
                #     "    JOIN known_for k ON p.id = k.people_id "
                #     "    JOIN titles t ON t.id = k.title_id "
                #     "    JOIN has_profession hp ON p.id = hp.people_id "
                #     "    JOIN professions pr ON pr.id = hp.profession_id "
                #     "WHERE p.name LIKE %s "
                #     "GROUP BY p.id "
                #     "ORDER BY SUM(t.num_ratings * t.avg_rating) DESC "
                #     "LIMIT 30",
                #     [predicate]
                # )
            else:
                user_result = Users.objects.filter(
                    name__icontains = search_content
                )[:50]

    return render(
        request,
        'webapp/Homepage.html',
        {
            **stats(),
            **{
                'user_result':user_result,
                'movie_result':movie_result,
                'people_result':people_result
            }
        }
    )


def register(request):
    success = 0
    form = Register()
    id = Users.objects.count()+10
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.id = id
            user.num_ratings = 0
            user.save()
            success = 1
        else:
            print("Register Failed!")
    return render(request,'webapp/Register.html',{'form':form,'id':id,'success':success})


def detail(request):
    rating_out_range = 0

    login_con = request.session.get('id')
    success = -1
    form = Rating()
    raw_id = request.path
    imdb_id = raw_id.split("/")[-1]
    imdb = Imdb()
    info = imdb.get_title(imdb_id)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM titles WHERE imdb_id = %s",[imdb_id])
    all_info = cursor.fetchone()

    id = all_info[0]
    runtime = all_info[7]
    start_year = all_info[5]
    num_ratings = all_info[9]
    avg_rating = all_info[10]

    title = info['base']['title']
    try:
        description = info['plot']['outline']['text']
    except:
        description = "Sorry,we don't have any description for this movie"
    try:
        image_url = info['base']['image']['url']
    except:
        image_url = 0

    #video
    try:
        video_url = imdb.get_title_videos(imdb_id)['videos'][0]['encodings'][0]['play']
    except:
        video_url = 0

    # Writers
    writers = People.objects.raw(
        "SELECT p.* "
        "FROM writes w JOIN people p ON w.people_id = p.id "
        "WHERE w.title_id = %s",
        [id]
    )

    #Directs
    directors = People.objects.raw(
        "SELECT p.* "
        "FROM directs d JOIN people p ON d.people_id = p.id "
        "WHERE d.title_id = %s",
        [id]
    )

    #Actors
    actors = People.objects.raw(
        "SELECT p.* "
        "FROM known_for k JOIN people p ON k.people_id = p.id "
        "WHERE k.title_id = %s",
        [id]
    )
    #Rating part
    if request.method == 'POST':
        form = Rating(request.POST)
        if form.is_valid():
            user_id = request.session.get('id')
            rating = form.cleaned_data['rating']
            if rating >= 0 and rating <= 10:
                try:
                    cursor.execute(
                    "INSERT INTO rates(user_id,title_id,rating)"
                    "VALUES(%s,%s,%s)",
                    [user_id,id,rating])
                    success = 1
                except:
                    success = 0
            else:
                rating_out_range = 1
    return render(request,'webapp/Detailpage.html',{
            'video_url':video_url,
            'image_url':image_url,
            'title':title,
            'description':description,
            'runtime':runtime,
            'start_year':start_year,
            'num_ratings':num_ratings,
            'avg_rating':avg_rating,
            'form':form,
            'login_con':login_con,
            'success':success,
            'rating_out_range':rating_out_range,
            'writers':writers,
            'directors':directors,
            'actors':actors})


def login(request):
    cursor = connection.cursor()
    form = Login()
    success = 2
    rating_history = []
    User_not_exist = 0
    if request.method =='POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login_username']
            password = form.cleaned_data['password']
            try:
                User_info=Users.objects.get(username=username)
                if User_info.password == password:
                    success = 1
                    rating_history = Rates.objects.filter(user = User_info.id)
                    request.session['id'] = User_info.id
                else:
                    success = 0
            except:
                User_not_exist = 1
    return render(request,'webapp/Login.html',{
            'form':form,
            'success':success,
            'rating_history':rating_history,
            'User_not_exist':User_not_exist})

def userinfo(request):
    raw_id = request.path
    #Is there a better way to get the id?
    id = raw_id.split("/")[-1]
    info = Users.objects.get(id=id)
    name = info.name
    username = info.username
    num_ratings = info.num_ratings
    rating_history = Rates.objects.filter(user = id)
    return render(request,'webapp/Userinfo.html',
    {'rating_history':rating_history,
    'id':id,
    'name':name,
    'username':username,
    'num_ratings':num_ratings})

def actorinfo(request):
    cursor = connection.cursor()
    id = request.path.split("/")[-1]
    actor = People.objects.get(id = id)
    name = actor.name
    imdb_id = actor.imdb_id
    imdb = Imdb()
    info = imdb.get_name(imdb_id)

    try:
        image_url = info['base']['image']['url']
    except:
        image_url = 0
    try:
        description = info['base']['miniBios'][0]['text']
    except:
        description = "Sorry,we don't have any description for this celebrity"

    try:
        video_url = imdb.get_name_videos(imdb_id)['videos'][0]['encodings'][0]['play']
    except:
        video_url = 0

    professions = Professions.objects.raw(
        "SELECT * "
        "FROM has_profession h JOIN professions p ON h.profession_id = p.id "
        "WHERE h.people_id = %s",
        [id]
    )
    known_for = Titles.objects.raw(
        "SELECT t.* "
        "FROM titles t JOIN known_for k ON t.id = k.title_id "
        "WHERE k.people_id = %s",
        [id]
    )
    return render(request,'webapp/Actordetail.html',
            {'name':name,
            'image_url':image_url,
            'description':description,
            'professions':professions,
            'known_for':known_for,
            'video_url':video_url})
