<html>
	<head>
		<title>{{title}}</title>
	</head>
	<body>
		<h1>{{h1}}</h1>
		<p>
			Quelle recherche aimeriez vous effectuer ?:
			<ul>
				<li>
					<form action="/authors/infos" method="get">
						<label for="info">Information sur un auteur</label>
						<input type="submit" id="info" value="Go" name="info_authors" />
					</form>
				</li>
				<li>
					<form action="/authors/publications" method="get">
						<label for="publication">Publication d'un auteur</label>
						<input type="submit" id="publication" value="Go" name="publications_authors" />
					</form>
				</li>
				<li>
					<form action="/authors/coauthors" method="get">
						<label for="coauthors">Co-auteur d'un auteur</label>
						<input type="submit" id="coauthors" value="Go" name="coauthors_author" />
					</form>
				</li>
				<li>
					<form action="/authors/search" method="get">
						<label for="search">Recherche d'auteur</label>
						<input type="submit" id="search" value="Go" name="search_author" />
					</form>
				</li>
				<li>
					<form action="/authors/distance" method="get">
						<label for="distance">Relation entre 2 auteurs</label>
						<input type="submit" id="distance" value="Go" name="authors_distance" />
					</form>
				</li>
			</ul>
		</p>
	</body>
</html>