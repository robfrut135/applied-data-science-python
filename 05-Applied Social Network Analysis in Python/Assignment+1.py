
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 1 - Creating and Manipulating Graphs
# 
# Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file `Employee_Movie_Choices.txt`.
# 
# A second file, `Employee_Relationships.txt`, has data on the relationships between different coworkers. 
# 
# The relationship score has value of `-100` (Enemies) to `+100` (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.
# 
# Both files are tab delimited.

# In[1]:

import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite


# This is the set of employees
employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])


# you can use the following function to plot graphs
# make sure to comment it out before submitting to the autograder
def plot_graph(G, weight_name=None):
    '''
    G: a networkx G
    weight_name: name of the attribute for plotting edge weights (if G is weighted)
    '''
    get_ipython().magic('matplotlib notebook')
    import matplotlib.pyplot as plt
    
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None
    
    if weight_name:
        weights = [int(G[u][v][weight_name]) for u,v in edges]
        labels = nx.get_edge_attributes(G,weight_name)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights);
    else:
        nx.draw_networkx(G, pos, edges=edges);


# ### Question 1
# 
# Using NetworkX, load in the bipartite graph from `Employee_Movie_Choices.txt` and return that graph.
# 
# *This function should return a networkx graph with 19 nodes and 24 edges*

# In[52]:

def answer_one():
        
    df = pd.read_csv('Employee_Movie_Choices.txt', sep='\t', names=['Employee', 'Movie'])[1:]

    G = nx.Graph()
    G.add_nodes_from(list(df["Employee"].unique()), bipartite=0) #label one
    G.add_nodes_from(list(df["Movie"].unique()), bipartite=1)
    G.add_edges_from([tuple(x) for x in df.to_records(index=False)])
    
    return G

#plot_graph(answer_one())


# ### Question 2
# 
# Using the graph from the previous question, add nodes attributes named `'type'` where movies have the value `'movie'` and employees have the value `'employee'` and return that graph.
# 
# *This function should return a networkx graph with node attributes `{'type': 'movie'}` or `{'type': 'employee'}`*

# In[61]:

def answer_two():
    df = pd.read_csv('Employee_Movie_Choices.txt', sep='\t', names=['Employee', 'Movie'])[1:]
    
    G = nx.Graph()
    G.add_nodes_from(list(df["Employee"].unique()), bipartite=0, type='movie') 
    G.add_nodes_from(list(df["Movie"].unique()), bipartite=1, type='employee')
    G.add_edges_from([tuple(x) for x in df.to_records(index=False)])
        
    return G

#answer_two().nodes(data=True)


# ### Question 3
# 
# Find a weighted projection of the graph from `answer_two` which tells us how many movies different pairs of employees have in common.
# 
# *This function should return a weighted projected graph.*

# In[66]:

def answer_three():
    df = pd.read_csv('Employee_Movie_Choices.txt', sep='\t', names=['Employee', 'Movie'])[1:]    
    
    G = answer_two()
    
    X = set(list(df["Employee"].unique()))
    P = bipartite.weighted_projected_graph(G, X)
    
    return P

#plot_graph(answer_three())


# ### Question 4
# 
# Suppose you'd like to find out if people that have a high relationship score also like the same types of movies.
# 
# Find the Pearson correlation ( using `DataFrame.corr()` ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in common it should be treated as a 0, not a missing value, and should be included in the correlation calculation.
# 
# *This function should return a float.*

# In[123]:

def answer_four():
            
    df_r = pd.read_csv('Employee_Relationships.txt', sep='\t', names=['EmployeeA', 'EmployeeB', 'Score'])
    df_r.set_index(['EmployeeA', 'EmployeeB'], inplace=True)
    
    G = answer_three()
    
    df_s_ini = pd.DataFrame(G.edges(data=True), columns=["EmployeeA","EmployeeB","Weight"])
    df_s_ini['Weight'] = df_s_ini['Weight'].map(lambda x: x['weight'])

    df_s_copy = df_s_ini.copy()
    df_s_copy.rename(columns={"EmployeeA":"A", "EmployeeB":"EmployeeA"}, inplace=True)
    df_s_copy.rename(columns={"A":"EmployeeB"}, inplace=True)    
    
    df_s = pd.concat([df_s_ini, df_s_copy])
    df_s.set_index(['EmployeeA', 'EmployeeB'], inplace=True)    
    
    df = pd.merge(df_r, df_s, how='left',left_index=True, right_index=True)
    df["Weight"].fillna(value=0, inplace=True)
    
    return df['Weight'].corr(df['Score'])

#answer_four()

