import bottle
import json
import requests

import sys

server_ip = "localhost"
server_port = 8084
api_ip = "localhost"
api_port = 8081

title_server = "publications scientifiques"

list_error_code = [400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 413, 414, 444, 500, 501, 502, 503, 504]


# la home
@bottle.get("/")
def start_server():
    site = {"title": title_server,
            "h1": "Bienvenue sur le site web dédiés au publications scientifiques"}
    s_home = bottle.template("templates/home.tpl", site)
    return s_home


@bottle.get("/authors/infos")
def info_authors():
    return '''
    <p>
        <form action="/authors/infos" method="post">
            <label for="name">nom:</label>
            <input name="name" type="text" />
            <input value="Go" type="submit" />
        </form>
    </p>
    <p>
        <form action="/" method="get">
            <label for="home">Home</label>
            <input type="submit" id="home" value="Go" name="home" />
        </form>
    </p>
    '''


@bottle.post("/authors/infos")
def get_info_authors():
    name = bottle.request.forms.getunicode('name')
    r = requests.get(f"http://{api_ip}:{api_port}/authors/{name}")
    if r.status_code in list_error_code:
        bottle.abort(404, "Ressource non trouvée!")
    print(type(r))
    print(r)
    result = json.loads(r.text)
    site = {"title": title_server,
            "h1": "Informations sur l'auteur",
            "name_author": name,
            "publications": result["PUBLICATIONS"],
            "coauteurs": result["CO-AUTHORS"]}
    if result["PUBLICATIONS"] > 0:
        site_author_infos = bottle.template("templates/author_infos.tpl", site, isauthor=True)
    else:
        site_author_infos = bottle.template("templates/author_infos.tpl", site, isauthor=False)
    return site_author_infos


@bottle.get("/authors/publications")
def publications_author():
    return '''
    <p>Requete d' informations sur les articles d'un auteur.</p>
    <form action="/authors/publications" method="post">
        <label for="name">nom:</label>
        <input name="name" type="text" /><br><br>
        <label for="start">Afficher les éléments à partir de l' élément n.:</label>
        <input name="start" type="number" min="0" value="0" /><br><br>
        <label for="count">Nombre d' élément à afficher:</label>
        <input name="count" type="number" min="0" max="100" value="John" /><br><br>
        <input value="Go" type="submit" />
    </form>
    '''


@bottle.post("/authors/publications")
def get_publications_author():
    name = bottle.request.forms.getunicode('name')
    start = bottle.request.forms.get('start')
    count = bottle.request.forms.get('count')
    # TODO: insérer start et count dans la requete
    r = requests.get(f"http://{api_ip}:{api_port}/authors/{name}/publications")
    if r.status_code in list_error_code:
        bottle.abort(404, "Ressource non trouvée!")
    result = json.loads(r.text)
    if result:
        site_elements = {"title": title_server,
                         "h1": "Publications d' article d' un auteur",
                         "author": name,
                         "contents": result}
        s = bottle.template("templates/author_publications.tpl", site_elements, list_content=True)
    else:
        site_elements = {"title": "publications scientifiques",
                         "h1": "Publications d' article d' un auteur",
                         "author": name,
                         "contents": []}
        s = bottle.template("templates/author_publications.tpl", site_elements, list_content=False)
    return s


@bottle.get("/authors/coauthors")
def coauthors_author():
    return '''
    <p>Requete d' informations sur les co-auteurs d' un auteur.</p>
    <form action="/authors/coauthors" method="post">
        <label for="name">nom:</label>
        <input name="name" type="text" /><br><br>
        <label for="start">Afficher les éléments à partir de l'ément n.:</label>
        <input name="start" type="number" min="0" value="0" /><br><br>
        <label for="count">Nombre d' élément à afficher:</label>
        <input name="count" type="number" min="0" max="100" value="John" /><br><br>
        <input value="Go" type="submit" />
    </form>
    '''


@bottle.post("/authors/coauthors")
def get_coauthors_author():
    name = bottle.request.forms.getunicode('name')
    start = bottle.request.forms.get('start')
    count = bottle.request.forms.get('count')
    # TODO: inserer start et count dans la requete
    r = requests.get(f"http://{api_ip}:{api_port}/authors/{name}/coauthors")
    if r.status_code in list_error_code:
        bottle.abort(404, "Ressource non trouvée!")
    result = json.loads(r.text)
    if result:
        site_elements = {"title": title_server,
                         "h1": "Liste de co-auteurs d'un auteur",
                         "author": name,
                         "contents": result}
        site_author_coauthors = bottle.template("templates/author_publications.tpl", site_elements, list_content=True)
    else:
        site_elements = {"title": "publications scientifiques",
                         "h1": "Liste de co-auteurs d'un auteur",
                         "author": name,
                         "contents": []}
        site_author_coauthors = bottle.template("templates/author_coauthors.tpl", site_elements, list_content=False)
    return site_author_coauthors


