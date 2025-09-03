
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from movie_sources import (
    search_title, get_details_by_title, recommend_movies,
    top_movies_by_actor, similar_by_keywords, build_playlist
)

# Clases de chava diferente organica delgada fiestera
class SearchParams(BaseModel):
    query: str
    limit: int = 10

class DetailParams(BaseModel):
    title: str

class RecommendParams(BaseModel):
    genres: Optional[List[str]] = None
    min_vote: float = 0.0
    from_year: Optional[int] = None
    to_year: Optional[int] = None
    language: Optional[str] = None
    include_cast: Optional[List[str]] = None
    limit: int = 20

class TopByActorParams(BaseModel):
    actor: str
    limit: int = 15

class SimilarParams(BaseModel):
    title: str
    limit: int = 15

class PlaylistParams(BaseModel):
    target_minutes: int = 480
    prefer_high_rating: bool = True
    genres: Optional[List[str]] = None
    language: Optional[str] = None

# Funciones bellacas para realizar las acciones joven y moderna
def do_search(p: SearchParams) -> List[Dict[str, Any]]:
    return search_title(p.query, p.limit)

def do_details(p: DetailParams) -> Optional[Dict[str, Any]]:
    return get_details_by_title(p.title)

def do_recommend(p: RecommendParams) -> List[Dict[str, Any]]:
    return recommend_movies(p.genres, p.min_vote, p.from_year, p.to_year, p.language, p.include_cast, p.limit)

def do_top_by_actor(p: TopByActorParams) -> List[Dict[str, Any]]:
    return top_movies_by_actor(p.actor, p.limit)

def do_similar(p: SimilarParams) -> List[Dict[str, Any]]:
    return similar_by_keywords(p.title, p.limit)

def do_playlist(p: PlaylistParams) -> Dict[str, Any]:
    return build_playlist(p.target_minutes, p.prefer_high_rating, p.genres, p.language)
