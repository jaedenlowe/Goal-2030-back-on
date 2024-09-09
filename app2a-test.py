import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model

# Load the PyCaret models
models = [
    load_model('model_y1_tradkeeper'),
    load_model('model_y2_sweeperkeeper'),
    load_model('model_y3_ballplayingdefender'),
    load_model('model_y4_nononsensedefender'),
    load_model('model_y5_fullback'),
    load_model('model_y6_allactionmidfielder'),
    load_model('model_y7_midfieldplaymaker'),
    load_model('model_y8_traditionalwinger'),
    load_model('model_y9_invertedwinger'),
    load_model('model_y10_goalpoacher'),
    load_model('model_y11_targetman')
]

# Model names corresponding to their roles
model_names = [
    "Traditional Keeper",
    "Sweeper Keeper",
    "Ball-Playing Defender",
    "No-Nonsense Defender",
    "Full-Back",
    "All-Action Midfielder",
    "Midfield Playmaker",
    "Traditional Winger",
    "Inverted Winger",
    "Goal Poacher",
    "Target Man"
]

# Dictionary mapping model names to their score column names
score_column_map = {
    "Traditional Keeper": "y1_tradkeeper",
    "Sweeper Keeper": "y2_sweeperkeeper",
    "Ball-Playing Defender": "y3_ballplayingdefender",
    "No-Nonsense Defender": "y4_nononsensedefender",
    "Full-Back": "y5_fullback",
    "All-Action Midfielder": "y6_allactionmidfielder",
    "Midfield Playmaker": "y7_midfieldplaymaker",
    "Traditional Winger": "y8_traditionalwinger",
    "Inverted Winger": "y9_invertedwinger",
    "Goal Poacher": "y10_goalpoacher",
    "Target Man": "y11_targetman"
}



# Additional functions for squad generation
def generate_squad(prediction_results, num_players_per_position, selected_roles):
    """Generates a squad based on prediction results, number of players per position, and selected roles."""

    squad = []
    for position, num_players in num_players_per_position.items():
        # Filter predictions for the current position
        position_predictions = [result for result in prediction_results if any(role in selected_roles[position] for role in result['model_names'])]

        # Sort predictions by prediction_score in descending order
        position_predictions = sorted(position_predictions, key=lambda x: x['prediction_score'], reverse=True)

        # Select the top N players based on the number of players for this position
        top_players = position_predictions[:num_players]

        # Add recommended tag
        top_players['Recommended'] = 'Recommended'

        # Append the top players to the squad
        squad.append(top_players)

    # Concatenate all roles into one DataFrame
    final_squad = pd.concat(squad, ignore_index=True)

    return final_squad

def display_squad(squad):
  """Displays the generated squad."""

  st.header("Generated Squad")
  for player in squad:
    st.write(f"- {player['Player']}: {player['model_names']} ({player['prediction_score']:.2f})")

# Streamlit app
st.title("Player Attribute Prediction and Squad Generation")

# File uploader widget
uploaded_file = st.file_uploader("Upload a CSV file with player attributes", type="csv")

if uploaded_file is not None:
  # Read the CSV file into a DataFrame
  df = pd.read_csv(uploaded_file)

  # Display the dataframe
  st.write("Uploaded DataFrame:")
  st.write(df.head())

  # Make predictions for each model
  predictions = [predict_model(model, data=df) for model in models]

  # Display predictions
  st.write("Predictions:")

  # Create checkboxes for each model
  model_checkboxes = st.multiselect("Select a Position/Role:", model_names)

  # Create a slider for the prediction threshold
  threshold = st.slider("Prediction Threshold:", 0.0, 1.0, 0.5)

  # Create checkboxes for filtering by prediction_label
  show_recommended = st.checkbox("Show Recommended")
  show_not_recommended = st.checkbox("Show Not Recommended")

  for i, (prediction, model_name) in enumerate(zip(predictions, model_names)):
    if model_name in model_checkboxes:
      # Access the correct score column based on the model name
      score_column = score_column_map.get(model_name, "score") # Default to "score" if not found

      # Filter predictions based on the threshold
      filtered_prediction = prediction[prediction['prediction_score'] >= threshold]

      # Filter predictions based on prediction_label
      if show_recommended and not show_not_recommended:
        filtered_prediction = filtered_prediction[filtered_prediction['prediction_label'] == 1]
      elif show_not_recommended and not show_recommended:
        filtered_prediction = filtered_prediction[filtered_prediction['prediction_label'] == 0]

      # Rename the 'prediction_label' column to 'Recommended' and convert values
      filtered_prediction['Recommended'] = filtered_prediction['prediction_label'].apply(lambda x: "Recommended" if x == 1 else "Not Recommended")
      filtered_prediction.drop('prediction_label', axis=1, inplace=True)

      # Rename the score column to the corresponding model name
      filtered_prediction.rename(columns={score_column: model_name}, inplace=True)

      # Display model name and filtered prediction results
      st.header(f"{model_name}")
      st.write(filtered_prediction[['Player', model_name, 'Recommended', 'prediction_score']])

