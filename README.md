# RockRankAnalyisis
An Analysis on the top 100 rock bands of all time, according to BusinessInsider

I first scraped Business Insider's article found here: https://www.businessinsider.com/the-100-most-popular-rock-bands-of-all-time-2018-9

Once I had a list of the "top 100 rock bands", I used the GeniusLyrics API to obtain the top 25 songs for the top 10 bands, then ranked them on unique vocabulary (the number of unique words used in their 25 most popular songs.


<img width="371" alt="Screen Shot 2022-01-02 at 5 37 47 PM" src="https://user-images.githubusercontent.com/58821846/147891502-5456d66a-d68b-49f7-893b-ef241116f436.png">


I then used the spotipy API to compare the BusinessInsider rank to the popularity on spotify:

<img width="562" alt="Screen Shot 2022-01-02 at 5 37 37 PM" src="https://user-images.githubusercontent.com/58821846/147891511-f87fc5f7-35ff-4259-8314-8681af7b200f.png">

Seems to me like the more recent bands are punching above their weight in the popularity category!

The most popular "unique words" are also attached in the file. However, due to the nature of genuius lyric format, the words such as chorus, or band member names may be present as headers within the lyrics and therefore are included within the analysis.
