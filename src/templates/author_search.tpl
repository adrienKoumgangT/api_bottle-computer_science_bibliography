<html>
	<head>
		<title>{{title}}</title>
	</head>
	<body>
		<h1>{{h1}}</h1>
		<p>
			% if list_content:
				<b>Liste des auteurs contenant le nom {{name}}:</b>
				<ul>
					% for content in contents:
						<li>{{content}}</li>
					% end
				</ul>
			% else:
				Le nom {{name}} n'est point présent dans la liste des auteurs répertoriés.
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