@bottle.get("/authors/search")
def search_author():
    return '''
    <p>Requete de liste d'auteurs.</p>
    <form action="/authors/search" method="post">
        <label for="name">nom:</label>
        <input name="name" type="text" /><br><br>
        <label for="start">Afficher les éléments à partir de l'ément n.:</label>
        <input name="start" type="number" min="0" value="0" /><br><br>
        <label for="count">Nombre d'élément à afficher:</label>
        <input name="count" type="number" min="0" max="100" value="John" /><br><br>
        <input value="Go" type="submit" />
    </form>
    '''


@bottle.post("/authors/search")
def get_search_author():
    name = bottle.request.forms.getunicode('name')
    start = bottle.request.forms.get('start')
    count = bottle.request.forms.get('count')
    # TODO: insérer start et count dans la requete
    r = requests.get(f"http://{api_ip}:{api_port}/search/authors/{name}")
    if r.status_code in list_error_code:
        bottle.abort(404, "Ressource non trouvée!")
    result = json.loads(r.text)
    if result:
        site_elements = {"title": title_server,
                         "h1": "Liste d'auteurs",
                         "name": name,
                         "contents": result}
        site_author_publications = bottle.template("templates/author_search.tpl", site_elements, list_content=True)
    else:
        site_elements = {"title": "Liste d'auteurs",
                         "h1": "Liste d'auteurs",
                         "name": name,
                         "contents": []}
        site_author_publications = bottle.template("templates/author_search.tpl", site_elements, list_content=False)
    return site_author_publications


@bottle.get("/authors/distance")
def authors_distance():
    return '''
    <form action="/authors/distance" method="post">
        <label for="name1">nom de l'auteur de départ:</label>
        <input name="name1" type="text" /><br><br>
        <label for="name2">nom de l'auteur de destination:</label>
        <input name="name2" type="text" /><br><br>
        <input value="Go" type="submit" />
    </form>
    '''


@bottle.post("/authors/distance")
def get_authors_distance():
    name_origin = bottle.request.forms.getunicode('name1')
    name_destination = bottle.request.forms.getunicode('name2')
    r = requests.get(f"http://{api_ip}:{api_port}/authors/{name_origin}/distance/{name_destination}")
    if r.status_code in list_error_code:
        bottle.abort(404, "Ressource non trouvée!")
    result = json.loads(r.text)
    site = {"title": title_server,
            "h1": "Informations sur les auteurs: distance séparant 2 auteurs",
            "author1": name_origin,
            "author2": name_destination,
            "distance": result}
    if result == 0:
        site_author_distance = bottle.template("templates/author_distance.tpl", site, connect=False)
    else:
        site_author_distance = bottle.template("templates/author_distance.tpl", site, connect=True)
    return site_author_distance


def read_config(name_file):
    if name_file:
        with open(name_file, 'w') as file_config:
            try:
                # si le fichier dont le nom est passé en ligne de commande n' est pas un fichier json
                # on prend les paramètres par défaut
                data = json.load(file_config)
                # s' il manque un seul élément de configuration, in prend ceux par défaut
                server_ip_read = data["SERVER WEB"]["IP"]
                server_port_read = data["SERVER WEB"]["PORT"]
                api_ip_read = data["API WEB"]["IP"]
                api_port_read = data["API WEB"]["PORT"]
            except Exception:
                return None
            return [server_ip_read, server_port_read, api_ip_read, api_port_read]


if __name__ == "__main__":
    bottle.run(host=server_ip, port=server_port, reloader=True)
    if len(sys.argv) > 1:
        # si un fichier de configuration est passé en paramètre en ligne de commande
        server_config = read_config(name_file=sys.argv[1])
        if server_config is None:
            # si la lecture du fichier de configuration ne s' est pas bien déroulé
            print(f"""configuration du serveur:
                        - adresse serveur ip = {server_ip}
                        - adresse serveur port = {server_port}
                        - adresse api ip = {api_ip}
                        - adresse api port = {api_port}
                        """)
        else:
            # si la lecture du fichier de configuration s' est bien déroulé
            server_ip = server_config[0]
            server_port = server_config[1]
            api_ip = server_config[2]
            api_port = server_config[3]
            print(f"""configuration du serveur:
                - adresse serveur ip = {server_ip}
                - adresse serveur port = {server_port}
                - adresse api ip = {api_ip}
                - adresse api port = {api_port}
                """)
    else:
        # si aucun fichier de configuration du serveur n' est passé en ligne de commande,
        # on prend les configurations par défaut
        print(f"""configuration du serveur:
            - adresse serveur ip = {server_ip}
            - adresse serveur port = {server_port}
            - adresse api ip = {api_ip}
            - adresse api port = {api_port}
            """)
