from bottle import *
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree

api_ip = "localhost"
api_port = 8081
local_input = "dblp_2017_2021.xml"

file_work2 = "work_file.xml"
file_work = "dblp_2020_2021.xml"
date_work = ["2019", "2020"]

list_error_code = [400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 413, 414, 444, 500, 501, 502, 503, 504]

"""
Partie fonctions de l'API
"""

# précision sur le type d' encodage des fichiers xml
p = etree.XMLParser(resolve_entities=True, dtd_validation=True, load_dtd=True, recover=False)

# ouverture du fichier principal de travail
# TODO: a remettre come code
"""
tree2 = etree.parse(local_input, parser=p)
root2 = tree2.getroot()
"""
# écriture dans le fichier secondaire de travail des données qui nous interesse
# dans notre de cas, des années indiqués dans la variable "date_work".
# ex: les 5 dernières années. date_work = ["2017", "2018", "2019", "2020", "2021"]

""""
with open(file_work2, "w+") as file_work_open:
    header = f'''<?xml version="1.0" encoding="ISO-8859-1"?>
             <!DOCTYPE dblp SYSTEM "dblp.dtd">
            <dblp>
'''
    file_work_open.write(header)
    for article in root2.iter('article', 'inproceedings', 'proceeding', 'book', 'incollection', 'phdthesis',
                                  'mastersthesis'):
        for elem in article:
            if elem.tag == "year":
                if elem.text in date_work:
                    file_work_open.write(etree.tostring(article, pretty_print=True).decode("utf-8"))
    file_work_open.write("</dblp>")
"""
# ouverture du fichier secondaire comme fichier de travail pour l'API
tree = etree.parse(file_work, parser=p)
root = tree.getroot()


def get_authors_info(name: str) -> dict:
    """Fonction qui prend le nom d' un auteur et retourne le nombre
    d' articles écrit par lui ainsi que le nombre de co-auteur avec
    lequel il a écrit certains articles.

    :param name: le nom de l' auteur

    :return: une liste: position 0: le nombre d' article écrit
                    position 1: le nombre de co-auteur
    """

    info_author = {"PUBLICATIONS": set(), "CO-AUTHORS": set()}
    for publication in root.iter('article', 'inproceedings', 'proceeding', 'book', 'incollection', 'phdthesis',
                                 'mastersthesis'):
        authors_of_articles = []
        title_of_articles = []
        for elem_pub in publication:
            if elem_pub.tag == "author" and elem_pub.text is not None:
                authors_of_articles.append(elem_pub.text.lower())
            if elem_pub.tag == "title":
                title_of_articles.append(elem_pub.text)
        if name.lower() in authors_of_articles:
            info_author["PUBLICATIONS"] |= set(title_of_articles)
            info_author["CO-AUTHORS"] |= set(authors_of_articles)
    result = {"PUBLICATIONS": len(info_author["PUBLICATIONS"]),
              "CO-AUTHORS": len(info_author["CO-AUTHORS"]) - 1}
    return result


def get_publications_author(name: str, start: int = 0, count: int = 100) -> list:
    """Fonction qui permet d' obtenir la liste des publications d' un auteur.
    le nombre de publications retourner est fonction des paramètres start et count.

    :param name: nom de l' auteur;
    :param start: définit à partir de quelle publication retourner le résultat;
    :param count : détermine le nombre maximum de publication à retourner comme résultat.

    :return: la liste des publications faites par l' auteur.
    """

    if start < 0:
        start = 0
    if 1 > count > 100:
        count = 100
    pub_author = set()
    result = []
    for publication in root.iter('article', 'inproceedings', 'proceeding', 'book', 'incollection', 'phdthesis',
                                 'mastersthesis'):
        is_author = False
        title = ""
        for elem in publication:
            if elem.tag == "author" and elem.text.lower() == name.lower():
                is_author = True
            elif elem.tag == "title":
                title = elem.text
        if is_author:
            pub_author |= {title}
            # Controle si le nombre de publications actuellemet enregistré
            # est supérieur ou égal au nombre dont j' ai besoin
            if len(pub_author) >= start + count:
                for pub in pub_author:
                    result.append(pub)
                return result[start:start + count]
    for pub in pub_author:
        result.append(pub)
    return result[start:]


