from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError

api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        pass

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        if cls.RESOURCE_NAME == 'people':
            data = api_client.get_people(resource_id)
            return People(json_data=data)
        elif cls.RESOURCE_NAME == 'films':
            data = api_client.get_films(resource_id)
            return Films(json_data=data)

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        if cls.RESOURCE_NAME == 'people':
            return PeopleQuerySet()

        elif cls.RESOURCE_NAME == 'films':
            return FilmsQuerySet()


class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)
        self.name = json_data.get('name', '')
        self.height = json_data.get('height', '0')
        self.mass = json_data.get('mass', '0')
        self.hair_color = json_data.get('hair_color', '')
        self.skin_color = json_data.get('skin_color', '')
        self.eye_color = json_data.get('eye_color', '')
        self.birth_year = json_data.get('birth_year', '')
        self. gender = json_data.get('gender', '')
        self.homeworld = json_data.get('homeworld', '')
        self.films = json_data.get('films', [])
        self.species = json_data.get('species', [])
        self.vehicles = json_data.get('vehicles', [])
        self.startships = json_data.get('starships', [])
        self.created = json_data.get('created', '')
        self.edited = json_data.get('edited', '')
        self.url = json_data.get('url', '')

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)
        self.title = json_data.get('title', '')
        self.episode_id = json_data.get('episode_id', '0')
        self.opening_crawl = json_data.get('opening_crawl', '')
        self.director = json_data.get('director', '')
        self.producer = json_data.get('producer', '')
        self.release_date = json_data.get('release_date', '')
        self.characters = json_data.get('characters', [])
        self.planets = json_data.get('planets', [])
        self.starships = json_data.get('starships', [])
        self.vehicles = json_data.get('vehicles', [])
        self.species = json_data.get('species', [])
        self.created = json_data.get('created', '')
        self.edited = json_data.get('edited', '')
        self.url = json_data.get('url', '')

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        self.page = 1
        json_data = self.get_data_by_page(self.page)
        self.data_count = json_data.get('count', 0)
        self.results = json_data.get('results', [])
        self.this_page_obj_visited = 0
        self.total_obj_visited = 0

    def get_data_by_page(self, page):
        json_data = {}
        if self.RESOURCE_NAME == 'people':
            json_data = api_client.get_people(page=page)
        elif self.RESOURCE_NAME == 'films':
            json_data = api_client.get_films(page=page)
        return json_data

    def __iter__(self):
        return self

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        if self.total_obj_visited == self.data_count:
            raise StopIteration
        if self.this_page_obj_visited == len(self.results):
            self.page += 1
            json_data = self.get_data_by_page(self.page)
            self.results = json_data.get('results', [])
            self.this_page_obj_visited = 0

        obj = None
        if self.RESOURCE_NAME == 'people' and len(self.results) > 0:
            obj = People(self.results[self.this_page_obj_visited])
        elif self.RESOURCE_NAME == 'films':
            obj = Films(self.results[self.this_page_obj_visited])
        self.this_page_obj_visited += 1
        self.total_obj_visited += 1
        return obj

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        return self.data_count


class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))
