# MCP Movie Server (MovieLens/TMDB)

A lightweight **Model Context Protocol (MCP)** server that reads local CSV files (MovieLens/TMDB) and exposes movie tools over **STDIO**. It is designed to be invoked by MCP-compatible hosts (e.g., MCP Inspector or your own LLM-powered chat host).

> **Repository state — datasets included**
>
> The repo already contains a `datasets/` folder with:
>
> - `movies_metadata.csv` ✅
> - `keywords.csv` ✅
>
> **Not included**: `credits.csv` (too large for GitHub).  
> Features that rely on cast/crew will work **only** if you download `credits.csv` and place it in `datasets/`. See **External datasets** below.

---

## 1) What this server provides
- **Title search** ranked by vote count / rating / popularity.
- **Movie detail** (base metadata, plus keywords; cast/crew when `credits.csv` is present).
- **Recommender** with filters by genres, language, year range, and minimum rating (optionally filter by cast when `credits.csv` exists).
- **Top movies by actor/actress** (requires `credits.csv`).
- **Similar movies by keywords** (uses `keywords.csv`).
- **Watchlist builder** that fills a target number of minutes using each movie's `runtime` (greedy, with bias to rating or popularity).

This server is intentionally simple: it loads CSVs into Pandas once (memoized), normalizes types, and parses JSON-like columns from TMDB (single quotes to valid JSON).

---

## 2) Tools exposed (and dataset dependencies)

| Tool | What it does | Requires |
|---|---|---|
| `search_movie` | Full-text title search; compact metadata | `movies_metadata.csv` |
| `movie_details` | Detailed record (adds `keywords` and, if available, `cast/crew`) | `movies_metadata.csv`, `keywords.csv`, *(optional)* `credits.csv` |
| `recommend_movies_tool` | Multi-filter recommender (genres, language, years, min rating; `include_cast` if cast data is available) | `movies_metadata.csv`, *(optional)* `credits.csv` |
| `top_movies_by_actor_tool` | Best-rated/popular films for an actor | **Requires** `credits.csv` |
| `similar_movies_tool` | Finds related titles via keyword overlap | `movies_metadata.csv`, `keywords.csv` |
| `build_playlist_tool` | Greedy watchlist toward a minute target (`runtime`) | `movies_metadata.csv` |

**Works without `credits.csv`:** `search_movie`, `movie_details` (basic + keywords), `recommend_movies_tool` (without `include_cast`), `similar_movies_tool`, `build_playlist_tool`.  
**Needs `credits.csv`:** `top_movies_by_actor_tool`, `movie_details` (cast/crew), and the `include_cast` filter in `recommend_movies_tool`.

---

## 3) External datasets (to enable cast/crew)
To unlock all cast/crew-based functionality, download the full dataset from Kaggle (by **Rounak Banik**) and copy **`credits.csv`** into your local `datasets/` folder:

- **The Movies Dataset (Kaggle)**: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/data

Project layout (suggested):
```
project-root/
├── mcp_servers/movies/
│   ├── movie_server.py
│   ├── movie_planner.py
│   ├── movie_sources.py
│   └── datasets/
│       ├── movies_metadata.csv
│       ├── keywords.csv
│       └── credits.csv  ← optional but recommended
└── ...
```

---

## 4) Installation
Requirements: **Python 3.10+**, `pip`

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements_movies.txt
pip install mcp[cli]
```

---

## 5) Running the MCP server (STDIO)

### A) From MCP Inspector
1. Transport: **STDIO**  
2. Command: `python` (or `py` on Windows)  
3. Arguments: `movie_server.py stdio`  
4. Working directory: the folder containing `movie_server.py`.  
5. **Optional**: if your CSVs are not in `./datasets`, set `MOVIELENS_DIR` to the directory with the files.

### B) From the command line
```bash
python movie_server.py stdio
```
Connect your MCP host to this process via STDIO.

---

## 6) Quick tests (good for screenshots)
Run from the **Tools → Call Tool** panel in MCP Inspector.

**a) `search_movie`**
```json
{"query":"Toy Story","limit":5}
```

**b) `movie_details`** (without `credits.csv` you will see base metadata + keywords; with `credits.csv` you also get cast/crew)
```json
{"title":"Inception"}
```

**c) `recommend_movies_tool`**
```json
{
  "genres": ["Science Fiction","Adventure"],
  "min_vote": 7.5,
  "from_year": 2000,
  "to_year": 2020,
  "language": "en",
  "limit": 10
}
```

**d) `similar_movies_tool`**
```json
{"title":"The Dark Knight","limit":10}
```

**e) `build_playlist_tool`**
```json
{"target_minutes":480,"prefer_high_rating":true,"genres":["Drama","Thriller"]}
```

**f) (requires `credits.csv`) `top_movies_by_actor_tool`**
```json
{"actor":"Tom Hanks","limit":8}
```

**g) (requires `credits.csv`) `recommend_movies_tool` with include_cast**
```json
{
  "genres": ["Drama"],
  "min_vote": 7.0,
  "include_cast": ["Leonardo DiCaprio"],
  "limit": 10
}
```

---

## 7) Troubleshooting
- **Empty results** → ensure CSVs exist in `datasets/` or set `MOVIELENS_DIR` to their directory.  
- **Missing modules** → `pip install -r requirements_movies.txt`.  
- **Cast/crew missing** → add `credits.csv`.  
- **Slow first call** → CSVs are cached after the first load.  
- **Encoding/JSON quirks** → loader fixes numeric types and parses JSON-like strings (single-quote to JSON).

---

## 8) References
- **Kaggle — The Movies Dataset (Rounak Banik)**: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/data  
- **MCP Python SDK (servers & docs used as reference)**: https://github.com/modelcontextprotocol/python-sdk  
- **MCP Architecture**: https://modelcontextprotocol.io/docs/learn/architecture  
- **MCP Specification (2025-06-18)**: https://modelcontextprotocol.io/specification/2025-06-18

