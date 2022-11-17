
import requests, json, os
from app import db
from flaskr.models import *
from queries import *
def get_movies_list(date_from, date_to, league_ids)->None:
    url = "http://api.football-data.org/v4/matches"

    response = requests.get(url, params={'competitions': league_ids, 'dateFrom': date_from, 'dateTo':date_to, 'X-Auth-Token': os.environ.get('FD_API_KEY')})
    dict = json.loads(response.json)

    for match in dict["matches"]:
        match = query_match_on_id(match['id'])
        if match:
            continue
        
        country = query_country_on_id(match['area']['id'])
        if not country:
            country = Country()
            country.id = match['area']['id']
            country.code = match['area']['code']
            country.name = match['area']['name']
            db.session.add(country)
            
        season = query_season_on_id(match['season']['id'])
        if not season:
            season = Season()
            season.id = match['season']['id']
            season.start_date = match['season']['startDate']
            season.end_date = match['season']['endDate']
            season.current_matchday = match['season']['currentMatchday']
            db.session.add(season)
            
        league = query_league_on_id(match['competition']['id'])
        if not league:
            league = League()
            league.id = match['competition']['id']
            league.name = match['competition']['name']
            league.country = country
            db.session.add(league)
        

            
        home_team = query_team_on_id(match['homeTeam']['id'])
        if not home_team:
            home_team = Team()
            home_team.id = match['homeTeam']['id']
            home_team.name = match['homeTeam']['name']
            home_team.tla = match['homeTeam']['tla']
            db.session.add(home_team)
        
        away_team = query_team_on_id(match['awayTeam']['id'])
        if not away_team:
            away_team = Team()
            away_team.id = match['awayTeam']['id']
            away_team.name = match['awayTeam']['name']
            away_team.tla = match['awayTeam']['tla']
            db.session.add(away_team)
        
        score = Score()
        score.fulltime_goals_away = match['score']['fulltime']['away']
        score.fulltime_goals_home = match['score']['fulltime']['home']
        score.halftime_goals_home = match['score']['halftime']['home']
        score.halftime_goals_away = match['score']['halftime']['away']
        score.winner = match['score']['winner']
        db.session.add(score)
        
        new_match = Match()
        new_match.id = match['id']
        new_match.matchday = match['matchday']
        new_match.status = match['status']
        new_match.match_date_time = match['utcDate']
        new_match.away_team = away_team
        new_match.home_team = home_team
        new_match.season = season
        new_match.score = score
        db.session.add(new_match)
        db.session.commit()
        
