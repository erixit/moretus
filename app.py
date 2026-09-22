"""
Streamlit application with SQLite database
"""

import streamlit as st
from database import Database
from team_manager import TeamManager
import pandas as pd
import os

# Initialize database
DB_PATH = "moretus.db"
db = Database(DB_PATH)

# Configure page
st.set_page_config(
    page_title="Moretus App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Moretus Application")
st.markdown("---")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Players", "Team Selection", "Data Manager", "Analytics", "Settings"]
)

if page == "Home":
    st.header("Welcome to Moretus")
    st.write("""
    This is a Streamlit application with SQLite database integration.
    Use the navigation menu to explore different sections.
    """)
    
    # Display database info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📁 Database: {DB_PATH}")
    with col2:
        st.info(f"✅ Database Status: Connected")

elif page == "Players":
    st.header("♟️ Chess Players Database")
    st.markdown("Read-only view of all registered chess players")
    
    try:
        # Fetch all players from database
        players = db.fetch_all("""
            SELECT id, club, idnumber, name, cluborig, rating, f_elo, b_elo, titular
            FROM playerlist
            ORDER BY rating DESC
        """)
        
        if players:
            # Convert to DataFrame for better display
            df = pd.DataFrame(players)
            
            # Rename columns for display
            df = df.rename(columns={
                'id': 'ID',
                'club': 'Club',
                'idnumber': 'ID Number',
                'name': 'Name',
                'cluborig': 'Original Club',
                'rating': 'Rating',
                'f_elo': 'FIDE ELO',
                'b_elo': 'B ELO',
                'titular': 'Titular'
            })
            
            # Display statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Players", len(df))
            with col2:
                st.metric("Highest Rating", df['Rating'].max())
            with col3:
                st.metric("Average Rating", f"{df['Rating'].mean():.0f}")
            with col4:
                st.metric("Lowest Rating", df['Rating'].min())
            
            st.markdown("---")
            
            # Display the table
            st.subheader("Player List")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn(width="small"),
                    "Club": st.column_config.NumberColumn(width="small"),
                    "ID Number": st.column_config.NumberColumn(width="medium"),
                    "Name": st.column_config.TextColumn(width="large"),
                    "Original Club": st.column_config.NumberColumn(width="small"),
                    "Rating": st.column_config.NumberColumn(width="medium"),
                    "FIDE ELO": st.column_config.NumberColumn(width="medium"),
                    "B ELO": st.column_config.NumberColumn(width="medium"),
                    "Titular": st.column_config.TextColumn(width="medium"),
                }
            )
            
            # Export option
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="playerlist.csv",
                    mime="text/csv"
                )
            
            with col2:
                json = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json,
                    file_name="playerlist.json",
                    mime="application/json"
                )
        else:
            st.warning("No players found in database")
            
    except Exception as e:
        st.error(f"Error loading players: {e}")