def is_publication_core_with_rank(title: str, rank: str) -> bool:
    """Fonction qui permet de déterminer si une publication est de rang spécifié

    :param title: le titre de la publication recherché
    :param rank: le rang que devrait avoir la publication recherché

    :return: True si la publication est de rang spécifié et False autrement
    """

    page = 1

    while True:
        # url du document à analyser
        a_url = f"http://portal.core.edu.au/jnl-ranks/?search={title}&by=title&source=all&sort=atitle&page={page}"

        # téléchargement du document à analyser
        r = requests.get(a_url)

        # vérification de l' aboutissement de la requete
        if r.status_code in list_error_code:
            return False

        # Extraction des données du fichier
        soup = BeautifulSoup(r.text, features="lxml")
        # extraction du tableau
        table_publications = soup.find('table')
        is_first_line = True
        # Analyse des publications obtenus comme résultat
        for publications in table_publications.find_all('tr'):
            if is_first_line:
                is_first_line = False
                continue
            pos = 1
            title_publication = ""
            source_publication = ""
            rank_publication = ""
            for elem in publications.find_all('td'):
                if pos == 1:
                    # print("title in for = " + elem.text)
                    tp = elem.text.split()
                    title_publication = " ".join(tp)
                    pos += 1
                elif pos == 2:
                    tp = elem.text.split()
                    source_publication = " ".join(tp)
                    pos += 1
                elif pos == 3:
                    tp = elem.text.split()
                    rank_publication = " ".join(tp)
                    pos += 1
                else:
                    pos += 1
            if title.lower() == title_publication.lower():
                if rank_publication.lower() == rank.lower():
                    return True
                else:
                    return False


def get_publications_rank_author(name: str, rank: str) -> list:
    """
    Fonction qui permet d' obtenir la liste des publications d' un auteur de rang celui passé en paramètre
    :param name: le nom de l' auteur
    :param rank: le rang des publications recherchés
    :return: la liste des publications de l' auteur de rang rank
    """

    if rank == "NotRanked":
        rank = "Not ranked"
    list_publications = get_publications_author(name)
    set_publications_rank = set()
    for publications in list_publications:
        if is_publication_core_with_rank(publications[0:len(publications)-1], rank):
            set_publications_rank |= {publications}
    if set_publications_rank:
        final_list = []
        for elem in set_publications_rank:
            final_list.append(elem)
        return final_list
    else:
        return []


def get_coauthors_author(name: str, start: int = 0, count: int = 100) -> list:
    """Fonction qui permet d' obtenir la liste des co-auteurs ayant écrit des articles
    avec l' auteur. Le nombre de cette est déterminé par les paramètres start et count.

    name: nom de l' auteur;
    start: à partir de quel co-auteur retourner le résultat;
    count: le nombre maximal d' éléments de cette liste.

    return: la liste des co-auteurs ayant écrit des articles avec l' auteur.
    """

    co_authors = set()
    result = []
    for publication in root.iter('article', 'inproceedings', 'proceeding', 'book', 'incollection', 'phdthesis',
                                 'mastersthesis'):
        authors_of_articles = []
        for elem in publication:
            if elem.tag == "author" and elem.text is not None:
                authors_of_articles.append(elem.text.lower())
        if name.lower() in authors_of_articles:
            co_authors |= set(authors_of_articles)
            if len(co_authors) >= start + count + 1:
                co_authors -= {name.lower()}
                for elem in co_authors:
                    result.append(elem)
                return result[start:start + count]
    co_authors -= {name.lower()}
    for elem in co_authors:
        result.append(elem)
    return result[start:]


def get_search_substring_author(search_string: str, start: int = 0, count: int = 100) -> list:
    """Fonction qui permet d' obtenir la liste des noms d' auteur contenant
    une certaine sous-chaine.

    :param search_string: sous chaine à rechercher dans les noms d' auteurs;
    :param start: à partir de quel élément retourner le résultat;
    :param count: nombre d' éléments à renvoyer comme réponse.

    :return: la liste des auteurs contenant la sous-chaine passé en paramètre.
    """

    if start < 0:
        start = 0
    if 1 > count > 100:
        count = 100
    authors = set()
    for publication in root.iter('article', 'inproceedings', 'proceeding', 'book', 'incollection', 'phdthesis',
                                 'mastersthesis'):
        authors_of_articles = []
        for elem in publication:
            if elem.tag == "author" and elem.text is not None:
                if search_string == "*":
                    authors_of_articles.append(elem.text)
                elif search_string in elem.text:
                    authors_of_articles.append(elem.text)
        authors |= set(authors_of_articles)
        if len(authors) >= start + count:
            result = []
            for elem in authors:
                result.append(elem)
            return result[start:start + count]
    result = []
    for elem in authors:
        result.append(elem)
    return result[start:]


