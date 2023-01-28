import os
import requests
from datetime import datetime, timedelta
from time import sleep

from app import db
from flaskr.models import *
from .queries import *


os.environ["FD_API_KEY"] = "497529ca191e46a9ade33d8e921449e8"


def get_matches(date_from, date_to, league_ids) -> None:
    url = "http://api.football-data.org/v4/matches"
    start, end = date_from, date_from + timedelta(days=6)
    while end < date_to:
        response = requests.get(
            url,
            params={
                "competitions": league_ids,
                "dateFrom": start.strftime("%Y-%m-%d"),
                "dateTo": end.strftime("%Y-%m-%d"),
            },
            headers={"X-Auth-Token": f"{os.environ.get('FD_API_KEY')}"},
        )
        start += timedelta(days=7)
        end += timedelta(days=7)
        dict = response.json()
        for match in dict.get("matches"):
            db_match = query_match_on_id(match.get("id"))
            if db_match:
                # continue if match already in database
                continue

            country = query_country_on_id(match.get("area").get("id"))
            if not country:
                country = Country()
                country.id = match.get("area").get("id")
                country.code = match.get("area").get("code")
                country.name = match.get("area").get("name")
                db.session.add(country)

            season = query_season_on_id(match.get("season").get("id"))
            if not season:
                season = Season()
                season.id = match.get("season").get("id")
                season.start_date = datetime.strptime(
                    match.get("season").get("startDate"), "%Y-%m-%d"
                )
                season.end_date = datetime.strptime(
                    match.get("season").get("endDate"), "%Y-%m-%d"
                )
                season.current_matchday = match.get("season").get("currentMatchday")
                db.session.add(season)

            league = query_league_on_id(match.get("competition").get("id"))
            if not league:
                league = League()
                league.id = match.get("competition").get("id")
                league.name = match.get("competition").get("name")
                league.country = country
                db.session.add(league)

            home_team = query_team_on_id(match.get("homeTeam").get("id"))
            if not home_team:
                home_team = Team()
                home_team.id = match.get("homeTeam").get("id")
                home_team.name = match.get("homeTeam").get("name")
                home_team.tla = match.get("homeTeam").get("tla")
                db.session.add(home_team)

            away_team = query_team_on_id(match.get("awayTeam").get("id"))
            if not away_team:
                away_team = Team()
                away_team.id = match.get("awayTeam").get("id")
                away_team.name = match.get("awayTeam").get("name")
                away_team.tla = match.get("awayTeam").get("tla")
                db.session.add(away_team)

            score = Score()
            score.fulltime_goals_away = match.get("score").get("fullTime").get("away")
            score.fulltime_goals_home = match.get("score").get("fullTime").get("home")
            score.halftime_goals_home = match.get("score")["halfTime"].get("home")
            score.halftime_goals_away = match.get("score")["halfTime"].get("away")
            score.winner = match.get("score").get("winner")
            db.session.add(score)

            new_match = Match()
            new_match.id = match.get("id")
            new_match.matchday = match.get("matchday")
            new_match.status = match.get("status")
            new_match.match_date_time = datetime.strptime(
                match.get("utcDate"), "%Y-%m-%dT%H:%M:%SZ"
            )
            new_match.away_team = [away_team]
            new_match.home_team = [home_team]
            new_match.season = season
            new_match.score = score
            db.session.add(new_match)
            db.session.commit()
        sleep(6)


def get_seasons(league_id: int) -> None:
    url = f"http://api.football-data.org/v4/competitions/{league_id}"
    response = requests.get(
        url, headers={"X-Auth-Token": f"{os.environ.get('FD_API_KEY')}"}
    )
    dict = response.json()
    league = query_league_on_code(f"{league_id}")

    if not league:
        get_league(league_id)
        league = query_league_on_code(f"{league_id}")

    for season in dict.get("seasons"):
        # if season does not exist yet create it
        if not query_season_on_id(season.get("id")):
            new_season = Season()
            new_season.id = season.get("id")
            new_season.name = season.get("name")
            new_season.start_date = datetime.strptime(
                season.get("startDate"), "%Y-%m-%d"
            )
            new_season.end_date = datetime.strptime(season.get("endDate"), "%Y-%m-%d")
            new_season.current_matchday = season.get("currentMatchday")
            new_season.league = league

            # if data for winner of season exists
            if season.get("winner"):
                winner = query_team_on_id(season.get("winner").get("id"))
                if not winner:
                    winner = Team()
                    winner.id = season.get("winner").get("id")
                    winner.name = season.get("winner").get("name")
                    winner.tla = season.get("winner").get("tla")
                    db.session.add(winner)
                new_season.winner = winner

            start_year = new_season.start_date.year
            start_date = new_season.start_date
            end_date = new_season.end_date
            if start_year == 2022 or start_year == 2023:
                url = f"http://api.football-data.org/v4/competitions/{league_id}/teams"
                response = requests.get(
                    url,
                    params={"season": start_year},
                    headers={"X-Auth-Token": f"{os.environ.get('FD_API_KEY')}"},
                )
                dict = response.json()

                for team in dict.get("teams"):
                    if not query_team_on_id(team.get("id")):
                        new_team = Team()
                        new_team.id = team.get("id")
                        new_team.name = team.get("name")
                        new_team.tla = team.get("tla")
                        new_team.seasons.append(new_season)
                        db.session.add(new_team)
                    else:
                        old_team = query_team_on_id(team.get("id"))
                        old_team.seasons.append(new_season)
                        db.session.add(old_team)

                sleep(6)
                get_matches(start_date, end_date, [league_id])

            db.session.add(new_season)
            db.session.commit()


