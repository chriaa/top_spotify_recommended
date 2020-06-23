import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests


endpoint = "https://accounts.spotify.com/authorize"

param = {
    "client_id" : "",
    "client_secret" : "",
    "response_type" : "code",
    "redirect_uri" : "http://localhost:8888/callback",
    "scopes" : "user-top-read"

}

#SORT THE LIST BY MOST LISTENED TO TO LEASET
def mergesort(a):
    if len(a) > 1:
        middle = int(len(a)/2)

        left = a[:middle]
        right = a[middle:]

        mergesort(left)
        mergesort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i][1] > right[j][1]:
                a[k] = left[i]
                i+=1
            else:
                a[k] = right[j]
                j+=1
            k+=1


        while i < len(left):
            a[k] = left[i]
            i+= 1
            k+= 1

        while j < len(right):
            a[k] = right[j]
            j+= 1
            k+= 1



#GETS TOP USER ARTISTS AND TOP RECCOMMENDED ARTISTS OF THE USER
def get_relations(token):

    if token:
        sp = spotipy.Spotify(token)
        result = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')


        source = []
        for i in result['items']:
            source.append(i)

        all_artists = {} #the dictionary of artists that have already been found and the count of how many times theyve been seen
        related_artists = {}

        for artist in result['items']:
            #get the related artist of every artist
            related = sp.artist_related_artists(artist['id'])

            rel = []
            for x in related['artists']:


                rel.append(x['name'])
                if x['id'] in all_artists: #if a related artist is already in the list then increment the times it has been seen
                    all_artists[x['id']] += 1
                else:
                    if x['id'] not in source: #otherwise, as long as it is an artist not in results, add it to the dictionary
                        all_artists[x['id']] = 1

            related_artists[artist['name']] = rel



        #Sorting the most reccommended by least to greatest
        collection = list(all_artists.items())
        mergesort(collection)


        x = 0
        b = 2
        while(collection[x][1] > b):
            collection[x] = [sp.artist(collection[x][0])['name'], collection[x][1]]#, collection[x][1])
            x+=1

        collection = collection[0:x]



        return collection, related_artists
