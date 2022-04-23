import requests
import json
from bs4 import BeautifulSoup
import plotly.express as px
from tabulate import tabulate

#OMDb API: http://www.omdbapi.com/?i=tt3896198&apikey=c5eb6c3c
#API Key: 2a79e05ccbae6651cc86911773917142


CACHE_FILENAME = "cache.json"
def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def get_movie_info_fromWeb(movie):
    req = requests.get(movie.TicketURL)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        movie.PGRate = soup.find(attrs={'itemprop': 'contentRating' }).get_text()
    except:
        print(movie.TicketURL)
    movie.MovieDescription = soup.find('p',class_='show-text').get_text()
    movie.Genre = soup.find(attrs={'itemprop': 'genre' }).get_text()
    if(movie.Genre) == "":
        movie.Genre = "N/A"

    return (movie.Genre, movie.PGRate, movie.MovieDescription)

def assignDataToMovieObj(movieData, movieObject):
        movieObject.TicketURL = movieData['URL']
        movieObject.Genre =  movieData['gengre']
        movieObject.PGRate = movieData['PG']
        movieObject.MovieDescription = movieData['description']
        movieObject.MovieRating = movieData['rating']
        movieObject.MovieYear = movieData['year']


def get_recent_movie(MOVIE_CACHE):
    """
    Function that do web scrapping and get the newest movie
    from the ACM's website.
    returns a list of movie objects.
    """
    allMovies = []
    url = "https://www.amctheatres.com/movies?availability=NOW_PLAYING"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    data = soup.find_all("div", class_="PosterContent")
    for item in data:
        movieObject = Movie()
        movieObject.MovieName = item.find("h3").string
        if(movieObject.MovieName in MOVIE_CACHE):
            assignDataToMovieObj(MOVIE_CACHE[movieObject.MovieName], movieObject)
        else:
            try:
                releaseDate = item.find("span", class_="MoviePosters__released-month clearfix").get_text()
                releaseDate = " ".join(releaseDate.split()[1:])
                releaseYear = releaseDate[-4:]
            except:
                continue
            movieObject.MovieYear = releaseYear
            movieObject.TicketURL = "https://www.amctheatres.com" + item.a['href']
            (gengre,PG, description) = get_movie_info_fromWeb(movieObject)
            MOVIE_CACHE[movieObject.MovieName] = {'gengre': gengre, 'PG': PG, 'description': description, 'rating': 'N/A', 'year': releaseYear, 'URL':movieObject.TicketURL}
            save_cache(MOVIE_CACHE)
        allMovies.append(movieObject)
    return allMovies

def get_popular_movie(MOVIE_CACHE):
    popularMovie = []
    count = 0
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    data = soup.find_all("td", class_="titleColumn")
    for item in data:
        movieObject = Movie()
        itemData = item.get_text().strip().split('\n')
        movieObject.MovieName = itemData[1].lstrip()
        if(movieObject.MovieName in MOVIE_CACHE):
            assignDataToMovieObj(MOVIE_CACHE[movieObject.MovieName], movieObject)
        else:
            movieObject.TicketURL = 'https://www.imdb.com' + item.a['href']
            movieObject.MovieYear = itemData[-1][1:5]
            (description, PG, gengre, rating) = get_popular_movie_info(movieObject)
            movie_data = {'gengre': gengre, 'PG': PG, 'description': description, 'rating': rating, 'year': movieObject.MovieYear, 'URL':movieObject.TicketURL}
            assignDataToMovieObj(movie_data, movieObject)
            MOVIE_CACHE[movieObject.MovieName] = movie_data
            save_cache(MOVIE_CACHE)
    
        popularMovie.append(movieObject)
    return popularMovie


def get_popular_movie_info(movie):
    params = {'t':movie.MovieName, 'y': movie.MovieYear, 'plot':'full'}
    description = ''
    PG = ''
    gengre = []
    rating = ''
    try:
        response = requests.get('http://www.omdbapi.com/?apikey=c5eb6c3c',params=params)
        movieData = response.json()
        description = movieData['Plot']
        PG = movieData['Rated']
        for item in movieData['Genre'].split(','):
            gengre.append(item.strip())
        rating = movieData['imdbRating']
    except:
        print("Some data might be missing.")
    return (description, PG, gengre, rating)


class Movie:
    def __init__(self):
        self.MovieName = ''
        self.TicketURL = ''
        self.Genre = ''
        self.PGRate = ''
        self.MovieDescription = ''
        self.MovieRating = ''
        self.MovieYear = ''