def get_distance(name_origin: str, name_destination: str) -> int:
    """Fonction qui permet de calculer la distance de collaboration
    entre les deux auteurs.

    :param name_origin: auteur de départ;
    :param name_destination: auteur d' arrivé;

    :return: - -1 s' il n'y a aucune collaboration distance entre
                    l' auteur de départ et celui d' arrivé
            - 0 si l' auteur de départ est le meme que celui d' arrivé
            - n > 0
    """

    # si le nom de l' auteur de départ est le meme que de celui de destination
    if name_origin.lower() == name_destination.lower():
        return 0
    list_of_coauthors = get_coauthors_author(name_origin.lower())
    list_alt = []
    for co in list_of_coauthors:
        list_alt.append(co.lower())
    list_of_coauthors = list_alt
    # si l' auteur de destination fait partie des co-auteurs de celui de déport
    if name_destination.lower() in list_of_coauthors:
        return 1
    dist = 1
    # ensemble de co-auteur déjà visité: au départ uniquement l' auteur de départ est visité
    coauthors_already_visited = {name_origin.lower()}
    # création de l' ensemble de connection
    set_of_connection = set(list_of_coauthors)
    while set_of_connection:
        dist += 1
        list_of_coauthors = list(set_of_connection)
        set_of_connection = set()
        for coauthor in list_of_coauthors:
            if coauthor in coauthors_already_visited:
                continue
            else:
                coauthors_already_visited |= {coauthor}
            loc = get_coauthors_author(coauthor)
            list_alt = []
            for co in loc:
                list_alt.append(co.lower())
            loc = list_alt
            if name_destination.lower() in loc:
                return dist
            else:
                set_of_connection |= set(loc)
    return -1


def generate_error(error_info=None):
    """Fonction qui permet de gé

    :param error_info: format de génération d' erreurs

    :return:
    """

    if error_info:
        return f"Not found: {error_info}!"
    else:
        return f"Not found!"


"""
Partie API
"""


@error(400)
def error400(error_info=None):
    if error_info:
        return f"Invalid request: {error_info}!"
    else:
        return f"Invalid request!"


@error(404)
def error404(error_info=None):
    if error_info:
        return f"Not found: {error_info}!"
    else:
        return f"Not found!"


@route('/authors/<name>')
def info_authors(name):
    if not name or name.isspace():
        message_error = "Nom d'auteur invalide"
        abort(404, generate_error(message_error))
    result = get_authors_info(name)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(result)


@route('/authors/<name>/publications')
def publications_author(name):
    # catch params in the url: /authors/<name>/publications?start=200&count=2
    start = request.query.start
    count = request.query.count
    try:
        if start:
            start = int(start)
        else:
            start = 0
    except Exception:
        message_error = "Paramètre start invalide"
        abort(404, generate_error(message_error))
    try:
        if count:
            count = int(count)
        else:
            count = 100
    except Exception:
        message_error = "Paramètre count invalide"
        abort(404, generate_error(message_error))
    result = get_publications_author(name=name, start=start, count=count)
    if not result:
        message_error = "L' auteur " + name + " n'a pas de publications répertorié!"
        abort(404, generate_error(message_error))
    return json.dumps(result)


@route('/authors/<name>/coauthors')
def coauthors_author(name):
    # catch params in the url: /authors/<name>/coauthors?start=200&count=2
    start = request.query.start
    count = request.query.count
    try:
        if start:
            start = int(start)
        else:
            start = 0
    except Exception:
        message_error = "Paramètre start invalide"
        abort(404, generate_error(message_error))
    try:
        if count:
            count = int(count)
        else:
            count = 100
    except Exception:
        message_error = "Paramètre count invalide"
        abort(404, generate_error(message_error))
    result = get_coauthors_author(name=name, start=start, count=count)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(result)


@route('/authors/<name>/publications/<rank>')
def publications_rank_author(name, rank):
    result = get_publications_rank_author(name, rank)
    if not result:
        message_error = "Pas de publication de l'auteur " + name + " de rank " + rank
        abort(404, generate_error(message_error))
    return json.dumps(result)


@route('/search/authors/<searchString>')
def search_author(searchString):
    # catch params in the url: /search/authors/<searchString>?start=200&count=2
    if not searchString or searchString.isspace():
        message_error = "Nom d'auteur invalide"
        abort(404, generate_error(message_error))
    start = request.query.start
    count = request.query.count
    try:
        if start:
            start = int(start)
        else:
            start = 0
    except Exception:
        message_error = "Paramètre start invalide"
        abort(404, generate_error(message_error))
    try:
        if count:
            count = int(count)
        else:
            count = 100
    except Exception:
        message_error = "Paramètre count invalide"
        abort(404, generate_error(message_error))
    if start is None or count is None:
        result = get_search_substring_author(search_string=searchString)
    else:
        result = get_search_substring_author(search_string=searchString, start=start, count=count)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(result)


@route('/authors/<name_origin>/distance/<name_destination>')
def distance(name_origin, name_destination):
    result = get_distance(name_origin=name_origin, name_destination=name_destination)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(result)


run(host=api_ip, port=api_port, reloader=True)
