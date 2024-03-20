import random
from lorem_text import lorem
from rb_books.models import Audience, Author, Book, Collection, Editor, Genre, Rating, Volume


def create_sample_authors():
    for _ in range(10):
        try:
            first_name, last_name = [e.capitalize() for e in lorem.words(2).split(' ')]
            Author.objects.create(first_name=first_name, last_name=last_name)
        except:
            pass


def create_sample_editors():
    for _ in range(10):
        try:
            name = lorem.words(1)
            Editor.objects.create(name=name)
        except:
            pass


def create_sample_genres():
    for _ in range(20):
        try:
            label_number = random.randint(1, 2)
            label = lorem.words(label_number).capitalize()
            description_number = random.randint(10, 50)
            description = lorem.words(description_number)
            Genre.objects.create(label=label, description=description)
        except:
            pass


def create_sample_ratings():
    for i in range(6):
        try:
            label_number = random.randint(1, 3)
            label = lorem.words(label_number).capitalize()
            code = label[:2].upper()
            description_number = random.randint(10, 30)
            description = lorem.words(description_number)
            Rating.objects.create(label=label, code=code, description=description, rating=i)
        except:
            pass


def create_sample_volumes():
    for i in range(100):
        try:
            value = i + 1
            Volume.objects.create(label=f'Tome {value}', code=f'T{value}')
        except:
            pass


def create_sample_audiences():
    for i in range(6):
        try:
            label_number = random.randint(2, 4)
            label = lorem.words(label_number).capitalize()
            description_number = random.randint(5, 20)
            description = lorem.words(description_number)
            Audience.objects.create(label=label, short_label=lorem.words(1), description=description)
        except:
            pass


def create_sample_data():
    create_sample_authors()
    create_sample_editors()
    create_sample_volumes()
    create_sample_genres()
    create_sample_ratings()
    create_sample_audiences()
