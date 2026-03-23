# Graph Connectivity and DFS Spanning Tree Analyzer

A Python application that determines whether an undirected graph is **connected** and generates a **Depth-First Search (DFS) spanning tree** from any chosen starting vertex. For disconnected graphs it automatically identifies every connected component and visualizes a spanning tree for each one.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Algorithm Overview](#algorithm-overview)
  - [Graph Representation](#graph-representation)
  - [Depth-First Search (DFS)](#depth-first-search-dfs)
  - [Connectivity Check](#connectivity-check)
  - [Spanning Tree Construction](#spanning-tree-construction)
  - [Spanning Forest for Disconnected Graphs](#spanning-forest-for-disconnected-graphs)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Input Format](#input-format)
- [Usage](#usage)
- [Output](#output)
- [Example Walkthroughs](#example-walkthroughs)
  - [Connected Graph](#connected-graph)
  - [Disconnected Graph](#disconnected-graph)
- [Limitations and Future Work](#limitations-and-future-work)

---

## Problem Statement

In graph theory, several fundamental questions arise when analyzing a network:

1. **Is the graph connected?** — Can every vertex be reached from every other vertex by following edges?
2. **What is the spanning tree?** — What is the minimal set of edges that keeps all vertices reachable from a starting point (i.e., a tree that spans every vertex)?
3. **Does the spanning tree change with the starting vertex?** — Yes. Different starting vertices explore neighbors in different orders, producing different DFS trees even on the same graph.
4. **What about disconnected graphs?** — A spanning tree cannot cross the gap between disconnected components. Instead, a **spanning forest** is built — one spanning tree per connected component.

These questions appear throughout computer science and engineering:
- Network routing (e.g., ensuring all computers in a network can communicate)
- Circuit analysis (e.g., finding minimal wiring paths)
- Social network analysis (e.g., determining whether a group is fully connected)

This project addresses all four questions by:
- Accepting a simple edge-list description of an undirected graph from a text file
- Asking the user which vertex to start DFS from (any vertex is valid)
- Performing an **iterative DFS traversal** from that vertex
- Reporting whether the graph is **connected** or **disconnected**
- If connected: extracting and visualizing the **DFS spanning tree** from the chosen vertex
- If disconnected: computing a **spanning forest** — finding and visualizing a spanning tree for **each** connected component
- Saving PNG visualizations of the original graph and all spanning trees

---

## Algorithm Overview

### Graph Representation

Edges are read from `data.txt` and stored as an **adjacency list** — a list of lists where index `i` holds the neighbors of vertex `i`. This representation is memory-efficient for sparse graphs and provides O(degree) neighbor lookups.

```
Example edges: (1,2), (1,3), (2,4)

Adjacency list:
  1 → [2, 3]
  2 → [1, 4]
  3 → [1]
  4 → [2]
```

### Depth-First Search (DFS)

The DFS implementation is **iterative** (not recursive), which avoids Python's recursion limit for large graphs. It uses a **precedence (parent) array** `prec` to record, for each vertex `v`, which vertex it was first visited from.

**Algorithm steps:**

1. Initialize `prec[start] = start` and set the current vertex `curr = start`.
2. Look at the neighbors of `curr`.  
   - If an unvisited neighbor `val` is found (`prec[val] == 0`), set `prec[val] = curr`, move to `val`, and restart the neighbor scan.
   - If no unvisited neighbor exists, **backtrack**: set `curr = prec[curr]`.
3. Terminate when `curr` returns to `start` with no unvisited neighbors remaining.

**Time complexity:** O(V + E) — each vertex and edge is processed at most once.

The function accepts an optional shared `prec` array so it can be called incrementally when building a spanning forest.

### Connectivity Check

After DFS completes, the `prec` array is inspected:
- If any entry `prec[v] == 0` for `v ≠ start`, vertex `v` was never visited, meaning the graph is **disconnected**.
- If all entries are non-zero, every vertex was reached — the graph is **connected**.

### Spanning Tree Construction

The spanning tree edges are derived directly from the `prec` array:
- For every vertex `v` where `prec[v] ≠ v` **and** `prec[v] ≠ 0`, the edge `(prec[v], v)` is a tree edge.
- These edges form a tree that connects all vertices using exactly `V − 1` edges.

### Spanning Forest for Disconnected Graphs

When the graph is disconnected, a single DFS cannot reach all vertices. The `spanning_forest` function extends DFS to cover every component:

1. Run DFS from the user-chosen starting vertex `start`, filling `prec` for all reachable vertices.
2. Scan vertices 1 to V; for each vertex `v` still unvisited (`prec[v] == 0`), run DFS from `v` using the **same shared `prec` array**.
3. Repeat until all vertices are assigned a parent.

After this, every vertex `v` where `prec[v] == v` is the **root** of one connected component. A fresh single-component DFS from each root then provides its individual spanning tree for display.

**Observation:** changing the starting vertex affects which component is explored first and which vertex acts as root in its component's spanning tree — two runs with different starting vertices may produce visually different forests.

---

## Project Structure

```
Technological-Project/
├── Main.py       # Core logic: DFS, spanning forest, connectivity check, spanning tree extraction
├── Display.py    # Graph visualization using NetworkX and Matplotlib
├── data.txt      # Input file containing graph edges (one edge per line)
└── README.md     # Project documentation
```

| File | Responsibility |
|------|----------------|
| `Main.py` | Reads input, builds adjacency list, prompts for start vertex, runs DFS / spanning forest, checks connectivity, extracts spanning trees, coordinates visualization |
| `Display.py` | Renders any edge list as a labeled graph image and saves it as a PNG file |
| `data.txt` | User-supplied graph description in edge-list format |

---

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| `matplotlib` | ≥ 3.0 | Plotting and saving graph images |
| `networkx` | ≥ 2.0 | Graph data structure and spring-layout positioning |

Both are installable via `pip` (see [Installation](#installation)).

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Smuthusivam/Technological-Project.git
   cd Technological-Project
   ```

2. **Create and activate a virtual environment** *(recommended)*

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install matplotlib networkx
   ```

---

## Input Format

Edit `data.txt` to describe your graph. Each line represents one **undirected edge** as two space-separated vertex numbers:

```
<vertex_a> <vertex_b>
```

**Rules:**
- Vertices are identified by positive integers (1-indexed, consecutive from 1).
- The number of vertices `V` is inferred automatically as the count of distinct vertex labels appearing in the file.
- Duplicate edges and self-loops are not explicitly filtered; avoid them for correct results.
- The file must contain at least one edge.

**Example — connected graph (`data.txt`):**

```
1 2
1 3
2 4
```

```
    1
   / \
  2   3
  |
  4
```

**Example — disconnected graph (`data.txt`):**

```
1 2
1 3
4 5
```

```
    1       4
   / \      |
  2   3     5
```

---

## Usage

Run the main script from the project directory:

```bash
python Main.py
```

The script will:
1. Delete any previously generated `*.png` files in the current directory.
2. Read edges from `data.txt` and print the edge list, vertex count, and adjacency list.
3. **Prompt you to enter a starting vertex** (any integer from 1 to V).
4. Run DFS from that vertex and check connectivity.
5. Save `Original Graph.png` — a visualization of the input graph.
6. **If connected:** print the spanning tree edges and save `Tree from vertex (N).png`.
7. **If disconnected:** identify all components, print and save a spanning tree PNG for each one.

---

## Output

### Terminal output — connected graph (start vertex 1)

```
The edges are [[1, 2], [1, 3], [2, 4]]
Number of vertices: 4
1: [2, 3]
2: [1, 4]
3: [1]
4: [2]
Enter starting vertex (1 to 4): 1
Prec: [1, 1, 1, 2]
The graph is connected.
Tree Edges from vertex - 1:
 [[1, 2], [1, 3], [2, 4]]
```

### Terminal output — connected graph (start vertex 3, different tree shape)

```
Enter starting vertex (1 to 4): 3
Prec: [3, 1, 3, 2]
The graph is connected.
Tree Edges from vertex - 3:
 [[1, 2], [1, 3], [2, 4]]
```

### Terminal output — disconnected graph (start vertex 1)

```
The edges are [[1, 2], [1, 3], [4, 5]]
Number of vertices: 5
...
Enter starting vertex (1 to 5): 1
Prec: [1, 1, 1, 0, 0]
Graph is disconnected
Finding spanning trees for each connected component...
Number of connected components: 2
Spanning tree of component starting at vertex 1: [[1, 2], [1, 3]]
Spanning tree of component starting at vertex 4: [[4, 5]]
```

### PNG files

| File | Contents |
|------|---------|
| `Original Graph.png` | Spring-layout visualization of all input edges |
| `Tree from vertex (N).png` | Spanning tree of the component whose DFS started at vertex N (one file per component) |

Node labels are drawn inside light-blue circles; edges are rendered in gray.

---

## Example Walkthroughs

### Connected Graph

Using `data.txt`:
```
1 2
1 3
2 4
```

**DFS trace from vertex 1:**

| Step | Current | Action | `prec` (indices 1–4) |
|------|---------|--------|----------------------|
| Init | 1 | Mark prec[1]=1 | [1, 0, 0, 0] |
| 1 | 1 | Visit neighbor 2, prec[2]=1 | [1, 1, 0, 0] |
| 2 | 2 | Visit neighbor 4, prec[4]=2 | [1, 1, 0, 2] |
| 3 | 4 | No unvisited neighbors → backtrack to 2 | [1, 1, 0, 2] |
| 4 | 2 | No unvisited neighbors → backtrack to 1 | [1, 1, 0, 2] |
| 5 | 1 | Visit neighbor 3, prec[3]=1 | [1, 1, 1, 2] |
| 6 | 3 | No unvisited neighbors → backtrack to 1 | [1, 1, 1, 2] |
| 7 | 1 | No unvisited neighbors, at start → stop | [1, 1, 1, 2] |

`prec = [1, 1, 1, 2]` — no zeros → **connected**. Spanning tree: `[[1,2], [1,3], [2,4]]`.

**DFS trace from vertex 3** (same graph, different root):

`prec = [3, 1, 3, 2]` — root is 3, vertex 1's parent is 3, vertex 4's parent is 2. The tree edges `[[1,3], [1,2], [2,4]]` represent the same edges but a different conceptual rooting.

### Disconnected Graph

Using `data.txt`:
```
1 2
1 3
4 5
```

**DFS from vertex 1:** visits {1, 2, 3}. `prec = [1, 1, 1, 0, 0]`.

Zeros detected → **disconnected**. `spanning_forest` continues from vertex 4 (first unvisited): visits {4, 5}.

Full `prec_forest = [1, 1, 1, 4, 4]`. Component roots (where `prec[v]==v`): vertices **1** and **4**.

| Component root | Spanning tree |
|---------------|---------------|
| 1 | `[[1,2], [1,3]]` |
| 4 | `[[4,5]]` |

Two PNG files are produced, one per component.

---

## Limitations and Future Work

| Limitation | Potential Improvement |
|------------|----------------------|
| No error handling for malformed `data.txt` | Add input validation with informative error messages |
| Vertices must be labeled 1 to V consecutively | Support arbitrary integer vertex labels |
| Only undirected graphs are supported | Extend to directed graphs (digraphs) |
| Graph must be described in a plain-text file | Add support for interactive input or standard input (`stdin`) |
| Minor typo in `adjacet_matrix` function name (`adjacet` instead of `adjacency`) | Rename to `adjacency_list` in a future refactor |

