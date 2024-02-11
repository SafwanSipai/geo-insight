import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

BASE_URL_V4 = "https://www.geoguessr.com/api/v4"
BASE_URL_V3 = "https://www.geoguessr.com/api/v3"

country_codes = {
    'ad': 'Andorra',
    'ae': 'United Arab Emirates',
    'af': 'Afghanistan',
    'ag': 'Antigua and Barbuda',
    'ai': 'Anguilla',
    'al': 'Albania',
    'am': 'Armenia',
    'ao': 'Angola',
    'aq': 'Antarctica',
    'ar': 'Argentina',
    'as': 'American Samoa',
    'at': 'Austria',
    'au': 'Australia',
    'aw': 'Aruba',
    'ax': 'Åland Islands',
    'az': 'Azerbaijan',
    'ba': 'Bosnia and Herzegovina',
    'bb': 'Barbados',
    'bd': 'Bangladesh',
    'be': 'Belgium',
    'bf': 'Burkina Faso',
    'bg': 'Bulgaria',
    'bh': 'Bahrain',
    'bi': 'Burundi',
    'bj': 'Benin',
    'bl': 'Saint Barthélemy',
    'bm': 'Bermuda',
    'bn': 'Brunei Darussalam',
    'bo': 'Bolivia (Plurinational State of)',
    'bq': 'Bonaire, Sint Eustatius and Saba',
    'br': 'Brazil',
    'bs': 'Bahamas',
    'bt': 'Bhutan',
    'bv': 'Bouvet Island',
    'bw': 'Botswana',
    'by': 'Belarus',
    'bz': 'Belize',
    'ca': 'Canada',
    'cc': 'Cocos (Keeling) Islands',
    'cd': 'Congo (Democratic Republic of the)',
    'cf': 'Central African Republic',
    'cg': 'Congo',
    'ch': 'Switzerland',
    'ci': 'Côte d\'Ivoire',
    'ck': 'Cook Islands',
    'cl': 'Chile',
    'cm': 'Cameroon',
    'cn': 'China',
    'co': 'Colombia',
    'cr': 'Costa Rica',
    'cu': 'Cuba',
    'cv': 'Cabo Verde',
    'cw': 'Curaçao',
    'cx': 'Christmas Island',
    'cy': 'Cyprus',
    'cz': 'Czechia',
    'de': 'Germany',
    'dj': 'Djibouti',
    'dk': 'Denmark',
    'dm': 'Dominica',
    'do': 'Dominican Republic',
    'dz': 'Algeria',
    'ec': 'Ecuador',
    'ee': 'Estonia',
    'eg': 'Egypt',
    'eh': 'Western Sahara',
    'er': 'Eritrea',
    'es': 'Spain',
    'et': 'Ethiopia',
    'fi': 'Finland',
    'fj': 'Fiji',
    'fk': 'Falkland Islands (Malvinas)',
    'fm': 'Micronesia (Federated States of)',
    'fo': 'Faroe Islands',
    'fr': 'France',
    'ga': 'Gabon',
    'gb': 'United Kingdom of Great Britain and Northern Ireland',
    'gd': 'Grenada',
    'ge': 'Georgia',
    'gf': 'French Guiana',
    'gg': 'Guernsey',
    'gh': 'Ghana',
    'gi': 'Gibraltar',
    'gl': 'Greenland',
    'gm': 'Gambia',
    'gn': 'Guinea',
    'gp': 'Guadeloupe',
    'gq': 'Equatorial Guinea',
    'gr': 'Greece',
    'gs': 'South Georgia and the South Sandwich Islands',
    'gt': 'Guatemala',
    'gu': 'Guam',
    'gw': 'Guinea-Bissau',
    'gy': 'Guyana',
    'hk': 'Hong Kong',
    'hm': 'Heard Island and McDonald Islands',
    'hn': 'Honduras',
    'hr': 'Croatia',
    'ht': 'Haiti',
    'hu': 'Hungary',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'il': 'Israel',
    'im': 'Isle of Man',
    'in': 'India',
    'io': 'British Indian Ocean Territory',
    'iq': 'Iraq',
    'ir': 'Iran (Islamic Republic of)',
    'is': 'Iceland',
    'it': 'Italy',
    'je': 'Jersey',
    'jm': 'Jamaica',
    'jo': 'Jordan',
    'jp': 'Japan',
    'ke': 'Kenya',
    'kg': 'Kyrgyzstan',
    'kh': 'Cambodia',
    'ki': 'Kiribati',
    'km': 'Comoros',
    'kn': 'Saint Kitts and Nevis',
    'kp': 'Korea (Democratic People\'s Republic of)',
    'kr': 'Korea (Republic of)',
    'kw': 'Kuwait',
    'ky': 'Cayman Islands',
    'kz': 'Kazakhstan',
    'la': 'Lao People\'s Democratic Republic',
    'lb': 'Lebanon',
    'lc': 'Saint Lucia',
    'li': 'Liechtenstein',
    'lk': 'Sri Lanka',
    'lr': 'Liberia',
    'ls': 'Lesotho',
    'lt': 'Lithuania',
    'lu': 'Luxembourg',
    'lv': 'Latvia',
    'ly': 'Libya',
    'ma': 'Morocco',
    'mc': 'Monaco',
    'md': 'Moldova (Republic of)',
    'me': 'Montenegro',
    'mf': 'Saint Martin (French part)',
    'mg': 'Madagascar',
    'mh': 'Marshall Islands',
    'mk': 'North Macedonia',
    'ml': 'Mali',
    'mm': 'Myanmar',
    'mn': 'Mongolia',
    'mo': 'Macao',
    'mp': 'Northern Mariana Islands',
    'mq': 'Martinique',
    'mr': 'Mauritania',
    'ms': 'Montserrat',
    'mt': 'Malta',
    'mu': 'Mauritius',
    'mv': 'Maldives',
    'mw': 'Malawi',
    'mx': 'Mexico',
    'my': 'Malaysia',
    'mz': 'Mozambique',
    'na': 'Namibia',
    'nc': 'New Caledonia',
    'ne': 'Niger',
    'nf': 'Norfolk Island',
    'ng': 'Nigeria',
    'ni': 'Nicaragua',
    'nl': 'Netherlands',
    'no': 'Norway',
    'np': 'Nepal',
    'nr': 'Nauru',
    'nu': 'Niue',
    'nz': 'New Zealand',
    'om': 'Oman',
    'pa': 'Panama',
    'pe': 'Peru',
    'pf': 'French Polynesia',
    'pg': 'Papua New Guinea',
    'ph': 'Philippines',
    'pk': 'Pakistan',
    'pl': 'Poland',
    'pm': 'Saint Pierre and Miquelon',
    'pn': 'Pitcairn',
    'pr': 'Puerto Rico',
    'ps': 'Palestine, State of',
    'pt': 'Portugal',
    'pw': 'Palau',
    'py': 'Paraguay',
    'qa': 'Qatar',
    're': 'Réunion',
    'ro': 'Romania',
    'rs': 'Serbia',
    'ru': 'Russian Federation',
    'rw': 'Rwanda',
    'sa': 'Saudi Arabia',
    'sb': 'Solomon Islands',
    'sc': 'Seychelles',
    'sd': 'Sudan',
    'se': 'Sweden',
    'sg': 'Singapore',
    'sh': 'Saint Helena, Ascension and Tristan da Cunha',
    'si': 'Slovenia',
    'sj': 'Svalbard and Jan Mayen',
    'sk': 'Slovakia',
    'sl': 'Sierra Leone',
    'sm': 'San Marino',
    'sn': 'Senegal',
    'so': 'Somalia',
    'sr': 'Suriname',
    'ss': 'South Sudan',
    'st': 'Sao Tome and Principe',
    'sv': 'El Salvador',
    'sx': 'Sint Maarten (Dutch part)',
    'sy': 'Syrian Arab Republic',
    'sz': 'Eswatini',
    'tc': 'Turks and Caicos Islands',
    'td': 'Chad',
    'tf': 'French Southern Territories',
    'tg': 'Togo',
    'th': 'Thailand',
    'tj': 'Tajikistan',
    'tk': 'Tokelau',
    'tl': 'Timor-Leste',
    'tm': 'Turkmenistan',
    'tn': 'Tunisia',
    'to': 'Tonga',
    'tr': 'Turkey',
    'tt': 'Trinidad and Tobago',
    'tv': 'Tuvalu',
    'tw': 'Taiwan, Province of China',
    'tz': 'Tanzania, United Republic of',
    'ua': 'Ukraine',
    'ug': 'Uganda',
    'um': 'United States Minor Outlying Islands',
    'us': 'United States of America',
    'uy': 'Uruguay',
    'uz': 'Uzbekistan',
    'va': 'Holy See',
    'vc': 'Saint Vincent and the Grenadines',
    've': 'Venezuela (Bolivarian Republic of)',
    'vg': 'Virgin Islands (British)',
    'vi': 'Virgin Islands (U.S.)',
    'vn': 'Viet Nam',
    'vu': 'Vanuatu',
    'wf': 'Wallis and Futuna',
    'ws': 'Samoa',
    'ye': 'Yemen',
    'yt': 'Mayotte',
    'za': 'South Africa',
    'zm': 'Zambia',
    'zw': 'Zimbabwe',
}