elif page == "Team Selection":
    st.header("🏆 Team Selection")
    st.markdown("Select 6 players to create your team")
    
    try:
        # Fetch all players for selection sorted by rating
        all_players = db.fetch_all("""
            SELECT id, name, rating, f_elo
            FROM playerlist
            ORDER BY rating DESC
        """)
        
        if all_players:
            # Create a session state dictionary for player selections
            if 'player_selections' not in st.session_state:
                st.session_state.player_selections = {p['id']: False for p in all_players}
            
            # Ensure all players are in the selection dict
            for player in all_players:
                player_id = player['id']
                if player_id not in st.session_state.player_selections:
                    st.session_state.player_selections[player_id] = False
            
            # Create a reset counter to force checkbox state refresh
            if 'reset_counter' not in st.session_state:
                st.session_state.reset_counter = 0
            
            # Create player selection interface
            st.subheader("Available Players")
            
            # Display players in columns for better layout
            cols = st.columns(3)
            col_idx = 0
            
            for player in all_players:
                player_name = f"{player['name']} ({player['rating']} Rating)"
                player_id = player['id']
                
                with cols[col_idx % 3]:
                    is_selected = st.checkbox(
                        player_name,
                        value=st.session_state.player_selections.get(player_id, False),
                        key=f"player_{player_id}_{st.session_state.reset_counter}"
                    )
                    
                    # Update session state
                    st.session_state.player_selections[player_id] = is_selected
                
                col_idx += 1
            
            st.markdown("---")
            
            # Compute selected players list
            selected_players = [
                player_id for player_id, selected in st.session_state.player_selections.items()
                if selected
            ]
            selected_count = len(selected_players)
            
            if selected_count == 6:
                st.success(f"✅ {selected_count}/6 players selected - Ready to create team!")
            elif selected_count > 6:
                st.error(f"⚠️ {selected_count}/6 players selected - Please deselect {selected_count - 6} player(s)")
            else:
                st.info(f"📋 {selected_count}/6 players selected - Select {6 - selected_count} more")
            
            # Create team buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("Standard Team", disabled=(selected_count != 6)):
                    if selected_count == 6:
                        # Fetch selected players data sorted by rating
                        placeholders = ','.join('?' * 6)
                        selected_players_data = db.fetch_all(f"""
                            SELECT id, name, rating, f_elo
                            FROM playerlist
                            WHERE id IN ({placeholders})
                            ORDER BY rating DESC
                        """, tuple(selected_players))
                        
                        # Create standard board assignment: [1, 2, 3, 4, 5, 6]
                        standard_config = list(range(1, 7))
                        
                        # Format team with board assignments
                        team_with_boards = TeamManager.format_team_assignment(
                            selected_players_data,
                            standard_config
                        )
                        
                        # Store in session state
                        st.session_state.created_team = team_with_boards
                        st.session_state.valid_team_count = 1  # Only one standard configuration
            
            with col2:
                if st.button("Hutsekluts Team", disabled=(selected_count != 6)):
                    if selected_count == 6:
                        # Fetch selected players data sorted by rating
                        placeholders = ','.join('?' * 6)
                        selected_players_data = db.fetch_all(f"""
                            SELECT id, name, rating, f_elo
                            FROM playerlist
                            WHERE id IN ({placeholders})
                            ORDER BY rating DESC
                        """, tuple(selected_players))
                        
                        # Calculate all valid team configurations and pick a random one
                        valid_configs = TeamManager.get_all_valid_assignments(6)
                        random_config = TeamManager.get_random_valid_assignment(6)
                        
                        # Format team with board assignments
                        team_with_boards = TeamManager.format_team_assignment(
                            selected_players_data, 
                            random_config
                        )
                        
                        # Store in session state
                        st.session_state.created_team = team_with_boards
                        st.session_state.valid_team_count = len(valid_configs)
            
            with col3:
                if st.button("🔄 Clear Selection"):
                    # Increment reset counter to force checkbox widgets to reset
                    st.session_state.reset_counter += 1
                    # Reset all selections to False
                    for player_id in st.session_state.player_selections:
                        st.session_state.player_selections[player_id] = False
                    st.rerun()
            
            # Display created team if exists
            if 'created_team' in st.session_state and st.session_state.created_team:
                st.markdown("---")
                st.subheader("📊 Your Team")
                
                # Display valid configurations count
                valid_count = st.session_state.get('valid_team_count', 0)
                st.info(f"✨ **{valid_count} possible valid team configurations** exist with these 6 players!")
                
                team_df = pd.DataFrame(st.session_state.created_team)
                team_df = team_df.rename(columns={
                    'id': 'ID',
                    'name': 'Name',
                    'rating': 'Rating',
                    'f_elo': 'FIDE ELO',
                    'rank': 'Strength Rank',
                    'board': 'Board Position'
                })
                
                # Select columns to display
                display_cols = ['Board Position', 'Strength Rank', 'Name', 'Rating', 'FIDE ELO']
                team_df = team_df[display_cols]
                
                # Display team statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Team Size", len(team_df))
                with col2:
                    st.metric("Avg Rating", f"{team_df['Rating'].mean():.0f}")
                with col3:
                    st.metric("Total Rating", f"{team_df['Rating'].sum()}")
                with col4:
                    st.metric("Strongest Player", f"{team_df['Rating'].max()}")
                
                st.markdown("")
                st.dataframe(
                    team_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Board Position": st.column_config.NumberColumn(width="small"),
                        "Strength Rank": st.column_config.NumberColumn(width="small"),
                        "Name": st.column_config.TextColumn(width="medium"),
                        "Rating": st.column_config.NumberColumn(width="small"),
                        "FIDE ELO": st.column_config.NumberColumn(width="small"),
                    }
                )
                
                # Show rule compliance
                st.markdown("---")
                st.subheader("✅ Rule Compliance Check")
                
                rule_info = []
                for _, player in team_df.iterrows():
                    rank = player['Strength Rank']
                    board = player['Board Position']
                    offset = board - rank
                    allowed_boards = TeamManager.get_allowed_boards(rank, 6)
                    status = "✅" if board in allowed_boards else "❌"
                    rule_info.append({
                        "Player": f"{player['Name']}",
                        "Strength Rank": rank,
                        "Board Position": board,
                        "Offset": f"{offset:+d}",
                        "Allowed Range": f"[{min(allowed_boards)}-{max(allowed_boards)}]",
                        "Status": status
                    })
                
                rule_df = pd.DataFrame(rule_info)
                st.dataframe(
                    rule_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Player": st.column_config.TextColumn(width="medium"),
                        "Strength Rank": st.column_config.NumberColumn(width="small"),
                        "Board Position": st.column_config.NumberColumn(width="small"),
                        "Offset": st.column_config.TextColumn(width="small"),
                        "Allowed Range": st.column_config.TextColumn(width="small"),
                        "Status": st.column_config.TextColumn(width="small"),
                    }
                )
                
                # Export options
                st.markdown("---")
                st.subheader("📥 Export Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = team_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Team as CSV",
                        data=csv,
                        file_name="team.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    json = team_df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Download Team as JSON",
                        data=json,
                        file_name="team.json",
                        mime="application/json"
                    )
        else:
            st.warning("No players available for team selection")
            
    except Exception as e:
        st.error(f"Error in team selection: {e}")