# Squad generation section
st.subheader("Squad Generation")

# Input for number of players per position
num_goalkeepers = st.number_input("Number of Goalkeepers", min_value=0, max_value=5, value=1)
num_defenders = st.number_input("Number of Defenders", min_value=0, max_value=10, value=4)
num_midfielders = st.number_input("Number of Midfielders", min_value=0, max_value=10, value=5)
num_attackers = st.number_input("Number of Attackers", min_value=0, max_value=5, value=3)

# Input for number of each role per position
st.write("**Goalkeeper Roles:**")
num_traditional_keepers = st.number_input("Traditional Keepers", min_value=0, max_value=num_goalkeepers, value=1)
num_sweeper_keepers = st.number_input("Sweeper Keepers", min_value=0, max_value=num_goalkeepers, value=0)
st.write("**Defender Roles:**")
num_ball_playing_defenders = st.number_input("Ball-Playing Defenders", min_value=0, max_value=num_defenders, value=2)
num_no_nonsense_defenders = st.number_input("No-Nonsense Defenders", min_value=0, max_value=num_defenders, value=2)
num_fullbacks = st.number_input("Full-Backs", min_value=0, max_value=num_defenders, value=0)
st.write("**Midfielder Roles:**")
num_all_action_midfielders = st.number_input("All-Action Midfielders", min_value=0, max_value=num_midfielders, value=2)
num_midfield_playmakers = st.number_input("Midfield Playmakers", min_value=0, max_value=num_midfielders, value=2)
num_traditional_wingers = st.number_input("Traditional Wingers", min_value=0, max_value=num_midfielders, value=1)
num_inverted_wingers = st.number_input("Inverted Wingers", min_value=0, max_value=num_midfielders, value=0)
st.write("**Attacker Roles:**")
num_goal_poachers = st.number_input("Goal Poachers", min_value=0, max_value=num_attackers, value=2)
num_target_men = st.number_input("Target Men", min_value=0, max_value=num_attackers, value=1)

# Squad generation section
if st.button("Generate Squad"):
    # Create a dictionary to store the selected roles for each position
    selected_roles = {
        "Goalkeeper": [
            "Traditional Keeper" * num_traditional_keepers +
            "Sweeper Keeper" * num_sweeper_keepers
        ],
        "Defender": [
            "Ball-Playing Defender" * num_ball_playing_defenders +
            "No-Nonsense Defender" * num_no_nonsense_defenders +
            "Full-Back" * num_fullbacks
        ],
        "Midfielder": [
            "All-Action Midfielder" * num_all_action_midfielders +
            "Midfield Playmaker" * num_midfield_playmakers +
            "Traditional Winger" * num_traditional_wingers +
            "Inverted Winger" * num_inverted_wingers
        ],
        "Attacker": [
            "Goal Poacher" * num_goal_poachers +
            "Target Man" * num_target_men
        ]
    }


    # Define number of players per position
    num_players_per_position = {
        "Goalkeeper": num_traditional_keepers + num_sweeper_keepers,
        "Defender": num_ball_playing_defenders + num_no_nonsense_defenders + num_fullbacks,
        "Midfielder": num_all_action_midfielders + num_midfield_playmakers + num_traditional_wingers + num_inverted_wingers,
        "Attacker": num_goal_poachers + num_target_men
    }

    # Generate the squad using the generate_squad function
    squad = generate_squad(predictions, num_players_per_position, selected_roles)

    # Display the generated squad
    display_squad(squad)