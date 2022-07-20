import sqlite3


class DbConnect:
    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

#поиск по названию

def movie_by_title(title):
    db_connect = DbConnect("netflix.db")
    db_connect.cur.execute(f"""
    SELECT title,country,release_year,listed_in,description 
    from netflix 
    where title like '%{title}%' 
    order by release_year desc
    limit 1""")

    result = db_connect.cur.fetchall()
    return{
		"title": result[0],
		"country": result[1],
		"release_year": result[2],
		"genre": result[3],
		"description": result[4]
}

#поиск по диапазону лет выпуска

def movies_by_years(year1, year2):
    db_connect = DbConnect("netflix.db")
    query= f"select from title,release_year from netflix where release_year between {year1} and {year2} limit 100"
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append ({"title": movie[0],
                             "release_year":movie[1]})
    return result_list


# поиск по рейтингу

def movies_by_rating(rating):
    db_connect = DbConnect("netflix.db")
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    query = f" select title,rating, describtion from netflix where rating ({rating_parameters[reting]})"
    result = db_connect.cur.execute(query)
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie [0],
            "rating": movie[1],
            "description": movie[2]
        })
    return result_list

#поиск по жанру


def movies_by_genere(genre):
    result = execute_query( f""" select title, description
    from netflix
    where listed_in like '%{genre}%'
    order by release_year desc
    limit 10;""")
    result_list = []
    for movie in result:
        result_list.append ({
            "title": movie[0],
            "description": movie[1]
        })
    return result_list

#функция, которая получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
#возвращает список тех, кто играет с ними в паре больше 2 раз.

def cast_partners(actor1,actor2):
    query = f" select `cast` from netflix where `cast` like ''%{actor1}%' and `cast` like '%{actor2}%';"
    result = execute_query(query)
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1,actor2] and count > 2:
            result_list.append(actor)
    return result_list

#функцию, с помощью которой можно будет передавать тип картины (фильм или сериал),
#год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON.

def search_movie_by_param(movie_type, release_year,genre):
    query =  f"""select title,description
    from netflix
    where type = '{movie_type}'
    and relese_year= '{release_year}'
    and listed_in like '%{genre}%'"""
    result = execute_query(query)
    result_list= []
    for movie in result:
        result_list.append({'title': movie[0],
                            'description': movie[1]})
    return result_list