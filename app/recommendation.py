import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

def get_recommendations(sp, top_tracks, limit=10):
    # Extract features from top tracks
    track_ids = [track['id'] for track in top_tracks]
    audio_features = sp.audio_features(track_ids)
    
    # Create a DataFrame with audio features
    df = pd.DataFrame(audio_features)
    df['id'] = track_ids
    
    # Select relevant features for recommendation
    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    
    # Normalize features
    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])
    
    # Get a larger pool of tracks for recommendations
    recommendations = sp.recommendations(seed_tracks=track_ids[:5], limit=100)
    rec_track_ids = [track['id'] for track in recommendations['tracks']]
    rec_audio_features = sp.audio_features(rec_track_ids)
    
    # Create a DataFrame with recommended track features
    rec_df = pd.DataFrame(rec_audio_features)
    rec_df['id'] = rec_track_ids
    rec_df[features] = scaler.transform(rec_df[features])
    
    # Combine user's top tracks and recommended tracks
    all_tracks = pd.concat([df, rec_df])
    
    # Create user profile by averaging features of top tracks
    user_profile = df[features].mean().values.reshape(1, -1)
    
    # Calculate similarity between user profile and all tracks
    similarities = cosine_similarity(user_profile, all_tracks[features])
    
    # Add similarity scores to the recommendation DataFrame
    all_tracks['similarity'] = similarities[0]
    
    # Sort recommendations by similarity
    rec_df = all_tracks[all_tracks['id'].isin(rec_track_ids)].sort_values('similarity', ascending=False)
    
    # Get top recommendations
    top_recommendations = rec_df.head(limit)
    
    # Fetch full track information for top recommendations
    recommended_tracks = sp.tracks(top_recommendations['id'].tolist())['tracks']
    
    return recommended_tracks

