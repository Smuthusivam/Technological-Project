# Graph Connectivity and DFS Spanning Tree Analyzer

A Python application that determines whether an undirected graph is **connected** and, if so, generates and visualizes a **Depth-First Search (DFS) spanning tree** from a chosen starting vertex.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Algorithm Overview](#algorithm-overview)
  - [Graph Representation](#graph-representation)
  - [Depth-First Search (DFS)](#depth-first-search-dfs)
  - [Connectivity Check](#connectivity-check)
  - [Spanning Tree Construction](#spanning-tree-construction)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Input Format](#input-format)
- [Usage](#usage)
- [Output](#output)
- [Example Walkthrough](#example-walkthrough)
- [Limitations and Future Work](#limitations-and-future-work)

---

## Problem Statement

In graph theory, two fundamental questions arise when analyzing a network:

1. **Is the graph connected?** — Can every vertex be reached from every other vertex by following edges?
2. **What is the spanning tree?** — What is the minimal set of edges that keeps all vertices reachable from a starting point (i.e., a tree that spans every vertex)?

These questions appear throughout computer science and engineering:
- Network routing (e.g., ensuring all computers in a network can communicate)
- Circuit analysis (e.g., finding minimal wiring paths)
- Social network analysis (e.g., determining whether a group is fully connected)

This project addresses both questions by:
- Accepting a simple edge-list description of an undirected graph from a text file
- Performing an **iterative DFS traversal** from vertex `1`
- Reporting whether the graph is **connected** or **disconnected**
- If connected, extracting and visualizing the **DFS spanning tree**
- Saving PNG visualizations of both the original graph and the spanning tree

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

### Connectivity Check

After DFS completes, the `prec` array is inspected:
- If any entry `prec[v] == 0` for `v ≠ start`, vertex `v` was never visited, meaning the graph is **disconnected**.
- If all entries are non-zero, every vertex was reached — the graph is **connected**.

### Spanning Tree Construction

The spanning tree edges are derived directly from the `prec` array:
- For every vertex `v` where `prec[v] ≠ v` (i.e., `v` is not the start vertex), the edge `(prec[v], v)` is a tree edge.
- These edges form a tree that connects all vertices using exactly `V − 1` edges.

---

## Project Structure

```
Technological-Project/
├── Main.py       # Core logic: DFS, connectivity check, spanning tree extraction
├── Display.py    # Graph visualization using NetworkX and Matplotlib
├── data.txt      # Input file containing graph edges (one edge per line)
└── README.md     # Project documentation
```

| File | Responsibility |
|------|----------------|
| `Main.py` | Reads input, builds adjacency list, runs DFS, checks connectivity, extracts spanning tree, coordinates visualization |
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
- Vertices are identified by positive integers (1-indexed).
- The number of vertices `V` is inferred automatically as the count of distinct vertex labels appearing in the file.
- Duplicate edges and self-loops are not explicitly filtered; avoid them for correct results.
- The file must contain at least one edge.

**Example `data.txt`:**

```
1 2
1 3
2 4
```

This describes the graph:

```
    1
   / \
  2   3
  |
  4
```

---

## Usage

Run the main script from the project directory:

```bash
python Main.py
```

The script will:
1. Delete any previously generated `*.png` files in the current directory.
2. Read edges from `data.txt` and display them along with the vertex count and adjacency list in the terminal.
3. Perform DFS from vertex `1`.
4. Check connectivity and display the result in the terminal.
5. Save `Original Graph.png` — a visualization of the input graph.
6. If the graph is connected, save `⎵Tree from vertex (1).png` — a visualization of the DFS spanning tree (the filename starts with a space due to the leading space in the title string in `Main.py`).

---

## Output

### Terminal output (connected graph example)

```
The edges are[[1, 2], [1, 3], [2, 4]]
Number of vertices:4
1:[2, 3]
2:[1, 4]
3:[1]
4:[2]
Prec:[1, 1, 1, 2]
The graph is connected.
Tree Edges from vertex - 1:
 [[1, 2], [1, 3], [2, 4]]
```

### Terminal output (disconnected graph example)

```
The edges are[[1, 2], [3, 4]]
Number of vertices:4
...
Prec:[1, 1, 0, 3]
Graph is disconnected
```

### PNG files

| File | Contents |
|------|---------|
| `Original Graph.png` | Spring-layout visualization of all input edges |
| `&nbsp;Tree from vertex (1).png` | Spring-layout visualization of the DFS spanning tree (only generated when the graph is connected). Note: the filename begins with a space character because the title string in `Main.py` contains a leading space. |

Node labels are drawn inside light-blue circles; edges are rendered in gray.

---

## Example Walkthrough

Using the default `data.txt`:

```
1 2
1 3
2 4
```

**Step 1 — Build adjacency list:**

```
1 → [2, 3]
2 → [1, 4]
3 → [1]
4 → [2]
```

**Step 2 — Run DFS from vertex 1:**

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

**Step 3 — Check connectivity:**

`prec = [1, 1, 1, 2]` — no zeros → **graph is connected**.

**Step 4 — Extract spanning tree edges:**

| Vertex `v` | `prec[v]` | Edge |
|-----------|-----------|------|
| 2 | 1 | (1, 2) |
| 3 | 1 | (1, 3) |
| 4 | 2 | (2, 4) |

Spanning tree: `[[1, 2], [1, 3], [2, 4]]`

For this particular input the spanning tree equals the original graph because the input is already a tree (3 edges, 4 vertices, connected).

---

## Limitations and Future Work

| Limitation | Potential Improvement |
|------------|----------------------|
| DFS always starts from vertex `1` | Accept a configurable start vertex via command-line argument |
| No error handling for malformed `data.txt` | Add input validation with informative error messages |
| Only undirected graphs are supported | Extend to directed graphs (digraphs) |
| Graph must be described in a plain-text file | Add support for interactive input or standard input (`stdin`) |
| Only one connected-component is analyzed | For disconnected graphs, enumerate and visualize each component separately |
| Minor typo in `adjacet_matrix` function name (`adjacet` instead of `adjacency`) | Rename to `adjacency_list` in a future refactor |
