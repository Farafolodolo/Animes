from flask import Blueprint, render_template, request, jsonify
from models import get_cursor
import json
#A blueprint is a way to declarate the endpoints
main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template('anime.html')


@main_bp.route('/api/animes')
def get_animes():
    try:
        #Im getting all the args from the javascript, all the args came from inputs on the HTML
        search = request.args.get('search', '')
        #If there is nothing, the default value will be void
        year = request.args.get('year', '')
        season = request.args.get('season', '')
        format_type = request.args.get('format', '')
        status = request.args.get('status', '')
        genre = request.args.get('genre', '')
        #It gets the pagination on the page
        page = request.args.get('page', 1, type=int)
        #It will be showing 10 while the user will be scrolling down on the front of the animes
        per_page = 10
        #It's where the pagination beggins
        offset = (page - 1) * per_page

        #It's the base query
        query = """
            SELECT SQL_CALC_FOUND_ROWS 
                id_anime, title, year, season, type, 
                status, episodes, genres, img 
            FROM animes 
            WHERE 1=1
        """
        
        #I created this list to add all the params
        params = []

        #If the input search was used, it will add to the query to add in the Where clause, it's going to search with like instead = because it can finds with only few letters (also the param is added with the %% for that)
        if search:
            query += " AND title LIKE %s"
            params.append(f"%{search}%")
        #If the varible year exists (or is not None), it will add on the query and on the list 
        if year:
            query += " AND year = %s"
            params.append(year)
        #If the variable season exists, it will add on the query and on the list 
        if season:
            query += " AND season = %s"
            params.append(season)
        #If the format_type exists, it will add on the query and on the list 
        if format_type:
            query += " AND type = %s"
            params.append(format_type)
        #If the status exists, it will add on the query and on the list 
        if status:
            query += " AND status = %s"
            params.append(status)
        #If the genre exists, it will add on the query and on the list (this also use like because there are animes with 2 or more genres)
        if genre:
            query += " AND genres LIKE %s"
            params.append(f"%{genre}%")

        #At the final, will add to the query the limit and offset (limit is how many rows I want, and the offset is where it beggins the consult)
        query += " LIMIT %s OFFSET %s"
        #In the front there is not a explicit pagination, but it's activated with the scroll
        params.extend([per_page, offset])

        #It executes the query and gets the information
        cursor = get_cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        #I created this list to add all the animes
        animes = []
        for row in results:
            #I stored all the information in a dictionary to get in an easier way on the javascripts
            anime = {
                'id': row[0],
                'title': row[1],
                'year': row[2],
                'season': row[3],
                'format_type': row[4],
                'airing_status': row[5],
                'episodes': row[6],
                'genres': row[7].split(',') if row[7] else [],
                'image_url': row[8]
            }
            #It adds the dictionary in the list
            animes.append(anime)
        #It selects how many rows the query returned
        #QUIERO QUE ME EXPLIQUES ESTA PARTE DEEPSEEK
        cursor.execute("SELECT FOUND_ROWS()")
        total_records = cursor.fetchone()[0]
        #If there are more rows, it will be true and allows the user keep scrolling
        has_next = (offset + per_page) < total_records  

        #It returns all the information as json
        return jsonify({
            'animes': animes,
            'has_next': has_next
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
            
@main_bp.route('/specific_anime/<id_anime>')
def specific_anime(id_anime):
    cursor = get_cursor()
    #It stablish the query, in this page will returns a specific anime with ID
    query = """
        SELECT title, episodes, type, genres, status, year, rating, score, synopsis, season, producers, licensors, studios, img, streaming
        FROM animes
        WHERE id_anime = %s
    """
    cursor.execute(query, (id_anime,))
    anime = cursor.fetchone()
    
    #If the anime exists (with that ID) it will store the information in a dictionary and render a template sending that parameter
    if anime:
        anime_data = {
            'title': anime[0],
            'episodes': anime[1],
            'type': anime[2],
            'genres': anime[3],
            'status': anime[4],
            'year': anime[5],
            'rating': anime[6],
            'score': anime[7],
            'synopsis': anime[8],
            'season': anime[9] if anime[9] else '', #If the anime does not have a season will store only a void value
            'producers': anime[10],
            'licensors': anime[11],
            'studios': anime[12],
            'image_url': anime[13],
            'streaming': json.loads(anime[14]) if anime[14] else [] #If the anime does not have a streaming page will store only a void value, I needed to use the json.loads because the streaming came from the database as a json variable
        }

        cursor.close()
        return render_template('pagina_anime.html', anime=anime_data)
    else:
        #If the ID does not exist on the database, it will return a not found page
        return render_template('not_found.html')