def getGenre(movies):
    """
    Function that grabs all the genre type for future tree structure
    returns a word list of genres.
    """
    genreList = []
    for item in movies:
        if(isinstance(item.Genre, list)):
            for eachG in item.Genre:
                if(eachG not in genreList):
                    genreList.append(eachG)
        else:
            if(item.Genre not in genreList):
                    genreList.append(item.Genre)           
    return genreList
        
def constructTree(movies, genreList):
    """
    Function will construct the data table into a tree for retrieving information
    parameter1: list of movie objects
    parameter2: list of grenres
    returns a tree of data.
    """
    tree = {}
    for genre in genreList:
        for movie in movies:
            if(isinstance(movie.Genre , list)):
                if(genre in movie.Genre):
                    if genre in tree:
                        movieData = tree[genre]
                    else:
                        movieData = {}
                    movieData[movie.MovieName] = {'URL': movie.TicketURL, 'PG':movie.PGRate, 'Description':movie.MovieDescription}
                    tree[genre] = movieData
            if(movie.Genre == genre):
                if genre in tree:
                    movieData = tree[genre]
                else:
                    movieData = {}
                movieData[movie.MovieName] = {'URL': movie.TicketURL, 'PG':movie.PGRate, 'Description':movie.MovieDescription}
                tree[genre] = movieData
    return tree
def printMovies(gengreChose, tree):
    data = []
    count = 1
    for key in tree:
        longtext =  tree[key]['Description'].split()
        grouped_words = [' '.join(longtext[i: i + 10]) for i in range(0, len(longtext), 10)]
        des = '\n'.join(grouped_words)
        data.append([count, key, tree[key]['PG'], des]) 
        count += 1
    print(tabulate(data, headers=["Movie Index", "Movie Name","Movie PG", "Movie Description"], tablefmt="fancy_grid"))
    while(True):
        choice = input("Please pick a movie and I will redirect you to the movie page. If none of the movie interest you , type quit or back to chose a different gengre: ")
        if(choice.lower() == 'back'):
            return True
        elif(choice.lower() == 'quit'):
            return False



def drawPieChart(tree):
    df = px.data.tips()
    value = []
    names = []
    counter = 1
    for key in tree:
        namestr = "{}. {}".format(counter, key)
        value.append(len(tree[key]))
        names.append(namestr)
        counter += 1
    fig = px.pie(values= value, names=names)
    fig.show()
    ans = num("Please pick a number for the gengre that you are interest in. ", 1, len(value))
    for name in names:
        namedata = name.split('.')
        if( namedata[0] == str(ans)):
            return namedata[1].strip()

def yes(prompt):
    """ returns a boolean
    Check whether the node is a answer.
    Return true if the answer is yes.
    Return false if the answer is no.
    """
    yesList = ['yes','yep','sure', 'y']
    noList = ['nop','no','not','n']
    while(True):
        answer = input(prompt).lower()
        if(answer in yesList):
            return True
        elif (answer in noList):
            return False
        else:
            print("Please enter a yes or no answer.\n")

def num(prompt, min, max):
    while(True):
        try:
            answer = int(input(prompt).lower())
            if(answer < min or answer > max):
                print("Please enter a valid number between {} and {}".format(min,max))
            else:
                return answer
        except:
            print("Please enter a valid number between {} and {}".format(min,max))

def interaction(tree):
    while(True):
        gengreChose = drawPieChart(tree)
        print("Here are the movies associate with the the gengre you picked: ")
        if(printMovies(gengreChose, tree[gengreChose])):
            continue;
        else:
            return False
    return ""

def main():
    MOVIE_CACHE = open_cache()
    popularMoviedata = get_popular_movie(MOVIE_CACHE)
    recentMoviedata = get_recent_movie(MOVIE_CACHE)
    recentGengre = getGenre(recentMoviedata)
    popularGengre = getGenre(popularMoviedata)
    recentTree = constructTree(recentMoviedata, recentGengre)
    popularTree = constructTree(popularMoviedata, popularGengre)

    while(True):
        if(yes("Do you want to view the recent movies by gengre? ")):
            interaction(recentTree)
        elif(yes("Do you want to view the Top 250 popular movies by gengre? ")):
            if(interaction(popularTree)):
                break;
        if(yes("Would you like to quit? ")):
            break;






if __name__ == "__main__":
    main()



