import Display as dp
import os
import glob

#Function to create the tree edges 
def tree_edges(prec,V):
    tree=[]
    for i in range(1,V+1):
        if prec[i] !=i:
            lst=[prec[i],i]
            lst.sort()
            tree.append(lst)
            tree.sort()
    return tree


#Function to get the input from text file and find vertices
def text_inp():
    edges=[]
    vertices=[]
    file=open("data.txt")
    for line in file:
        a,b=line.strip().split(' ')
        if a not in vertices:
            vertices.append(a)
        if b not in vertices:
            vertices.append(b)
        lst=[int(a),int(b)]
        lst.sort()
        edges.append(lst)
    file.close()
    return edges,len(vertices)

#Function to create the adjacency matrix
def adjacet_matrix(edges,V):
    adj = [[] for _ in range(V+1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

# DFS algorithm Function 
def dfs(adj,start,V):
    prec=[0]*(V+1)
    prec[start]=start
    curr=start
    nr=[0]*(V+1)
    nr[start]=1
    i=0
    while True:
        neigbours=adj[curr]
        for val in neigbours:
            # Detecting back edge
            if prec[val]!=0 and prec[curr]!=val and nr[curr] > nr[val]:
                 print(f"back edge: ({val},{curr})")
            
            if prec[val]==0:
                prec[val]=curr
                nr[val]=i+1
                i=nr[val]
                curr=val
                break
        else:   
            if curr==start:
                break
            else:
                curr=prec[curr]
    return prec

def compare(tree_All):
    G=[]
    for i in range(len(tree_All)):
        val=[]
        val.append(i+1)
        for j in range(len(tree_All)):
            if i!=j:
                if tree_All[i]==tree_All[j]:
                    val.append(j+1)
        val.sort()
        if val not in G and len(val)>1:
            G.append(val)
    return G

#Main Method
if __name__ == "__main__":

    for old_file in glob.glob("*.png"):   
        os.remove(old_file)

    edges,V=text_inp()
    dp.plot_graph(edges,"Original Graph")

    print(f"The edges are{edges}")
    print(f"Number of vertices:{V}")

    adj=adjacet_matrix(edges,V)

    for i in range(1,len(adj)):
        print(f"{i}:{adj[i]}")


    start=1
    prec=dfs(adj,start,V)
    print(f"Prec:{prec[1:]}")

    if 0 in prec[1:]:
        print("Graph is disconnected")
    else:
        tree=tree_edges(prec,V)
        print("The graph is connected.")
        print(f"Tree Edges from vertex - {start}: \n {tree}")
        dp.plot_graph(tree, f" Tree from vertex ({start})")
    

   
