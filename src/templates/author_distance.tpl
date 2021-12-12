<html>
	<head>
		<title>{{title}}</title>
	</head>
	<body>
		<h1>{{h1}}</h1>
		<p>
			% if connect:
				L'auteur {{author1}} et l'auteur {{author2}} sont connectés avec une distance {{distance}}.
			% else:
				L'auteur {{author1}} et l'auteur {{author2}} ne sont point connectés.
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