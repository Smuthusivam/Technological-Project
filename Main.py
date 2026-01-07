import Display as dp
import os
import glob

#Function to create the tree edges 
def tree_edges(prec,V):
    tree=[]
    new_tree=[]
    for i in range(1,V+1):
        if prec[i] !=i and prec[i]!=0 :
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
            vertices.append(int(a))
        if b not in vertices:
            vertices.append(int(b))
        lst=[int(a),int(b)]
        lst.sort()
        edges.append(lst)
    vertices=max(vertices)
    file.close()
    return edges,vertices

#Function to create the adjacency matrix
def adjacet_matrix(edges,V):
    adj = [[] for _ in range(V+1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

# DFS algorithm Function 
def dfs(adj,start,V,v_count,prec):
    prec[start]=start
    curr=start
    v_count+=1
    while True:
        neigbours=adj[curr]
        for val in neigbours:
            if prec[val]==0:
                prec[val]=curr
                curr=val
                v_count +=1
                break
        else:   
            if curr==start:
                break
            else:
                curr=prec[curr]
    return prec,v_count

def first(prec):
    for i in range(1,len(prec)):
       if prec[i]==0:
        return i

#Method to print the edges of each connected component tree edges
def connect_comp_tree(V,adj):
    count=1
    vis=[]
    start=1
    prec=[0]*(V+1)
    ls=[]
    while count < V:
        for i in range(V):
            if prec[i]!=0 and i not in vis:
                vis.append(i)
        for i in range(1,len(prec)):
            if prec[i] == 0 and i not in vis:
                prec = [0]*(V+1)
                start = i
                prec,count=dfs(adj, start, V, count, prec)
                tr=tree_edges(prec, V)
                if adj[i]==[]:
                    ls.append([[i,i]])
                else:
                    ls.append(tr)
                break
            
                

    for i in range(len(ls)):
        print(f"tree in Connected Component-{i+1}: {ls[i]}")
        dp.plot_graph(ls[i],f"tree-{i+1}")

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

    #Method to print the edges of each connected component edges
    ls = []
    count = 1
    prec = [0]*(V+1)
    while count<V:
        start=first(prec)
        prec,count=dfs(adj,start,V,count,prec) 
        print(prec,count)
        tree = []
        for i in range(1,len(prec)):
            for val in edges:
                if prec[i]==val[0]or prec[i]==val[1]:
                    tree.append(val)
                    edges.remove(val)
        
        ls.append(tree)
    for i in range(len(ls)):
        adj_tre=adjacet_matrix(ls[i],V)
        print(f"Tree-{i+1}={adj_tre}")

    
   