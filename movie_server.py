
import os, asyncio
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from movie_planner import (
    SearchParams, DetailParams, RecommendParams, TopByActorParams, SimilarParams, PlaylistParams,
    do_search, do_details, do_recommend, do_top_by_actor, do_similar, do_playlist
)

mcp = FastMCP("mcp-movielens")

MOVIE_TOOL_TIMEOUT = float(os.getenv("MOVIE_TOOL_TIMEOUT", "25.0"))

async def _run(fn, *args, timeout: Optional[float] = None):
    to = timeout if timeout is not None else MOVIE_TOOL_TIMEOUT
    return await asyncio.wait_for(asyncio.to_thread(fn, *args), timeout=to)

# Herramientas que resuelven
@mcp.tool()
async def search_movie(params: SearchParams) -> List[Dict[str, Any]]:
    """Full-text search over titles; returns brief metadata sorted by rating/popularity."""
    return await _run(do_search, params)

@mcp.tool()
async def movie_details(params: DetailParams) -> Dict[str, Any]:
    """Exact/best-match details for a title; includes cast, crew (Director/Writer) and keywords when available."""
    res = await _run(do_details, params)
    return res or {}

@mcp.tool()
async def recommend_movies_tool(params: RecommendParams) -> List[Dict[str, Any]]:
    """Multi-filter recommender: genres, min_vote, year range, language, include_cast."""
    return await _run(do_recommend, params)

@mcp.tool()
async def top_movies_by_actor_tool(params: TopByActorParams) -> List[Dict[str, Any]]:
    """Top rated/popular films for a given actor name."""
    return await _run(do_top_by_actor, params)

@mcp.tool()
async def similar_movies_tool(params: SimilarParams) -> List[Dict[str, Any]]:
    """Keyword-overlap similarity to a given title."""
    return await _run(do_similar, params)

@mcp.tool()
async def build_playlist_tool(params: PlaylistParams) -> Dict[str, Any]:
    """Greedy watchlist fill to target_minutes using runtime; optional genres/language; bias toward rating/popularity."""
    return await _run(do_playlist, params)

if __name__ == "__main__":
    mcp.run()
