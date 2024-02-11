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
        mov_stats= stats['moving']
        no_mov_stats= stats['no-moving']
        nmpz_stats= stats['nmpz']
        
        # plot points vs time graph
        mov_points_vs_time_fig = utils.plot_points_vs_time(mov_stats)
        no_mov_points_vs_time_fig = utils.plot_points_vs_time(no_mov_stats)
        nmpz_points_vs_time_fig = utils.plot_points_vs_time(nmpz_stats)

        # get most and least stats for points and distances per country
        mov_most_pts_lost_per_country, mov_least_pts_lost_per_country = utils.get_most_and_least_data(mov_stats, type='points')
        mov_most_dist_per_country, mov_least_dist_per_country = utils.get_most_and_least_data(mov_stats, type='distance')
        
        no_mov_most_pts_lost_per_country, no_mov_least_pts_lost_per_country = utils.get_most_and_least_data(no_mov_stats, type='points')
        no_mov_most_dist_per_country, no_mov_least_dist_per_country = utils.get_most_and_least_data(no_mov_stats, type='distance')
        
        nmpz_most_pts_lost_per_country, nmpz_least_pts_lost_per_country = utils.get_most_and_least_data(nmpz_stats, type='points')
        nmpz_most_dist_per_country, nmpz_least_dist_per_country = utils.get_most_and_least_data(nmpz_stats, type='distance')

        # plot points histogram
        mov_points_hist_fig = utils.points_histogram(mov_stats)
        no_mov_points_hist_fig = utils.points_histogram(no_mov_stats)
        nmpz_points_hist_fig = utils.points_histogram(nmpz_stats)
        
        # plot countries bar chart
        mov_countries_bar_fig = utils.plot_countries_bar_chart(mov_stats)
        no_mov_countries_bar_fig = utils.plot_countries_bar_chart(no_mov_stats)
        nmpz_countries_bar_fig = utils.plot_countries_bar_chart(nmpz_stats)
        
        # plot guessed locations
        mov_guessed_loc_fig = utils.plot_guessed_locations(mov_stats['guessed_locations'])
        no_mov_guessed_loc_fig = utils.plot_guessed_locations(no_mov_stats['guessed_locations'])
        nmpz_guessed_loc_fig = utils.plot_guessed_locations(nmpz_stats['guessed_locations'])

        progress_bar.empty()
        
        st.header('Singleplayer Games')
        mov, no_mov, nmpz = st.tabs(['Moving', 'No moving', 'NMPZ'])
        
        with mov:
            col1, col2 = st.columns(2)
            col1.metric('Total Games', str(mov_stats['number_of_games']))
            col2.metric('Total Rounds', str(mov_stats['number_of_rounds']))
            
            col1, col2, col3 = st.columns(3)
            col1.metric('Average Points', str(mov_stats['average_score']))
            col2.metric('Average Distance', str(mov_stats['average_distance']) + ' KM')
            col3.metric('Average Game Time', str(mov_stats['average_time']) + ' seconds')
            
            st.write('Points lost per country - Least vs Most')
            col1, col2 = st.columns(2)
            col1.dataframe(mov_least_pts_lost_per_country[::-1], hide_index=True)
            col2.dataframe(mov_most_pts_lost_per_country, hide_index=True)
            
            st.write('Distance per country - Least vs Most')
            col1, col2 = st.columns(2)
            col1.dataframe(mov_least_dist_per_country[::-1], hide_index=True)
            col2.dataframe(mov_most_dist_per_country, hide_index=True)
            
            st.pyplot(mov_countries_bar_fig)
            st.pyplot(mov_points_vs_time_fig)
            st.pyplot(mov_points_hist_fig)
            st.pyplot(mov_guessed_loc_fig)
        
        with no_mov:
            col1, col2 = st.columns(2)
            col1.metric('Total Games', str(no_mov_stats['number_of_games']))
            col2.metric('Total Rounds', str(no_mov_stats['number_of_rounds']))
            
            col1, col2, col3 = st.columns(3)
            col1.metric('Average Points', str(no_mov_stats['average_score']))
            col2.metric('Average Distance', str(no_mov_stats['average_distance']) + ' KM')
            col3.metric('Average Time', str(no_mov_stats['average_time']) + ' seconds')
            
            st.write('Points lost per country - Least vs Most')
            col1, col2 = st.columns(2)
            col1.dataframe(no_mov_least_pts_lost_per_country[::-1], hide_index=True)
            col2.dataframe(no_mov_most_pts_lost_per_country, hide_index=True)
            
            st.write('Distance per country - Least vs Most')
            col1, col2 = st.columns(2)
            col1.dataframe(no_mov_least_dist_per_country[::-1], hide_index=True)
            col2.dataframe(no_mov_most_dist_per_country, hide_index=True)
            
            st.pyplot(no_mov_countries_bar_fig)
            st.pyplot(no_mov_points_vs_time_fig)
            st.pyplot(no_mov_points_hist_fig)
            st.pyplot(no_mov_guessed_loc_fig)
            
        with nmpz:
            col1, col2 = st.columns(2)
            col1.metric('Total Games', str(nmpz_stats['number_of_games']))
            col2.metric('Total Rounds', str(nmpz_stats['number_of_rounds']))
            
            col1, col2, col3 = st.columns(3)
            col1.metric('Average Points', str(nmpz_stats['average_score']))
            col2.metric('Average Distance', str(nmpz_stats['average_distance']) + ' KM')
            col3.metric('Average Time', str(nmpz_stats['average_time']) + ' seconds')
            
            st.write('Points lost per country - Least vs Most')
            col1, col2 = st.columns(2)
            col1.dataframe(nmpz_least_pts_lost_per_country[::-1], hide_index=True)
            col2.dataframe(nmpz_most_pts_lost_per_country, hide_index=True)
            
            st.write('Distance per country - Least vs Most')
            col1, col2 = st.columns(2)
            col1.dataframe(nmpz_least_dist_per_country[::-1], hide_index=True)
            col2.dataframe(nmpz_most_dist_per_country, hide_index=True)
            
            st.pyplot(nmpz_countries_bar_fig)
            st.pyplot(nmpz_points_vs_time_fig)
            st.pyplot(nmpz_points_hist_fig)
            st.pyplot(nmpz_guessed_loc_fig)
            
            
            
            
            
        
    