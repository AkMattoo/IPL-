"""
IPL Data Analysis Model (2008-2026)
====================================
A comprehensive analytics engine for Indian Premier League data.

Author: IPL Analytics Team
Version: 1.0.0
Date: 2026-07-01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================

TEAM_COLORS = {
    'CSK': '#FFFF00', 'MI': '#004BA0', 'RCB': '#EC1C24', 'KKR': '#3A225D',
    'SRH': '#FF822A', 'DC': '#0078BC', 'RR': '#254AA5', 'PBKS': '#ED1B24',
    'GT': '#1B2133', 'LSG': '#0057E7', 'DEC': '#8B4513', 'GL': '#FF4500',
    'RPS': '#C0C0C0', 'KTK': '#800080', 'PWI': '#4B0082'
}

TEAM_FULL_NAMES = {
    'CSK': 'Chennai Super Kings', 'MI': 'Mumbai Indians', 'RCB': 'Royal Challengers Bangalore',
    'KKR': 'Kolkata Knight Riders', 'SRH': 'Sunrisers Hyderabad', 'DC': 'Delhi Capitals',
    'RR': 'Rajasthan Royals', 'PBKS': 'Punjab Kings', 'GT': 'Gujarat Titans', 
    'LSG': 'Lucknow Super Giants', 'DEC': 'Deccan Chargers', 'GL': 'Gujarat Lions',
    'RPS': 'Rising Pune Supergiant', 'KTK': 'Kochi Tuskers Kerala', 'PWI': 'Pune Warriors India'
}

ACTIVE_TEAMS = ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GT', 'LSG']

SEASONS_CONFIG = {
    2008: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'DEC'], 'matches': 59},
    2009: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'DEC'], 'matches': 59},
    2010: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'DEC'], 'matches': 60},
    2011: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'KTK', 'PWI'], 'matches': 74},
    2012: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'PWI'], 'matches': 76},
    2013: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'PWI'], 'matches': 76},
    2014: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS'], 'matches': 60},
    2015: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS'], 'matches': 60},
    2016: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GL', 'RPS'], 'matches': 60},
    2017: {'teams': ['MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GL', 'RPS'], 'matches': 60},
    2018: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS'], 'matches': 60},
    2019: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS'], 'matches': 60},
    2020: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS'], 'matches': 60},
    2021: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS'], 'matches': 60},
    2022: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GT', 'LSG'], 'matches': 74},
    2023: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GT', 'LSG'], 'matches': 74},
    2024: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GT', 'LSG'], 'matches': 74},
    2025: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GT', 'LSG'], 'matches': 74},
    2026: {'teams': ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'RR', 'PBKS', 'GT', 'LSG'], 'matches': 74},
}

FINALS = {
    2008: ('RR', 'CSK'), 2009: ('DEC', 'RCB'), 2010: ('CSK', 'MI'),
    2011: ('CSK', 'RCB'), 2012: ('KKR', 'CSK'), 2013: ('MI', 'CSK'),
    2014: ('KKR', 'PBKS'), 2015: ('MI', 'CSK'), 2016: ('SRH', 'RCB'),
    2017: ('MI', 'RPS'), 2018: ('CSK', 'SRH'), 2019: ('MI', 'CSK'),
    2020: ('MI', 'DC'), 2021: ('CSK', 'KKR'), 2022: ('GT', 'RR'),
    2023: ('CSK', 'GT'), 2024: ('KKR', 'SRH'), 2025: ('RCB', 'PBKS'),
    2026: ('RCB', 'GT'),
}

VENUES = {
    'Mumbai': {'home': 'MI', 'type': 'batting', 'avg_score': 165, 'dew': 7.5},
    'Chennai': {'home': 'CSK', 'type': 'spin', 'avg_score': 155, 'dew': 5.0},
    'Bangalore': {'home': 'RCB', 'type': 'batting', 'avg_score': 170, 'dew': 6.5},
    'Kolkata': {'home': 'KKR', 'type': 'balanced', 'avg_score': 160, 'dew': 6.0},
    'Hyderabad': {'home': 'SRH', 'type': 'balanced', 'avg_score': 158, 'dew': 5.5},
    'Delhi': {'home': 'DC', 'type': 'batting', 'avg_score': 162, 'dew': 6.0},
    'Jaipur': {'home': 'RR', 'type': 'balanced', 'avg_score': 160, 'dew': 5.0},
    'Mohali': {'home': 'PBKS', 'type': 'batting', 'avg_score': 168, 'dew': 5.5},
    'Ahmedabad': {'home': 'GT', 'type': 'batting', 'avg_score': 175, 'dew': 6.5},
    'Lucknow': {'home': 'LSG', 'type': 'balanced', 'avg_score': 160, 'dew': 5.5},
}


# ============================================================
# IPL ANALYTICS MODEL CLASS
# ============================================================

class IPLAnalyticsModel:
    """
    IPL Data Analytics Model (2008-2026)

    Comprehensive analysis covering:
    - Best batsman/bowler per season (composite scoring)
    - Toss impact analysis
    - Home vs away performance
    - Top 4 to trophy conversion
    - Pitch evolution over years
    - Team success metrics
    - Match prediction model

    Usage:
        model = IPLAnalyticsModel(matches_df, batting_df, bowling_df, pitch_df, points_df)
        toss_impact = model.analyze_toss_impact()
        best_batsmen = model.get_best_batsman_per_season()
        ...
    """

    def __init__(self, matches_df, batting_df, bowling_df, pitch_df, points_df):
        """
        Initialize the model with datasets.

        Parameters:
        -----------
        matches_df : DataFrame
            Match-level data with scores, toss, venue info
        batting_df : DataFrame
            Batsman statistics per season
        bowling_df : DataFrame
            Bowler statistics per season
        pitch_df : DataFrame
            Venue/pitch conditions per season
        points_df : DataFrame
            Points table standings per season
        """
        self.matches = matches_df
        self.batting = batting_df
        self.bowling = bowling_df
        self.pitch = pitch_df
        self.points = points_df

    # ---- COMPOSITE SCORING FUNCTIONS ----

    def calculate_batsman_composite(self, row):
        """
        Calculate composite score for batsman evaluation.

        Formula: Runs×0.4 + StrikeRate×2 + Average×3 + Impact×50 + MatchWins×30 − Dot%×2

        This weights:
        - Runs (volume) at 0.4x
        - Strike Rate (aggression) at 2x
        - Average (consistency) at 3x
        - Impact Score (match-winning ability) at 50x
        - Match-winning knocks at 30x
        - Penalty for dot ball percentage at 2x
        """
        return (
            row['runs'] * 0.4 +
            row['strike_rate'] * 2.0 +
            row['average'] * 3.0 +
            row['impact_score'] * 50.0 +
            row['match_winning_knocks'] * 30.0 -
            row['dot_ball_percentage'] * 2.0
        )

    def calculate_bowler_composite(self, row):
        """
        Calculate composite score for bowler evaluation.

        Formula: Wkts×15 + (12−Econ)×20 + Dot%×3 + Impact×40 + MatchWins×25 + 4W×10 + 5W×20

        This weights:
        - Wickets (volume) at 15x
        - Economy rate (lower is better, inverted) at 20x
        - Dot ball percentage (pressure) at 3x
        - Impact Score at 40x
        - Match-winning spells at 25x
        - 4-wicket hauls at 10x
        - 5-wicket hauls at 20x
        """
        return (
            row['wickets'] * 15.0 +
            (12 - row['economy']) * 20.0 +
            row['dot_ball_percentage'] * 3.0 +
            row['impact_score'] * 40.0 +
            row['match_winning_spells'] * 25.0 +
            row['four_wickets'] * 10.0 +
            row['five_wickets'] * 20.0
        )

    # ---- ANALYSIS 1: TOSS IMPACT ----

    def analyze_toss_impact(self):
        """
        Analyze how toss affects match outcomes season by season.

        Returns DataFrame with columns:
        - season: Year
        - toss_winner_won: Count of matches where toss winner also won match
        - total_matches: Total matches in season
        - toss_win_pct: Percentage of toss winners who won the match
        - field_first_win_pct: Win % when choosing to field first
        - bat_first_win_pct: Win % when choosing to bat first
        """
        results = []
        for season in range(2008, 2027):
            season_matches = self.matches[self.matches['season'] == season]
            toss_winners_won = season_matches[season_matches['toss_winner'] == season_matches['winner']].shape[0]
            total = season_matches.shape[0]

            field_first = season_matches[season_matches['toss_decision'] == 'field']
            bat_first = season_matches[season_matches['toss_decision'] == 'bat']

            field_win_pct = field_first[field_first['toss_winner'] == field_first['winner']].shape[0] / max(1, field_first.shape[0]) * 100
            bat_win_pct = bat_first[bat_first['toss_winner'] == bat_first['winner']].shape[0] / max(1, bat_first.shape[0]) * 100

            results.append({
                'season': season,
                'toss_winner_won': toss_winners_won,
                'total_matches': total,
                'toss_win_pct': round(toss_winners_won / total * 100, 2),
                'field_first_win_pct': round(field_win_pct, 2),
                'bat_first_win_pct': round(bat_win_pct, 2),
                'field_count': field_first.shape[0],
                'bat_count': bat_first.shape[0]
            })

        return pd.DataFrame(results)

    # ---- ANALYSIS 2: BEST PLAYERS PER SEASON ----

    def get_best_batsman_per_season(self):
        """
        Find best batsman per season using composite score.

        Returns DataFrame with season, player, team, and all metrics.
        """
        self.batting['composite_score'] = self.batting.apply(self.calculate_batsman_composite, axis=1)
        best = self.batting.loc[self.batting.groupby('season')['composite_score'].idxmax()]
        return best[['season', 'player', 'team', 'runs', 'strike_rate', 'average', 
                     'impact_score', 'match_winning_knocks', 'dot_ball_percentage', 'composite_score']].sort_values('season')

    def get_best_bowler_per_season(self):
        """
        Find best bowler per season using composite score.

        Returns DataFrame with season, player, team, and all metrics.
        """
        self.bowling['composite_score'] = self.bowling.apply(self.calculate_bowler_composite, axis=1)
        best = self.bowling.loc[self.bowling.groupby('season')['composite_score'].idxmax()]
        return best[['season', 'player', 'team', 'wickets', 'economy', 'dot_ball_percentage',
                     'impact_score', 'match_winning_spells', 'death_over_economy', 'composite_score']].sort_values('season')

    # ---- ANALYSIS 3: HOME VS AWAY ----

    def analyze_home_away(self):
        """
        Analyze home vs away performance for all active teams.

        Returns DataFrame with columns:
        - team: Team code
        - home_wins, home_total: Home match stats
        - away_wins, away_total: Away match stats
        - home_win_pct, away_win_pct: Win percentages
        - advantage: Home advantage percentage (home - away)
        """
        results = []
        for team in ACTIVE_TEAMS:
            home_wins = 0; home_total = 0; away_wins = 0; away_total = 0

            for season in range(2008, 2027):
                season_matches = self.matches[self.matches['season'] == season]
                if team not in SEASONS_CONFIG[season]['teams']: continue

                for _, match in season_matches.iterrows():
                    venue = match['venue']
                    home_team = VENUES.get(venue, {}).get('home', None)

                    if match['team1'] == team or match['team2'] == team:
                        if home_team == team:
                            home_total += 1
                            if match['winner'] == team: home_wins += 1
                        elif home_team is not None:
                            away_total += 1
                            if match['winner'] == team: away_wins += 1

            if home_total > 0 and away_total > 0:
                results.append({
                    'team': team,
                    'home_wins': home_wins, 'home_total': home_total,
                    'away_wins': away_wins, 'away_total': away_total,
                    'home_win_pct': round(home_wins / home_total * 100, 2),
                    'away_win_pct': round(away_wins / away_total * 100, 2),
                    'advantage': round((home_wins / home_total - away_wins / away_total) * 100, 2)
                })

        return pd.DataFrame(results).sort_values('advantage', ascending=False)

    # ---- ANALYSIS 4: TOP 4 TO TROPHY CONVERSION ----

    def analyze_playoff_conversion(self):
        """
        Analyze how often each playoff position wins the trophy.

        Returns DataFrame with columns:
        - position: 1st, 2nd, 3rd, or 4th place
        - trophies: Number of trophies won from that position
        - playoff_appearances: Total times that position qualified
        - conversion_rate: Trophies / Appearances × 100
        """
        position_wins = self.points[self.points['winner'] == True]['position'].value_counts().sort_index()
        position_qualified = self.points[self.points['qualified'] == True]['position'].value_counts().sort_index()

        results = []
        for pos in [1, 2, 3, 4]:
            wins = position_wins.get(pos, 0)
            qualified = position_qualified.get(pos, 0)
            results.append({
                'position': pos,
                'trophies': wins,
                'playoff_appearances': qualified,
                'conversion_rate': round(wins / qualified * 100, 2) if qualified > 0 else 0
            })

        return pd.DataFrame(results)

    # ---- ANALYSIS 5: PITCH EVOLUTION ----

    def analyze_pitch_evolution(self):
        """
        Analyze how pitches have evolved over time.

        Returns DataFrame with aggregated pitch metrics per season.
        """
        return self.pitch.groupby('season').agg({
            'avg_first_innings_score': 'mean',
            'avg_second_innings_score': 'mean',
            'batting_friendly': 'mean',
            'bounce_rating': 'mean',
            'turn_rating': 'mean',
            'dew_factor': 'mean',
            'chasing_success_rate': 'mean'
        }).round(2).reset_index()

    # ---- ANALYSIS 6: TEAM SUCCESS METRICS ----

    def analyze_team_success(self):
        """
        Comprehensive team success analysis.

        Returns DataFrame with columns:
        - team: Team code
        - trophies: Total IPL titles
        - finals: Total finals appearances
        - playoff_appearances: Total playoff qualifications
        - playoff_rate: % of seasons in playoffs
        - trophy_rate: Trophies / Playoff appearances
        """
        trophies = self.points[self.points['winner'] == True]['team'].value_counts()
        playoff_apps = self.points[self.points['qualified'] == True]['team'].value_counts()
        finals = self.points[self.points['finalist'] == True]['team'].value_counts()

        all_teams = set(trophies.index) | set(playoff_apps.index)
        results = []
        for team in all_teams:
            results.append({
                'team': team,
                'trophies': trophies.get(team, 0),
                'finals': finals.get(team, 0),
                'playoff_appearances': playoff_apps.get(team, 0),
                'playoff_rate': round(playoff_apps.get(team, 0) / 19 * 100, 2),
                'trophy_rate': round(trophies.get(team, 0) / max(1, playoff_apps.get(team, 0)) * 100, 2)
            })

        return pd.DataFrame(results).sort_values('trophies', ascending=False)

    # ---- ANALYSIS 7: PREDICTIVE MODEL ----

    def build_match_predictor(self):
        """
        Build a Random Forest model to predict match outcomes.

        Features used:
        - Season context
        - Toss winner and decision
        - Team strength (historical win rate)
        - Home advantage

        Returns dict with:
        - model: Trained RandomForestClassifier
        - accuracy: Model accuracy on training data
        - feature_importance: Dict of feature importance scores
        """
        from sklearn.ensemble import RandomForestClassifier

        pred_df = self.matches.copy()
        pred_df['toss_winner_is_team1'] = (pred_df['toss_winner'] == pred_df['team1']).astype(int)
        pred_df['toss_decision_field'] = (pred_df['toss_decision'] == 'field').astype(int)

        team_win_rates = self.points.groupby('team')['won'].sum() / self.points.groupby('team')['matches_played'].sum()
        pred_df['team1_strength'] = pred_df['team1'].map(team_win_rates)
        pred_df['team2_strength'] = pred_df['team2'].map(team_win_rates)

        pred_df['team1_home'] = pred_df.apply(lambda x: 1 if VENUES.get(x['venue'], {}).get('home') == x['team1'] else 0, axis=1)
        pred_df['team2_home'] = pred_df.apply(lambda x: 1 if VENUES.get(x['venue'], {}).get('home') == x['team2'] else 0, axis=1)

        pred_df['team1_wins'] = (pred_df['winner'] == pred_df['team1']).astype(int)

        features = ['season', 'toss_winner_is_team1', 'toss_decision_field', 
                   'team1_strength', 'team2_strength', 'team1_home', 'team2_home']

        X = pred_df[features].fillna(0.5)
        y = pred_df['team1_wins']

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        accuracy = model.score(X, y)
        feature_importance = dict(zip(features, model.feature_importances_))

        return {'model': model, 'accuracy': accuracy, 'feature_importance': feature_importance}

    # ---- VISUALIZATION: FULL DASHBOARD ----

    def create_full_dashboard(self, save_path='ipl_dashboard.png'):
        """
        Generate a comprehensive 24-panel visualization dashboard.

        Parameters:
        -----------
        save_path : str
            Path to save the dashboard image
        """
        # This method contains all visualization code
        # (Implementation is in the notebook for brevity)
        pass


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def load_data(data_dir='data/raw'):
    """
    Load all IPL datasets from CSV files.

    Parameters:
    -----------
    data_dir : str
        Directory containing CSV files

    Returns:
    --------
    tuple : (matches_df, batting_df, bowling_df, pitch_df, points_df)
    """
    matches = pd.read_csv(f'{data_dir}/ipl_matches_2008_2026.csv')
    batting = pd.read_csv(f'{data_dir}/ipl_batting_2008_2026.csv')
    bowling = pd.read_csv(f'{data_dir}/ipl_bowling_2008_2026.csv')
    pitch = pd.read_csv(f'{data_dir}/ipl_pitch_2008_2026.csv')
    points = pd.read_csv(f'{data_dir}/ipl_points_table_2008_2026.csv')
    return matches, batting, bowling, pitch, points


def run_full_analysis(data_dir='data/raw', output_dir='reports/analysis_results'):
    """
    Run the complete IPL analysis pipeline and save all results.

    Parameters:
    -----------
    data_dir : str
        Input data directory
    output_dir : str
        Output directory for analysis results
    """
    # Load data
    matches, batting, bowling, pitch, points = load_data(data_dir)

    # Initialize model
    model = IPLAnalyticsModel(matches, batting, bowling, pitch, points)

    # Run all analyses
    print("Running Toss Impact Analysis...")
    toss_impact = model.analyze_toss_impact()
    toss_impact.to_csv(f'{output_dir}/toss_impact.csv', index=False)

    print("Finding Best Batsman Per Season...")
    best_batsmen = model.get_best_batsman_per_season()
    best_batsmen.to_csv(f'{output_dir}/best_batsmen.csv', index=False)

    print("Finding Best Bowler Per Season...")
    best_bowlers = model.get_best_bowler_per_season()
    best_bowlers.to_csv(f'{output_dir}/best_bowlers.csv', index=False)

    print("Analyzing Home vs Away Performance...")
    home_away = model.analyze_home_away()
    home_away.to_csv(f'{output_dir}/home_away.csv', index=False)

    print("Analyzing Playoff Conversion...")
    playoff_conversion = model.analyze_playoff_conversion()
    playoff_conversion.to_csv(f'{output_dir}/playoff_conversion.csv', index=False)

    print("Analyzing Pitch Evolution...")
    pitch_evolution = model.analyze_pitch_evolution()
    pitch_evolution.to_csv(f'{output_dir}/pitch_evolution.csv', index=False)

    print("Analyzing Team Success...")
    team_success = model.analyze_team_success()
    team_success.to_csv(f'{output_dir}/team_success.csv', index=False)

    print("Building Match Predictor...")
    predictor = model.build_match_predictor()

    print(f"\n✅ Analysis complete! Results saved to {output_dir}/")
    print(f"   Match Predictor Accuracy: {predictor['accuracy']:.3f}")
    print(f"   Top Feature: {max(predictor['feature_importance'], key=predictor['feature_importance'].get)}")

    return model


if __name__ == '__main__':
    # Run full analysis when executed directly
    run_full_analysis()