def get_league(league_id):
    url = f"http://api.football-data.org/v4/competitions/{league_id}"
    response = requests.get(
        url, headers={"X-Auth-Token": f"{os.environ.get('FD_API_KEY')}"}
    )
    dict = response.json()
    league = query_league_on_id(league_id)
    if not league:
        new_league = League()
        new_league.id = dict.get("id")
        new_league.name = dict.get("name")
        new_league.code = dict.get("code")

        country = query_country_on_id(dict.get("area").get("id"))

        if not country:
            new_country = Country()
            new_country.id = dict.get("area").get("id")
            new_country.name = dict.get("area").get("name")
            new_country.code = dict.get("area").get("code")
            db.session.add(new_country)
        else:
            new_country = country

        new_league.country = new_country

        db.session.add(new_league)
        db.session.commit()


# def get_standings_of_league(league_id, season):

# def get_countries():


def get_teams_of_season(league_id: int, start_year: int) -> None:
    url = f"http://api.football-data.org/v4/competitions/{league_id}/teams"
    response = requests.get(
        url,
        params={"season": start_year},
        headers={"X-Auth-Token": f"{os.environ.get('FD_API_KEY')}"},
    )
    dict = response.json()

    league = query_league_on_code(f"{league_id}")

    if not league:
        get_league(f"{league_id}")
        league = query_league_on_code(f"{league_id}")

    for team in dict.get("teams"):
        if not query_team_on_id(team.get("id")):
            new_team = Team()
            new_team.id = team.get("id")
            new_team.name = team.get("name")
            new_team.tla = team.get("tla")
            # create season first
            # new_team.seasons.append(query_season_on_id(dict.get('season').get('id')))
            db.session.add(new_team)
        else:
            old_team = query_team_on_id(team.get("id"))
            # create season first
            # old_team.seasons.append(query_season_on_id(dict.get('season').get('id')))
            db.session.add(old_team)

    db.session.commit()


def get_matches_of_season(league_id: str, start_year: str, match_day: int) -> None:
    url = f"http://api.football-data.org/v4/competitions/{league_id}/matches"
    response = requests.get(
        url,
        params={"season": start_year, "matchday": match_day},
        headers={"X-Auth-Token": f"{os.environ.get('FD_API_KEY')}"},
    )
    dict = response.json()

    league = query_league_on_code(league_id)

    for match in dict.get("matches"):
        if not query_match_on_id(match.get("id")):
            new_match = Match()

            new_match.id = match.get("id")
            new_match.matchday = match.get("matchday")
            new_match.match_date_time = datetime.strptime(
                match.get("utcDate"), "%Y-%m-%dT%H:%M:%SZ"
            )
            new_match.status = match.get("status")
            score = Score()
            score.winner = query_match_on_id(match.get("score").get("winner"))
            score.fulltime_goals_away = match.get("score").get("fullTime").get("away")
            score.fulltime_goals_home = match.get("score").get("fullTime").get("home")
            score.halftime_goals_away = match.get("score").get("halfTime").get("away")
            score.halftime_goals_home = match.get("score").get("halfTime").get("home")
            new_match.score = score
            new_match.season = query_season_on_id(match.get("season").get("id"))
            new_match.home_team = query_team_on_id(match.get("homeTeam").get("id"))
            new_match.away_team = query_team_on_id(match.get("awayTeam").get("id"))

            db.session.add(new_match)

    db.session.commit()


def get_data(league_id):
    get_league(league_id)
    get_seasons(league_id)
    seasons = query_all_seasons()
    for season in seasons:
        start_year = season.start_date.year
        get_teams_of_season(league_id, start_year)
        match_day = 1
        team_count = len(season.teams)
        while match_day < (team_count - 1) * 2:
            get_matches_of_season(league_id, start_year, match_day)
            sleep(6)
            match_day += 1


def test_get_data():
    get_data(2002)


def test_call():
    # get_league(2002)
    get_seasons(2002)
