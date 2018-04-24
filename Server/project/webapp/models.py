from django.db import models
from django.contrib.auth.models import AbstractUser


class Directs(models.Model):
    people_id = models.IntegerField(blank=True, null=True)
    title_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'directs'


class Episodes(models.Model):
    title = models.ForeignKey('Titles', models.DO_NOTHING, primary_key=True)
    title = models.ForeignKey('Titles', models.DO_NOTHING, blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    episode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episodes'


class Genres(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    num_titles = models.IntegerField()
    num_ratings = models.IntegerField()
    avg_rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'genres'


class HasGenre(models.Model):
    title = models.ForeignKey('Titles', models.DO_NOTHING)
    genre = models.ForeignKey(Genres, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'has_genre'
        unique_together = ('title', 'genre')


class HasProfession(models.Model):
    people_id = models.IntegerField(blank=True,null=True)
    profession_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'has_profession'


class KnownFor(models.Model):
    people = models.ForeignKey('People', models.DO_NOTHING)
    title_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'known_for'
        unique_together = ('people', 'title_id')


class People(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Professions(models.Model):
    id = models.IntegerField(blank=True,primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'professions'


class Rates(models.Model):
    #a small problem here 
    user = models.ForeignKey('Users', models.DO_NOTHING, primary_key=True)
    title = models.ForeignKey('Titles', models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rates'
        unique_together = ('user', 'title')


class TitleTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'title_types'


class Titles(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=32, blank=True, null=True)
    primary_title = models.CharField(max_length=255, blank=True, null=True)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    is_adult = models.IntegerField(blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    type = models.ForeignKey(TitleTypes, models.DO_NOTHING, blank=True, null=True)
    num_ratings = models.IntegerField(blank=True, null=True)
    avg_rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'titles'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    num_ratings = models.IntegerField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Writes(models.Model):
    people_id = models.IntegerField(blank=True, null=True)
    title_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'writes'


class TopTitles(models.Model):
    rank = models.IntegerField(primary_key=True)
    title = models.ForeignKey(
        'Titles',
        models.DO_NOTHING,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'top_titles'


class Stats(models.Model):
    id = models.IntegerField(primary_key=True)
    title_count = models.IntegerField(blank=True, null=True)
    people_count = models.IntegerField(blank=True, null=True)
    user_count = models.IntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stats'