def get_session(ncfa):
    session = requests.Session()
    session.cookies.set("_ncfa", ncfa, domain="www.geoguessr.com")
    return session

def get_game_tokens(session):
    game_tokens = []
    pagination_token = None
    while True:
        response = session.get(f"{BASE_URL_V4}/feed/private", params={'paginationToken': pagination_token})
        pagination_token = entries = response.json()['paginationToken']
        entries = response.json()['entries']
        for entry in entries:
            payload_json = json.loads(entry['payload'])
            for payload in payload_json:
                try:
                    # print(payload['payload'])
                    if payload['payload']['gameMode'] == 'Standard':
                        game_tokens.append(payload['payload']['gameToken']) 
                except Exception as e:
                    continue 
        if not pagination_token:
            break
    return game_tokens

def get_stats(session, game_tokens, number_of_games, progress_bar):
    # moving stats
    mov_total_score = 0
    mov_total_distance_km = 0
    mov_total_time_sec = 0
    mov_round_wise_points = []
    mov_round_wise_time = []
    mov_guessed_locations = []
    mov_points_lost_per_country = dict({})
    mov_distance_per_country = dict({})
    mov_countries = dict({})
    mov_number_of_games = 0
    mov_number_of_rounds = 0
    
    # no-moving stats
    no_mov_total_score = 0
    no_mov_total_distance_km = 0
    no_mov_total_time_sec = 0
    no_mov_round_wise_points = []
    no_mov_round_wise_time = []
    no_mov_guessed_locations = []
    no_mov_points_lost_per_country = dict({})
    no_mov_distance_per_country = dict({})
    no_mov_countries = dict({})
    no_mov_number_of_games = 0
    no_mov_number_of_rounds = 0
    
    # nmpz stats
    nmpz_total_score = 0
    nmpz_total_distance_km = 0
    nmpz_total_time_sec = 0
    nmpz_round_wise_points = []
    nmpz_round_wise_time = []
    nmpz_guessed_locations = []
    nmpz_points_lost_per_country = dict({})
    nmpz_distance_per_country = dict({})
    nmpz_countries = dict({})
    nmpz_number_of_games = 0
    nmpz_number_of_rounds = 0
    
    for i, token in enumerate(game_tokens[:number_of_games]):
        try:
            game = session.get(f"{BASE_URL_V3}/games/{token}").json() 
            
            if not game['forbidMoving'] and not game['forbidZooming'] and not game['forbidRotating']: # moving
                mov_number_of_games += 1
                mov_total_score += float(game['player']['totalScore']['amount'])
                mov_total_time_sec += float(game['player']['totalTime'])
                for actual, guess in zip(game['rounds'], game['player']['guesses']):
                    mov_number_of_rounds += 1
                    mov_round_wise_time.append(guess['time'])
                    mov_round_wise_points.append(int(guess['roundScore']['amount'])) 
                    
                    country_code = actual['streakLocationCode']
                    round_score = float(guess['roundScoreInPoints'])
                    round_distance_km = float(guess['distance']['meters']['amount'])
                    mov_total_distance_km += round_distance_km
                    mov_guessed_locations.append({'lat': guess['lat'],
                                                  'lng': guess['lng'],
                                                  'score': guess['roundScoreInPoints']})
                    
                    if country_code not in mov_points_lost_per_country:
                        mov_points_lost_per_country[country_code] = int(5000 - round_score)
                        mov_distance_per_country[country_code] = int(round_distance_km)
                        mov_countries[country_code] = 1
                    else:
                        mov_points_lost_per_country[country_code] += int(5000 - round_score)
                        mov_distance_per_country[country_code] += int(round_distance_km)
                        mov_countries[country_code] += 1
                        
            elif game['forbidMoving'] and not game['forbidZooming'] and not game['forbidRotating']: # no-moving
                no_mov_number_of_games += 1
                no_mov_total_score += float(game['player']['totalScore']['amount'])
                no_mov_total_time_sec += float(game['player']['totalTime'])
                for actual, guess in zip(game['rounds'], game['player']['guesses']):
                    no_mov_number_of_rounds += 1
                    no_mov_round_wise_time.append(guess['time'])
                    no_mov_round_wise_points.append(int(guess['roundScore']['amount'])) 
                    
                    country_code = actual['streakLocationCode']
                    round_score = float(guess['roundScoreInPoints'])
                    round_distance_km = float(guess['distance']['meters']['amount'])
                    no_mov_total_distance_km += round_distance_km
                    no_mov_guessed_locations.append({'lat': guess['lat'],
                                                     'lng': guess['lng'],
                                                     'score': guess['roundScoreInPoints']})
                    
                    if country_code not in no_mov_points_lost_per_country:
                        no_mov_points_lost_per_country[country_code] = int(5000 - round_score)
                        no_mov_distance_per_country[country_code] = int(round_distance_km)
                        no_mov_countries[country_code] = 1
                    else:
                        no_mov_points_lost_per_country[country_code] += int(5000 - round_score)
                        no_mov_distance_per_country[country_code] += int(round_distance_km)
                        no_mov_countries[country_code] += 1
                        
            elif game['forbidMoving'] and game['forbidZooming'] and game['forbidRotating']: # nmpz
                
                nmpz_number_of_games += 1
                nmpz_total_score += float(game['player']['totalScore']['amount'])
                nmpz_total_time_sec += float(game['player']['totalTime'])
                for actual, guess in zip(game['rounds'], game['player']['guesses']):
                    nmpz_number_of_rounds += 1
                    nmpz_round_wise_time.append(guess['time'])
                    nmpz_round_wise_points.append(int(guess['roundScore']['amount'])) 
                    
                    country_code = actual['streakLocationCode']
                    round_score = float(guess['roundScoreInPoints'])
                    round_distance_km = float(guess['distance']['meters']['amount'])
                    nmpz_total_distance_km += round_distance_km
                    nmpz_guessed_locations.append({'lat': guess['lat'],
                                                   'lng': guess['lng'],
                                                   'score': guess['roundScoreInPoints']})
                    
                    if country_code not in no_mov_points_lost_per_country:
                        nmpz_points_lost_per_country[country_code] = int(5000 - round_score)
                        nmpz_distance_per_country[country_code] = int(round_distance_km)
                        nmpz_countries[country_code] = 1
                    else:
                        nmpz_points_lost_per_country[country_code] += int(5000 - round_score)
                        nmpz_distance_per_country[country_code] += int(round_distance_km)
                        nmpz_countries[country_code] += 1
                        
        except Exception as e:
            continue
        finally:
            percent_complete = int(i * 100 / number_of_games)
            progress_bar.progress(percent_complete, f'Analyzing... ({percent_complete}%)')
    
    return {
        'moving': {'average_score': int(mov_total_score/mov_number_of_games) if mov_number_of_games else 0,
                   'average_distance': int(mov_total_distance_km/mov_number_of_games) if mov_number_of_games else 0,
                   'average_time': int(mov_total_time_sec/mov_number_of_games) if mov_number_of_games else 0,
                   'round_wise_points': mov_round_wise_points,
                   'round_wise_time': mov_round_wise_time,
                   'points_lost_per_country': mov_points_lost_per_country,
                   'distance_per_country': mov_distance_per_country,
                   'number_of_games': mov_number_of_games,
                   'number_of_rounds': mov_number_of_rounds,
                   'guessed_locations': mov_guessed_locations,
                   'countries': mov_countries},
        'no-moving': {'average_score': int(no_mov_total_score/no_mov_number_of_games) if no_mov_number_of_games else 0,
                      'average_distance': int(no_mov_total_distance_km/no_mov_number_of_games) if no_mov_number_of_games else 0,
                      'average_time': int(no_mov_total_time_sec/no_mov_number_of_games) if no_mov_number_of_games else 0,
                      'round_wise_points': no_mov_round_wise_points,
                      'round_wise_time': no_mov_round_wise_time,
                      'points_lost_per_country': no_mov_points_lost_per_country,
                      'distance_per_country': no_mov_distance_per_country,
                      'number_of_games': no_mov_number_of_games,
                      'number_of_rounds': no_mov_number_of_rounds,
                      'guessed_locations': no_mov_guessed_locations,
                      'countries': no_mov_countries},
        'nmpz': {'average_score': int(nmpz_total_score/nmpz_number_of_games) if nmpz_number_of_games else 0,
                 'average_distance': int(nmpz_total_distance_km/nmpz_number_of_games) if nmpz_number_of_games else 0,
                 'average_time': int(nmpz_total_time_sec/nmpz_number_of_games) if nmpz_number_of_games else 0,
                 'round_wise_points': nmpz_round_wise_points,
                 'round_wise_time': nmpz_round_wise_time,
                 'points_lost_per_country': nmpz_points_lost_per_country,
                 'distance_per_country': nmpz_distance_per_country,
                 'number_of_games': nmpz_number_of_games,
                 'number_of_rounds': nmpz_number_of_rounds,
                 'guessed_locations': nmpz_guessed_locations,
                 'countries': nmpz_countries}
    }  

