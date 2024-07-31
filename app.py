import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import utils

st.title('GeoInsight')
st.write('''
GeoInsight is your ultimate companion for dissecting and understanding your GeoGuessr gameplay.
Dive into detailed analyses of your guesses, uncover patterns in your play style, 
and enhance your skills with valuable insights.
Explore your GeoGuessr games like never before!''')
st.divider()

ncfa_guide_url = 'https://github.com/SafwanSipai/geo-insight?tab=readme-ov-file#getting-your-_ncfa-cookie'

ncfa = st.text_input('Enter your NCFA cookie ([click here to obtain yours](%s))' % ncfa_guide_url, None)
if ncfa:
    with st.spinner(text='Fetching data...'):
        session = utils.get_session(ncfa)
        game_tokens = utils.get_game_tokens(session)

    default_number_of_games = 100 if len(game_tokens) > 100 else len(game_tokens)
    st.slider('How many games would you like to analyze? (400 games ~ 1 min analysis time)', 0, len(game_tokens), default_number_of_games,
              step=10, key='slider', 
              help='''Adjusting the slider value determines the number of your most recent games to analyze. 
                      For instance, selecting '50' will analyze your fifty most recent games. 
                      Please note that higher values will increase processing time accordingly.''')
    
    button = st.button('Analyze')
    
    if button:
        progress_bar = st.progress(0)
        stats = utils.get_stats(session, game_tokens, st.session_state.slider, progress_bar)
        mov_stats = stats['moving']
        no_mov_stats = stats['no-moving']
        nmpz_stats = stats['nmpz']
        
        def plot_and_display_data(stats, label):
            # Extracting most and least stats for points and distances per country
            most_pts, least_pts = utils.get_most_and_least_data(stats, type='points')
            most_dist, least_dist = utils.get_most_and_least_data(stats, type='distance')

            # Plotting figures
            points_vs_time_fig = utils.plot_points_vs_time(stats)
            points_hist_fig = utils.points_histogram(stats)
            countries_bar_fig = utils.plot_countries_bar_chart(stats)
            guessed_loc_fig = utils.plot_guessed_locations(stats['guessed_locations'])

            # Displaying data and figures in the corresponding tab
            with label:
                col1, col2 = st.columns(2)
                col1.metric('Total Games', str(stats['number_of_games']))
                col2.metric('Total Rounds', str(stats['number_of_rounds']))

                col1, col2, col3 = st.columns(3)
                col1.metric('Average Points', str(stats['average_score']))
                col2.metric('Average Distance', str(stats['average_distance']) + ' KM')
                col3.metric('Average Game Time', str(stats['average_time']) + ' seconds')

                st.write('Points lost per country - Least vs Most')
                col1, col2 = st.columns(2)
                col1.dataframe(least_pts[::-1], hide_index=True)
                col2.dataframe(most_pts, hide_index=True)

                st.write('Distance per country - Least vs Most')
                col1, col2 = st.columns(2)
                col1.dataframe(least_dist[::-1], hide_index=True)
                col2.dataframe(most_dist, hide_index=True)

                st.pyplot(countries_bar_fig)
                st.pyplot(points_vs_time_fig)
                st.pyplot(points_hist_fig)
                st.pyplot(guessed_loc_fig)

        progress_bar.empty()
        
        st.header('Singleplayer Games')
        mov, no_mov, nmpz = st.tabs(['Moving', 'No moving', 'NMPZ'])
        
        plot_and_display_data(mov_stats, mov)
        plot_and_display_data(no_mov_stats, no_mov)
        plot_and_display_data(nmpz_stats, nmpz)