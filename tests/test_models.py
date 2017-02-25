import responses

from tests import BaseStarWarsAPITestCase
from starwars_api.exceptions import SWAPIClientError
from starwars_api.models import *


class PeopleTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_people_model(self):
        luke = People.get(1)
        self.assertEqual(luke.name, 'Luke Skywalker')
        self.assertEqual(luke.name, 'Luke Skywalker')
        self.assertEqual(luke.height, '172')
        self.assertEqual(luke.mass, '77')
        self.assertEqual(luke.hair_color, 'blond')
        self.assertEqual(luke.skin_color, 'fair')
        self.assertEqual(luke.eye_color, 'blue')
        self.assertEqual(luke.birth_year, '19BBY')
        self.assertEqual(luke.gender, 'male')

    @responses.activate
    def test_people_model_not_found(self):
        error = ('Request to SWAPI "/api/people/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            People.get(100)


class PeopleQuerySetTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_people_qs_next(self):
        qs = People.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, People))
        self.assertEqual(obj.name, 'Luke Skywalker')

    @responses.activate
    def test_people_qs_iterable(self):
        qs = People.all()
        # 10 in page1, 5 in page2
        self.assertEqual(len([elem for elem in qs]), 15)

    @responses.activate
    def test_people_qs_count(self):
        qs = People.all()
        self.assertEqual(qs.count(), 15)


class FilmsTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_films_model(self):
        objFilm = Films.get(1)
        self.assertEqual(objFilm.title, 'A New Hope')
        self.assertEqual(int(objFilm.episode_id), 4)
        self.assertEqual(objFilm.opening_crawl, "It is a period of civil war.\r\nRebel spaceships, striking\r\nfrom a hidden base, have won\r\ntheir first victory against\r\nthe evil Galactic Empire.\r\n\r\nDuring the battle, Rebel\r\nspies managed to steal secret\r\nplans to the Empire's\r\nultimate weapon, the DEATH\r\nSTAR, an armored space\r\nstation with enough power\r\nto destroy an entire planet.\r\n\r\nPursued by the Empire's\r\nsinister agents, Princess\r\nLeia races home aboard her\r\nstarship, custodian of the\r\nstolen plans that can save her\r\npeople and restore\r\nfreedom to the galaxy....")
        self.assertEqual(objFilm.director, 'George Lucas')
        self.assertEqual(objFilm.producer, 'Gary Kurtz, Rick McCallum')
        self.assertEqual(objFilm.release_date, '1977-05-25')
        self.assertEqual(len(objFilm.characters), 18)
        self.assertEqual(len(objFilm.planets), 3)
        self.assertEqual(len(objFilm.starships), 8)
        self.assertEqual(len(objFilm.vehicles), 4)
        self.assertEqual(len(objFilm.species), 5)
        self.assertEqual(objFilm.created, '2014-12-10T14:23:31.880000Z')
        self.assertEqual(objFilm.edited, '2015-04-11T09:46:52.774897Z')
        self.assertEqual(objFilm.url, 'http://swapi.co/api/films/1/')

    @responses.activate
    def test_films_model_not_found(self):
        error = ('Request to SWAPI "/api/films/100" failed with '
                 'status "404". Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            Films.get(100)


class FilmsQuerySetTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_films_qs_next(self):
        qs = Films.all()
        obj = qs.next()
        self.assertTrue(isinstance(obj, Films))
        self.assertEqual(obj.title, 'A New Hope')

    @responses.activate
    def test_films_qs_iterable(self):
        qs = Films.all()
        # 10 in page1, 5 in page2
        self.assertEqual(len([elem for elem in qs]), 7)

    @responses.activate
    def test_films_qs_count(self):
        qs = Films.all()
        self.assertEqual(qs.count(), 7)
