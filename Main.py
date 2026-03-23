import Display as dp
import os
import glob

#Function to create the tree edges 
def tree_edges(prec,V):
    tree=[]
    for i in range(1,V+1):
        if prec[i] !=0 and prec[i] !=i:
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
def dfs(adj,start,V,prec=None):
    if prec is None:
        prec=[0]*(V+1)
    prec[start]=start
    curr=start
    while True:
        neigbours=adj[curr]
        for val in neigbours:
            if prec[val]==0:
                prec[val]=curr
                curr=val
                break
        else:   
            if curr==start:
                break
            else:
                curr=prec[curr]
    return prec


#Build a spanning forest: run DFS from start, then from each remaining unvisited vertex
def spanning_forest(adj,start,V):
    prec=dfs(adj,start,V)
    for v in range(1,V+1):
        if prec[v]==0:
            dfs(adj,v,V,prec)
    return prec


#Main Method
if __name__ == "__main__":

    for old_file in glob.glob("*.png"):   
        os.remove(old_file)

    edges,V=text_inp()
    dp.plot_graph(edges,"Original Graph")

    print(f"The edges are {edges}")
    print(f"Number of vertices: {V}")

    adj=adjacet_matrix(edges,V)

    for i in range(1,len(adj)):
        print(f"{i}: {adj[i]}")

    # Ask user which vertex to start DFS from
    start=int(input(f"Enter starting vertex (1 to {V}): "))
    while start < 1 or start > V:
        print(f"Invalid vertex. Please enter a number between 1 and {V}.")
        start=int(input(f"Enter starting vertex (1 to {V}): "))

    prec=dfs(adj,start,V)
    print(f"Prec: {prec[1:]}")

    if 0 in prec[1:]:
        print("Graph is disconnected")
        print("Finding spanning trees for each connected component...")
        prec_forest=spanning_forest(adj,start,V)
        # Component roots are vertices where prec[v] == v
        roots=[v for v in range(1,V+1) if prec_forest[v]==v]
        print(f"Number of connected components: {len(roots)}")
        for root in roots:
            comp_prec=dfs(adj,root,V)
            comp_tree=tree_edges(comp_prec,V)
            print(f"Spanning tree of component starting at vertex {root}: {comp_tree}")
            if comp_tree:
                dp.plot_graph(comp_tree,f"Tree from vertex ({root})")
    else:
        tree=tree_edges(prec,V)
        print("The graph is connected.")
        print(f"Tree Edges from vertex - {start}: \n {tree}")
        dp.plot_graph(tree,f"Tree from vertex ({start})")