def country_code_to_name(df):
    df['Country'] = df['Country'].apply(lambda x:country_codes[x] if x else None)
    return df

def plot_points_vs_time(stats):
    fig, ax = plt.subplots()
    y_ticks = [0, 1000, 2000, 3000, 4000, 5000]
    times = []
    points = []
    for time, point in zip(stats['round_wise_time'], stats['round_wise_points']):
        if time < 150:
            times.append(time)
            points.append(point)
            
    ax.scatter(times, points, marker='.', color='b')
    ax.set_yticks(y_ticks)
    ax.set_xlabel('Round Time (s)')
    ax.set_ylabel('Points')
    ax.set_title('Points vs Time')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    return fig

def get_most_and_least_data(stats, type):
    key_mapping = {'points': {'stat_name': 'points_lost_per_country',
                              'col_name': ['Country', 'Points Lost']},
                   'distance': {'stat_name': 'distance_per_country',
                                'col_name': ['Country', 'Total Distance (KM)']}}
    
    stat_name = key_mapping[type]['stat_name']
    col_name = key_mapping[type]['col_name']
    
    top_n = 5 if len(stats) > 5 else len(stats)
    desc_per_country = sorted(stats[stat_name].items(), key=lambda x: x[1], reverse=True)[:top_n]
    asc_per_country = sorted(stats[stat_name].items(), key=lambda x: x[1], reverse=True)[-top_n:]

    least_per_country = pd.DataFrame(asc_per_country, columns=col_name)
    most_per_country = pd.DataFrame(desc_per_country, columns=col_name)
    
    most_per_country = country_code_to_name(most_per_country)
    least_per_country = country_code_to_name(least_per_country)
    
    return most_per_country, least_per_country

