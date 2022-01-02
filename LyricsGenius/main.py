import lyricsgenius
from bs4 import BeautifulSoup
import requests
import pandas as pd
import spotipy
from pathlib import Path
from collections import Counter
import re
import os.path
from requests.exceptions import Timeout


SPOTIFY_CLIENT_ID = 'SECRET'
SPOTIFY_CLIENT_SECRET = 'SECRET'
SPOTIFY_CLIENT_URI = "https://google.com"
GENIUS_ACCESS_TOKEN = 'SECRET'

# scope = 'user-read-currently-playing'

oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID
,client_secret=SPOTIFY_CLIENT_SECRET
,redirect_uri=SPOTIFY_CLIENT_URI
# ,scope=scope
)
tokenDict = oauth_object.get_access_token()
token = tokenDict['access_token']

url = "https://www.businessinsider.com/the-100-most-popular-rock-bands-of-all-time-2018-9"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
scraped_bands = soup.find_all('h2', class_="slide-title-text")


bands = []
for band in scraped_bands:
  b = ""
  band = band.get_text()
  i = 0
  for l in band:
    i+=1
    if l == "1" or l=="2" or l=="3" or l=="4" or l=="5" or l=="6" or l=="7" or l=="8" or l=="9" or l=="0" or l==".":
      if (i<=3):
        pass
      else:
        b+=l
    else:
      b += l
  #appends everything but first char
  bands.append(b[1:])
#flip the list so the most popular bands are first
bands.reverse()
voc_bands = bands[:10]
print(bands)
print(voc_bands)

#initiate Genius
genius_object = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)



#non-significant words
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
             'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
             'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
             'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
             'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
             'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
             'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
             'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
             'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 've', 'll', 'amp']


  
def split_into_words(any_chunk_of_text):
    lowercase_text = any_chunk_of_text.lower()
    split_words = re.split("\W+", lowercase_text)
    return split_words 

def get_most_frequent_words_directory(directory_path, band):
    
    number_of_desired_words = 20
    meaningful_words_tally = Counter()
    tot_words = set()
    
    for filepath in Path(directory_path).glob('*.txt'):
            if(band in filepath.name):
              full_text = open(filepath, encoding="utf-8").read()
              all_the_words = split_into_words(full_text)
              for word in all_the_words:
                tot_words.add(word)
              meaningful_words = [word for word in all_the_words if word not in stopwords]
              meaningful_words_tally.update(meaningful_words)
            elif(("ACDC" in filepath.name) or ("Guns N Roses" in filepath.name)):
              full_text = open(filepath, encoding="utf-8").read()
              all_the_words = split_into_words(full_text)
              for word in all_the_words:
                tot_words.add(word)
              meaningful_words = [word for word in all_the_words if word not in stopwords]
              meaningful_words_tally.update(meaningful_words)
              
    most_frequent_meaningful_words = meaningful_words_tally.most_common(number_of_desired_words)

    return most_frequent_meaningful_words, tot_words


#For getting the vocabulary
vocab = []
for band in voc_bands:
  print(band)
  artist = genius_object.search_artist(band, 
  max_songs=25)
  numwords = set()
  for song in artist.songs:
      song.save_lyrics(filename = band+ " " + song.title, overwrite=True, extension='txt')
  
  frequencies, numwords = get_most_frequent_words_directory("/Users/lukelorenz/Desktop/IndependentProjects/LyricsGenius/", band)
  # Make Counter dictionary into a Pandas DataFrame
  word_frequency_df = pd.DataFrame(frequencies, columns=['word', 'word_count'])
  # Plot word counts
  # word_frequency_df.sort_values(by='word_count').plot(x='word', kind='barh', title="beatles:\n Most Frequent Words in Top 10 Songs")
  if(band == "AC/DC"):
    word_frequency_df.to_csv("IMPORTANTWORDS " + "ACDC")
    print(frequencies)
  else:
    word_frequency_df.to_csv("IMPORTANTWORDS " + band)
  
  print(band + " Used : " + str(len(numwords)) + " unique words in their top 10 songs")
  vocab.append(len(numwords))
  print(vocab)
print("DONE")
print(vocab)
    
directory_path = '/Users/lukelorenz/Desktop/IndependentProjects/LyricsGenius/'
for file in Path(directory_path).glob('*.txt'):
    print(file)


#initiate Spotipy
sp = spotipy.Spotify(auth=token)

rating = []
for band in bands:
  result = sp.search(q=band, type="artist")
  rating.append(result['artists']['items'][0]['popularity'])
  print(band)
  print(result['artists']['items'][0]['popularity'])
  
rank = []
for i in range (100):
  rank.append(i+1)

print(rank)

data = pd.DataFrame()
data['Bands'] = bands
data['Rank'] = rank
data['Popularity Rating'] = rating

vocabulary = pd.DataFrame()
vocabulary['Bands'] = voc_bands
vocabulary['Vocabulary'] = vocab

print(data)
data = data.sort_values('Popularity Rating',ascending=False)
print(data)

print("PRINTING VOCAB")
print(vocabulary)
vocabulary = vocabulary.sort_values('Vocabulary', ascending=False)
print(vocabulary)
data.to_csv("RockRanked", index=False)
