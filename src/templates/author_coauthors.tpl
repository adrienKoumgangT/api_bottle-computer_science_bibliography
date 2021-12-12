<html>
	<head>
		<title>{{title}}</title>
	</head>
	<body>
		<h1>{{h1}}</h1>
		<p>
			% if list_content:
				<b>Liste des co-auteurs de l'auteur {{author}}:</b>
				<ul>
					% for content in contents:
						<li>{{content}}</li>
					% end
				</ul>
			% else:
				L'auteur {{author}} n'a pas de co-auteur enregistré dans son actif.
			% end
		</p>
		<br>
		<!-- Button qui me permet de retourner à la home -->
		<p>
			<form action="/" method="get">
				<label for="home">Back to Home</label>
				<input type="submit" id="home" value="Go" name="home" />
			</form>
		</p>
	</body>
</html>