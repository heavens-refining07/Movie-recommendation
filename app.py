from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)

# ─── DATASET ───────────────────────────────────────────────────────────────────
movies_data = [
    {"id":1,"title":"The Dark Knight","genres":"Action Crime Drama","director":"Christopher Nolan","cast":"Christian Bale Heath Ledger","description":"Batman faces the Joker a criminal mastermind who plunges Gotham into anarchy","year":2008,"rating":9.0},
    {"id":2,"title":"Inception","genres":"Action SciFi Thriller","director":"Christopher Nolan","cast":"Leonardo DiCaprio Joseph Gordon-Levitt","description":"A thief enters dreams to plant an idea in a target's mind","year":2010,"rating":8.8},
    {"id":3,"title":"Interstellar","genres":"Adventure Drama SciFi","director":"Christopher Nolan","cast":"Matthew McConaughey Anne Hathaway","description":"Astronauts travel through a wormhole near Saturn to find a new home for humanity","year":2014,"rating":8.6},
    {"id":4,"title":"The Shawshank Redemption","genres":"Drama","director":"Frank Darabont","cast":"Tim Robbins Morgan Freeman","description":"Two imprisoned men bond over years finding solace and redemption through decency","year":1994,"rating":9.3},
    {"id":5,"title":"Pulp Fiction","genres":"Crime Drama Thriller","director":"Quentin Tarantino","cast":"John Travolta Uma Thurman Samuel L Jackson","description":"Lives of two hit men a boxer and a pair of bandits intertwine in four tales of violence","year":1994,"rating":8.9},
    {"id":6,"title":"The Godfather","genres":"Crime Drama","director":"Francis Ford Coppola","cast":"Marlon Brando Al Pacino","description":"The aging patriarch of an organized crime dynasty transfers control to his reluctant son","year":1972,"rating":9.2},
    {"id":7,"title":"Forrest Gump","genres":"Drama Romance","director":"Robert Zemeckis","cast":"Tom Hanks Robin Wright","description":"The presidencies of Kennedy and Johnson through the eyes of an Alabama man with low IQ","year":1994,"rating":8.8},
    {"id":8,"title":"The Matrix","genres":"Action SciFi","director":"Wachowski Sisters","cast":"Keanu Reeves Laurence Fishburne","description":"A computer hacker learns about the true nature of reality and his role in the war against its controllers","year":1999,"rating":8.7},
    {"id":9,"title":"Goodfellas","genres":"Biography Crime Drama","director":"Martin Scorsese","cast":"Ray Liotta Robert De Niro Joe Pesci","description":"The story of Henry Hill and his life in the mob covering his relationship with his wife Karen","year":1990,"rating":8.7},
    {"id":10,"title":"Schindler's List","genres":"Biography Drama History","director":"Steven Spielberg","cast":"Liam Neeson Ben Kingsley","description":"In German-occupied Poland during World War II industrialist Oskar Schindler saves Jewish refugees","year":1993,"rating":9.0},
    {"id":11,"title":"The Silence of the Lambs","genres":"Crime Drama Thriller","director":"Jonathan Demme","cast":"Jodie Foster Anthony Hopkins","description":"A young FBI cadet seeks help from an imprisoned cannibal killer to catch another serial killer","year":1991,"rating":8.6},
    {"id":12,"title":"Avatar","genres":"Action Adventure Fantasy SciFi","director":"James Cameron","cast":"Sam Worthington Zoe Saldana","description":"A paraplegic Marine is dispatched to the moon Pandora on a unique mission","year":2009,"rating":7.8},
    {"id":13,"title":"Titanic","genres":"Drama Romance","director":"James Cameron","cast":"Leonardo DiCaprio Kate Winslet","description":"A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the ill-fated Titanic","year":1997,"rating":7.9},
    {"id":14,"title":"The Avengers","genres":"Action Adventure SciFi","director":"Joss Whedon","cast":"Robert Downey Jr Chris Evans Scarlett Johansson","description":"Earths mightiest heroes must come together and learn to fight as a team","year":2012,"rating":8.0},
    {"id":15,"title":"Joker","genres":"Crime Drama Thriller","director":"Todd Phillips","cast":"Joaquin Phoenix Robert De Niro","description":"In Gotham City mentally troubled comedian Arthur Fleck is disregarded by society","year":2019,"rating":8.4},
    {"id":16,"title":"Parasite","genres":"Comedy Drama Thriller","director":"Bong Joon-ho","cast":"Kang-ho Song Sun-kyun Lee","description":"Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan","year":2019,"rating":8.5},
    {"id":17,"title":"1917","genres":"Action Drama War","director":"Sam Mendes","cast":"George MacKay Dean-Charles Chapman","description":"Two British soldiers are given a seemingly impossible mission to deliver a message deep in enemy territory","year":2019,"rating":8.3},
    {"id":18,"title":"Whiplash","genres":"Drama Music","director":"Damien Chazelle","cast":"Miles Teller J.K. Simmons","description":"A promising young drummer enrolls at a cut-throat music conservatory where his pursuit of perfection drives him to the edge","year":2014,"rating":8.5},
    {"id":19,"title":"La La Land","genres":"Comedy Drama Music Romance","director":"Damien Chazelle","cast":"Ryan Gosling Emma Stone","description":"While navigating their careers in Los Angeles a pianist and an actress fall in love while attempting to reconcile their aspirations for the future","year":2016,"rating":8.0},
    {"id":20,"title":"Get Out","genres":"Horror Mystery Thriller","director":"Jordan Peele","cast":"Daniel Kaluuya Allison Williams","description":"A young African-American visits his white girlfriend's parents for the weekend where his simmering uneasiness about their reception of him eventually reaches a boiling point","year":2017,"rating":7.7},
    {"id":21,"title":"Mad Max Fury Road","genres":"Action Adventure SciFi","director":"George Miller","cast":"Tom Hardy Charlize Theron","description":"In a post-apocalyptic wasteland a woman rebels against a tyrannical ruler in search for her homeland","year":2015,"rating":8.1},
    {"id":22,"title":"Blade Runner 2049","genres":"Drama Mystery SciFi Thriller","director":"Denis Villeneuve","cast":"Ryan Gosling Harrison Ford","description":"A young blade runner discovers a long-buried secret that has the potential to plunge what's left of society into chaos","year":2017,"rating":8.0},
    {"id":23,"title":"Dune","genres":"Adventure Drama SciFi","director":"Denis Villeneuve","cast":"Timothee Chalamet Zendaya","description":"Feature adaptation of Frank Herberts science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset in the galaxy","year":2021,"rating":8.0},
    {"id":24,"title":"Spirited Away","genres":"Animation Adventure Family Fantasy","director":"Hayao Miyazaki","cast":"Daveigh Chase Suzanne Pleshette","description":"During her family's move to the suburbs a sulky 10-year-old girl wanders into a world ruled by gods witches and spirits","year":2001,"rating":8.6},
    {"id":25,"title":"Fight Club","genres":"Drama","director":"David Fincher","cast":"Brad Pitt Edward Norton","description":"An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more","year":1999,"rating":8.8},
    {"id":26,"title":"The Lion King","genres":"Animation Adventure Drama Family","director":"Roger Allers","cast":"Matthew Broderick Jeremy Irons","description":"Lion prince Simba flees his kingdom only to learn the true meaning of responsibility and bravery","year":1994,"rating":8.5},
    {"id":27,"title":"Gladiator","genres":"Action Adventure Drama","director":"Ridley Scott","cast":"Russell Crowe Joaquin Phoenix","description":"A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family","year":2000,"rating":8.5},
    {"id":28,"title":"The Departed","genres":"Crime Drama Thriller","director":"Martin Scorsese","cast":"Leonardo DiCaprio Matt Damon Jack Nicholson","description":"An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang","year":2006,"rating":8.5},
    {"id":29,"title":"No Country for Old Men","genres":"Crime Drama Thriller","director":"Coen Brothers","cast":"Tommy Lee Jones Javier Bardem Josh Brolin","description":"Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and a briefcase filled with money","year":2007,"rating":8.2},
    {"id":30,"title":"There Will Be Blood","genres":"Drama","director":"Paul Thomas Anderson","cast":"Daniel Day-Lewis Paul Dano","description":"A story of family religion hatred oil and madness featuring Daniel Plainview a silver miner turned oilman","year":2007,"rating":8.2},
]

df = pd.DataFrame(movies_data)

def build_tags(row):
    return f"{row['genres']} {row['director']} {row['cast']} {row['description']}"

df['tags'] = df.apply(build_tags, axis=1)

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['tags'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(movie_title, n=6):
    movie_title_lower = movie_title.lower().strip()
    matches = df[df['title'].str.lower().str.contains(movie_title_lower)]
    if matches.empty:
        return None, []
    idx = matches.index[0]
    movie = df.iloc[idx].to_dict()
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx][:n]
    recommended = []
    for i, score in sim_scores:
        rec = df.iloc[i].to_dict()
        rec['similarity'] = round(float(score) * 100, 1)
        recommended.append(rec)
    return movie, recommended

def get_all_titles():
    return sorted(df['title'].tolist())

# ─── ROUTES ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    titles = get_all_titles()
    return render_template('index.html', titles=titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie_title = data.get('movie', '')
    movie, recommendations = get_recommendations(movie_title)
    if movie is None:
        return jsonify({'error': 'Movie not found. Try another title!'}), 404
    return jsonify({'movie': movie, 'recommendations': recommendations})

@app.route('/all-movies')
def all_movies():
    return jsonify(df[['id','title','genres','year','rating']].to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
