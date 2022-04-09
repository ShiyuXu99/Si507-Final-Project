import requests
from bs4 import BeautifulSoup
#OMDb API: http://www.omdbapi.com/?i=tt3896198&apikey=c5eb6c3c
#API Key: 2a79e05ccbae6651cc86911773917142

def get_movie_info_fromWeb(movie):
    req = requests.get(movie.TicketURL)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        movie.PGRate = soup.find(attrs={'itemprop': 'contentRating' }).get_text()
    except:
        print(movie.TicketURL)
    movie.MovieDescription = soup.find('p',class_='show-text').get_text()
    movie.Genre = soup.find(attrs={'itemprop': 'genre' }).get_text()


def get_recent_movie():
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
        try:
            releaseDate = item.find("span", class_="MoviePosters__released-month clearfix").get_text()
            releaseDate = " ".join(releaseDate.split()[1:])
        except:
            continue
        movieObject = Movie()
        movieObject.MovieYear = releaseDate[-4:]
        movieObject.MovieName = item.find("h3").string
        movieObject.TicketURL = "https://www.amctheatres.com" + item.a['href']
        get_movie_info_fromWeb(movieObject)
        allMovies.append(movieObject)
    return allMovies

def get_popular_movie():
    popularMovie = []
    count = 0
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    data = soup.find_all("td", class_="titleColumn")
    for item in data:
        movie = Movie()
        movie.TicketURL = 'https://www.imdb.com' + item.a['href']
        itemData = item.get_text().strip().split('\n')
        movie.MovieName = itemData[1].lstrip()
        movie.MovieYear = itemData[-1][1:5]
        get_popular_movie_info(movie)
        popularMovie.append(movie)
        count += 1
        if(count > 10):
            break;
    return popularMovie


def get_popular_movie_info(movie):
    params = {'t':movie.MovieName, 'y': movie.MovieYear, 'plot':'full'}
    try:
        response = requests.get('http://www.omdbapi.com/?apikey=c5eb6c3c',params=params)
        movieData = response.json()
        movie.MovieDescription = movieData['Plot']
        movie.PGRate = movieData['Rated']
        movie.Genre = movieData['Genre'].split(',')
        movie.MovieRating = movieData['imdbRating']
    except:
        print("Some data might be missing.")
    pass

class Movie:
    def __init__(self):
        self.MovieName = ''
        self.TicketURL = ''
        self.Genre = ''
        self.PGRate = ''
        self.MovieDescription = ''
        self.MovieRating = ''
        self.MovieYear = ''

def get_movie_info(movie):
    params = {'t':movie.MovieName, 'y': movie.MovieYear, 'plot':'full'}
    try:
        response = requests.get('http://www.omdbapi.com/?apikey=c5eb6c3c',params=params)
        movieData = response.json()
        movie.MovieDescription = movieData['Plot']
        movie.PGRate = movieData['Rated']
        movie.Genre = movieData['Genre']
        movie.MovieRating = movieData['Ratings']
    except:
        print("hi")
    pass

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
                    genreList.append(item.Genre)
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
            if(movie.Genre == genre):
                if genre in tree:
                    movieData = tree[genre]
                else:
                    movieData = {}
                movieData[movie.MovieName] = {'URL': movie.TicketURL, 'PG':movie.PGRate, 'Description':movie.MovieDescription}
                tree[genre] = movieData
    return tree



def main():
    data = get_recent_movie()
    tree = constructTree(data, getGenre(data))


    


if __name__ == "__main__":
    main()



