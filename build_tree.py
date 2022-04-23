
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