elif page == "Data Manager":
    st.header("Data Manager")
    
    tab1, tab2, tab3 = st.tabs(["View Data", "Add Data", "Delete Data"])
    
    with tab1:
        st.subheader("Current Data")
        # Example: Display data from database
        st.write("Data will be displayed here")
    
    with tab2:
        st.subheader("Add New Record")
        with st.form("add_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name")
            with col2:
                value = st.number_input("Value")
            
            submitted = st.form_submit_button("Add Record")
            if submitted and name:
                st.success(f"Added: {name} with value {value}")
    
    with tab3:
        st.subheader("Delete Records")
        st.warning("Delete functionality coming soon")

elif page == "Analytics":
    st.header("Analytics")
    st.write("Analytics dashboard coming soon")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", "0")
    with col2:
        st.metric("Last Updated", "N/A")
    with col3:
        st.metric("Status", "Active")

elif page == "Settings":
    st.header("Settings")
    st.write("Application settings coming soon")
    
    with st.form("settings_form"):
        debug_mode = st.checkbox("Debug Mode")
        auto_refresh = st.selectbox("Auto Refresh", ["Disabled", "5 seconds", "30 seconds", "1 minute"])
        
        if st.form_submit_button("Save Settings"):
            st.success("Settings saved!")

st.markdown("---")
st.caption("Moretus Application • Built with Streamlit & SQLite")