def points_histogram(stats):

    buckets = [0, 1000, 2000, 3000, 4000, 5000]
    x_tick_labels = ['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000']

    # Count the points falling into each bucket
    counts, _ = np.histogram(stats['round_wise_points'], bins=buckets)

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.bar(buckets[:-1], counts, width=1000)

    # Customize the plot (optional)
    ax.set_xlabel('Points Range')
    ax.set_ylabel('Count')
    ax.set_title('Points Distribution')
    ax.set_xticks(ticks=buckets[:-1], labels=x_tick_labels)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')
    
    return fig

def plot_countries_bar_chart(stats):

    top_n = 10 if len(stats['countries']) > 10 else len(stats['countries'])
    
    new_stats = {country_codes[key]: value for key, value in stats['countries'].items() if key}
    
    sorted_data = dict(sorted(new_stats.items(), key=lambda item: item[1], reverse=True)[:top_n])

    fig, ax = plt.subplots()
    
    ax.bar(sorted_data.keys(), sorted_data.values())
    ax.set_xlabel('Country')
    ax.set_ylabel('Count')
    ax.set_title('Most frequently occurring countries')
    ax.set_xticks(ax.get_xticks(), labels=ax.get_xticklabels(), rotation=45, fontsize='x-small')
    
    return fig

def plot_guessed_locations(guessed_locations):
    guessed_lat = []
    guessed_lng = []
    round_scores = []
    
    for guessed_loc in guessed_locations:
        guessed_lat.append(guessed_loc['lat'])
        guessed_lng.append(guessed_loc['lng'])
        round_scores.append(guessed_loc['score'])
        
    guessed_df = pd.DataFrame({'lat': guessed_lat,
                               'lng': guessed_lng,
                               'score': round_scores})
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    guessed_geometry = [Point(xy) for xy in zip(guessed_df['lng'], guessed_df['lat'])]
    guessed_gdf = GeoDataFrame(guessed_df, geometry=guessed_geometry)
    ax = guessed_gdf.plot(ax=world.plot(figsize=(10,10), color='lightblue'), marker='o', markersize=3,
                    cax='score', cmap='YlOrRd', vmin=0, vmax=5000)
    
    ax.set_title('Guessed Locations')
    ax.set_axis_off()
    fig = ax.get_figure()
    cax = fig.add_axes([0.1, 0.26, 0.8, 0.03])
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=5000))
    sm._A = []
    fig.colorbar(sm, cax=cax, orientation='horizontal', label='Score')
    return fig