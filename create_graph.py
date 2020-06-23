import networkx as nx
from get_artists import *
from pyvis.network import Network
from pyvis.options import Layout
import numpy as np
import json
import pandas as pd

#SETS ATTRIBUTES OF THE TOP 5 MOST LISTENED TO GROUP OF RELATED ARTISTS
def set_node_attributes(Graph, most_related_artists, edges):
    d = []
    get_most_related(d, most_related_artists)

    u = 0

    #set attributes of all most seen related nodes
    colors = ["#7E3F8F", "#81559B", "#8C86AA", "#B2EF9B", "DAFF7D"]
    sizes = [70, 65, 60, 55, 50 ]
    for x in d:
        for y in x[1]:
            Graph.nodes[y]['color'] = colors[u]
            Graph.nodes[y]['size'] = sizes[u]
            #Graph.nodes[y]['shape'] = "circle"
            Graph.nodes[y]['title'] = y

        u+=1

    #set attributes of source nodes
    for x in edges:
        print(x)
        Graph.nodes[x]['color'] = "#99E1D9"
        Graph.nodes[x]['size'] = 70
        Graph.nodes[x]['shape'] = "square"
        Graph.nodes[x]['title'] = "Source Artist : "+ x


#ORGANIZES MOST RELATED ARTIST BY GROUPINGS
def get_most_related(d, data):
    #d is a list of artists grouped
    #data[0] = related_list

    r = data[0][1]
    q = []
    #groups artists with the same number of hits together in the list d
    for i in range(0, len(data)):
        #d.append(data[0][i])
        if(data[i][1] != r):
            new_group = [r, q]
            d.append(new_group)
            r = data[i][1]
            q = []
        q.append(data[i][0])
    new_group = [r, q]
    d.append(new_group)
    r = data[i][1]


#CREATES GRAPH BASED ON GIVEN RELATIONS
def get_edges(fr, to, edges):

    seen_nodes = {}
    #gets all source artists and all their related
    for x in edges:

            seen_nodes[x] = 1
            current_from = [x] * len(edges[x])

            fr.extend(current_from)
            to.extend(edges[x])

#PHYSICS OF THE SHOWN GRAPH
def show_network(G):

    nt = Network("700px", "700px",directed = True)
    nt.from_nx(G)


    #UNCOMMENT BELOW TO PLAY WITH PHYSICS OF SHOWN GRAPH
    #nt.show_buttons(filter_=["physics"])
    #nt.show_buttons(filter_=['nodes', 'interaction', 'selection'])
    nt.toggle_physics(status = True)
    nt.force_atlas_2based(gravity = -500, central_gravity = 0.02, damping = 0.2, overlap = 0.5)
    nt.show("Most_Related_Artists.html")


def main():

    fr = []
    to = []
    #USER IS PROMPTED FOR ACCOUNT INFORMATION
    token = util.prompt_for_user_token( 'username', 'user-top-read', param["client_id"], param["client_secret"], param["redirect_uri"])

    #GETS THE MOST RELATED ARTISTS AND ALL RECCOMMENDED ARTIST
    most_related_artists, edges = get_relations(token)


    get_edges(fr, to, edges)


    #CREATE GRAPH AND SETS ATTRIBUTES
    df = pd.DataFrame({'from': fr, 'to': to})
    G = nx.from_pandas_edgelist(df, source = 'from', target = 'to', create_using = nx.DiGraph())

    set_node_attributes(G, most_related_artists, edges)

    show_network(G)



if __name__ == "__main__":


    main()
