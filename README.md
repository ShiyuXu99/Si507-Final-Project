# Si507-Final-Project

## Description of how to run the program:
Simply run the file named movie_tracker in your terminal, and the program will prompt you to choose from viewing recent movies on AMC or 250 most famous movies from your terminal. Then you can follow the printed instructions and chose the movies you are interested in, and you will be redirected to the movie's web page.


### Packages needed to be downloaded and instructions:
`pip install requests`
`pip install beautifulsoup4` or `pip3 install beautifulsoup4`
`pip install plotly` or `pip3 install plotly`
`pip install tabulate` or `pip3 install tabulate`

API used:
OMDb API: https://www.omdbapi.com
API Key: 2a79e05ccbae6651cc86911773917142
Other websites used (with multiple pages not listed):
https://www.amctheatres.com
https://www.imdb.com


Link to github repo for your final project code
A README containing any special instructions for running your code (e.g., how to supply API
keys) as well as a brief description of how to interact with your program.
Any required Python packages for your project to work (e.g., requests, flask). You do not need
to name built-in packages (e.g., random, json)


### Data Structure
I’m using a tree structure to organize my data. I constructed two trees with a similar structure for the movie information that is on display right now, and the tree that stores information for popular movies. Prior to constructing the tree, I filtered all the genres of the movie into a list, and the first layer of the tree will be the different genres of the movies, for example, action movies, comedy, animation, and so on. The second layer of the tree will be the suggested movie names grouped by genre, and the third layer, the leaf layer will be movie descriptions, the PG of the movie, and links to where the movie ticket can be bought or where to watch the movie. The tree is stored in a dictionary, and each tree node is also consisting of a dictionary. A simple example of the tree will be:
{{comedy: {'Turning Red': {'URL: 'URL Here', 'PG': 'PG 13'}, {'How to train your dragon': {'URL: 'URL Here', 'PG': 'PG 13'}}, {Action movies: {...}}}

Construct tree python file: `build_tree.py`
JSON file with tree: `tree_data.json`
Read info python file: `read_tree.py`

