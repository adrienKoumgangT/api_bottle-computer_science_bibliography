from requests import *
from json import *
import unittest


class TestAPIMethods(unittest.TestCase):
    server_ip = "localhost"
    server_port = 8081

    def test_author(self):
        # test bon fonctionnement
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Eun%20Ah%20Lee")
        data = r1.text
        # l = "Le nombre de publications 1<br/>Le nombre de co_auteurs 4"
        l = '{"PUBLICATIONS": 1, "CO-AUTHORS": 4}'
        self.assertEqual(data, l)
        self.assertNotEqual(data, "Indira Nair")

    def test_unknown(self):
        # test d' un auteur qui n' existe pas et  qui doit afficher erreur
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Inconnu/publications")
        self.assertEqual(r1.status_code, 404)

    def test_coauthors(self):
        # marche pas
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Amos%20Darko/coauthors")
        self.assertEqual(r1.status_code, 200)

    def test_search_string_unknown(self):
        # test pas d' auteur trouvé
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/ ")
        self.assertEqual(r1.status_code, 404)

    def test_search_string_start(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Adrien?start=50&count=15")
        self.assertEqual(len(loads(r1.text)), 15)

    def test_distance(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/M.%20Reza%20Hosseini/distance/Igor%20Martek")
        data = r1.text
        l = "1"
        self.assertEqual(data, l)

    def test_distance2(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/M.%20Reza%20Hosseini/distance/Greg%20Dome")
        self.assertEqual(r1.text, "-1")


if __name__ == '__main__':
    unittest.main()
