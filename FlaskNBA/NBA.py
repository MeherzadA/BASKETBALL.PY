from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup
from schedule_functions import getCurrent
from image_functions import deleteImages, getText
from graph_functions import shootingRadar, defenseRadar
import os
import requests

app = Flask(__name__)



@app.route('/')
@app.route('/home')
@app.route('/search')
def home_page():
    return render_template('home.html')

@app.route('/UpcomingGames', methods = ['GET'])
def upcoming_games():
    # defaultDay = 0
    team_away_list = []
    team_home_list = []
    time_list = []
    location_list = []
    score_list = []
    schedule_list_of_dict = []


    current, defaultDay = getCurrent()
    day = current.strftime("%A")
    month = current.strftime("%B")
    number = current.strftime("%d")
    year = current.strftime("%Y")
    dateString = f"{day}, {month} {number}, {year}"



    current_date_link = str(current).replace('-', '')
    schedule_scraping_page = requests.get(f'https://www.cbssports.com/nba/schedule/{current_date_link}/').text
    scheduleLink = f'https://www.cbssports.com/nba/schedule/{current_date_link}/'

    soup_schedule = BeautifulSoup(schedule_scraping_page, 'lxml')



    game_rows = soup_schedule.find_all('tr', class_='TableBase-bodyTr')

    print(game_rows)
    print()

    for i in game_rows:
        TeamNames = i.find_all('span', class_ = 'TeamName')
        print(TeamNames)
        print()
        TeamLogos = i.find_all('img', class_ = 'TeamLogo-image')
        print(TeamLogos)
        print()
        tipoff = i.find_all('div', class_='CellGame')
        print(tipoff)
        print()
        location = i.find_all('td',  attrs={'style': ' min-width: 120px; width: 20%;'})
        print(location)
        print()
        if location == []:
            location_list.append('Game Over!')



        for index, (teams, logos) in enumerate(zip(TeamNames, TeamLogos)):
            print(teams.text)
            if index % 2 == 0:
                team_away_list.append([teams.text, logos['data-lazy']])
            elif index % 1 == 0:
                team_home_list.append([teams.text, logos['data-lazy']])

        for tipoff in tipoff:
            if 'pm' in tipoff.text or 'am' in tipoff.text:
                time_list.append([tipoff.text.strip()])
                score_list.append(['Game Not Yet Started!'])
            else:
                if '1st' in tipoff.text or '2nd' in tipoff.text or '3rd' in tipoff.text or '4th' in tipoff.text:
                    tipoff = (tipoff.text.strip().replace(',', ' ║').replace('-', '║').replace('NBAt', '').replace('ESPN', '') + " Q.").split()
                else:
                    tipoff = (tipoff.text.strip().replace('-', ' ║').replace('OT', '') + " ║Final").split()
                tipoff.insert(1, ':')
                tipoff.insert(5, ':')

                score_list.append([' '.join(tipoff)])


                time_list.append(['Game Started!'])
        for location in location:
            if 'Tickets' in location.text:
                pass
            else:
                location_list.append([location.text.strip()])


    for teamAway, teamHome, time, location, score in zip(team_away_list, team_home_list, time_list, location_list, score_list):
        schedule_dict = {'Away': teamAway, 'Home': teamHome, 'Tipoff Time': time, 'Location' : location, 'Score': score}
        schedule_dict_copy = schedule_dict.copy()
        if schedule_dict_copy['Location'] == 'Game Over!':
            schedule_dict_copy['Tipoff Time'] = ['Game Over!']
            schedule_dict_copy['Location'] = ''
        schedule_list_of_dict.append(schedule_dict_copy)
        schedule_dict.clear()



    winners = []
    for i in schedule_list_of_dict:
        if 'Final' in i['Score'][0]:
            winners.append(i['Score'][0].split()[0].replace('NY', "New York").replace('OKC', "Oklahoma City").replace('NO', "New Orleans").replace('LAC', "L.A. Clippers").replace('LAL', "L.A. Lakers").replace('BKN', "Brooklyn").replace('GS', "Golden St."))
        else:
            winners.append("N/A")

    return render_template('upcoming games.html', schedule = schedule_list_of_dict, winners = winners, zip = zip, len = len, date = dateString, page = defaultDay, scheduleLink = scheduleLink)



@app.route('/PlayerStats', methods = ["POST", "GET"])
def player_stats_page():

    deleteImages()

    query_name = request.form.get('player_name')

    if not query_name:
        no_player_found = "Please Enter a Valid Player Name!"
        return render_template('home.html', no_player_found=no_player_found)


        # Getting the first character of the last name of the user input:
    try:
        firstCharLastName = query_name.split()[1][0]
    except:
        no_player_found = "Please Enter a Valid Player Name!"
        return render_template('home.html', no_player_found=no_player_found)

    # making a request for the first player directory page on basketball reference website:
    player_dir = requests.get('https://www.basketball-reference.com/players/').text
    soup_player_dir = BeautifulSoup(player_dir, 'lxml')

    # Searching for the first occurence of the unordered list w/ the class of "page_index", which contains all the different last name characters from A-Z:
    last_names = soup_player_dir.find('ul', class_='page_index')

    # Goes through the entire unordered list above (the ul tag) and creates a new list with all of the li tags
    LastNameLinks = last_names.find_all('li', limit=26)

    # Loops through our LastNameLinks list which contains all our li tags:
    for links in LastNameLinks:
        try:
            # Grabs the ACTUAL href link from each anchor tag of 'links' (links meaning the variable we are using to store the values of our iteration through the LastNameLinks list)
            basic_link = links.a['href']

            # Checks to see if the firstCharLastName is equal to the anchor tag of 'links' (In this scenario the anchor tag will be one of the 26 characters of the alphabet!)
            if firstCharLastName.lower() == links.a.text.lower():
                playersLink = f"https://www.basketball-reference.com{basic_link}"
                print(f"Link to all players with the first character of their last name being {links.a.text}:")
                print(playersLink)
                break
        except TypeError:
            continue

    print(
        "==========================SECOND PAGE OF WEBSITE (WITH ALL PLAYER NAMES OF THAT LAST NAME STARTING CHARACTER! Example: https://www.basketball-reference.com/players/c/================")

    # making a request for the playersLink web adress created above using the user inputted info!
    player_names_website = requests.get(playersLink).text

    soup_player_names = BeautifulSoup(player_names_website, 'lxml')

    # Searches for all occurences of the 'tbody' tag, and stores them into a list:
    tbody_player_names = soup_player_names.find_all('tbody')

    # Loops through entire tbody list, and stores each 'tr' tag, which contains each row of all the players that are stored on this page:
    for rows in tbody_player_names:
        rows = rows.find_all("tr")

    # Goes through each name in rows list, and checks to see if it matches the original user input:
    for names in rows:
        player_name = names.th.a.text
        player_stats_link = f"https://www.basketball-reference.com{names.th.a['href']}"
        if query_name.lower() == player_name.lower():
            print(player_name)
            print(player_stats_link)
            break
    else:
        no_player_found = "Please Enter a Valid Player Name!"
        return render_template('home.html', no_player_found=no_player_found)

    print(
        "==========================THIRD PAGE OF WEBSITE (WITH ALL PLAYER STATS! Example: https://www.basketball-reference.com/players/c/curryst01.html================")

    # max(arg1, arg2, _args, key)aking a request for the player_stats_link web adress defined above using our program!
    player_stats = requests.get(player_stats_link).text
    soup_all_player_stats = BeautifulSoup(player_stats, 'lxml')

    # Finds the totals_table, which contains the career stats of the player in question:
    totals_table = soup_all_player_stats.find_all('div', class_='table_wrapper tabbed')

    # Retrieves the image of the player:
    try:
        player_image = soup_all_player_stats.find('div', class_='media-item').img['src']
        print("IMAGE:")
        print(player_image)
    except:
        player_image = ''

    print()

    # Retrieves the stat names/headers for the entire table --> uses index[1] since that is always the position of the career total values for every player
    # NOTE:(There is some stuff I did below that I won't explain but it was vital to do since

    # Basketball reference totals table is kinda weird since they added tripl dubls stat but only for that table alone, and they include fully empty rows/columns ONLY FOR THE TOTALS TABLE which make everything 100x more annoying and if I didn't do it, the final output formatting gets really weird so just here:
    all_stats_names = totals_table[1].tr.text
    all_stats_names = all_stats_names.split()
    # print(f"Stat Names: {all_stats_names}")
    if 'Trp' in all_stats_names:
        all_stats_names.pop(-1)
        all_stats_names.pop(-1)
        all_stats_names.append(' ')
        all_stats_names.append('Trp Dbl')
        trp_db = True

    elif 'Trp' not in all_stats_names:
        all_stats_names = totals_table[1].tr.text
        all_stats_names = all_stats_names.split()
        trp_db = False

    # print(all_stats_names)
    # print(len(all_stats_names))

    # Gets all of the tr tagged rows and stores into a list:
    value_rows = totals_table[1].tfoot.find_all('tr')
    print()

    # print(len(h))

    tags_list = []
    stat_values = []

    for row in value_rows:
        # the th tagged values represent the season, and there is only one of them in each(in tagged form)
        tags_list.extend(row.find_all('th'))

        # The rest are all td tagged values, which represent the actual stats value (in tagged form, however)
        tags_list.append(row.find_all('td'))

    for j in tags_list:
        # Since tags_list is a list of list we need to iterate through it twice:
        for k in j:
            # Finally goes through each value in the tags_list and appends its .text form to a NEW stat_values list
            stat_values.append(k.text)


    CareerTotalList = []
    CareerTotalDict = {}
    # Since some players have played in both NBA and ABA, and have played a different number of seasons with different teams, there can be more than 1 row in the career totals area:
    # Thus, we need to tell the program how many times we want to iterate through the entire table --> Can accomplish this based on the calculation defined below:
    for i in range((len(stat_values) // len(all_stats_names)) + 1):

        # Now we iterate through each 'statName' and 'statValue' in their corresponding listL
        for statName, statValue in zip(all_stats_names, stat_values):
            if statName == ' ':
                pass
            else:
                # Will print out the statname and value so long as they are both non-white spaces!
                print(f"{statName}: {statValue}")
                CareerTotalDict[statName] = statValue
                # print(CareerTotalDict)

            # Since players can have multiple rows of stat values, the list will also be very long, so after each iteration of 32, (which is the number of total stats there can be in any one row)
            # The program will delete the first 32 elements of the stat_values list, and will then go onto the next full iteration and repeat the process
            if trp_db == True:
                if statName == 'Trp Dbl':
                    del stat_values[:32]
                    CareerTotalList.append(CareerTotalDict.copy())
                    CareerTotalDict.clear()
                    print()

                # Obviously, if there are no elements in the list, we want the loop  to stop running:
                    if len(stat_values) == 0:
                        break

                # Hard to explain, but becuase of those empty rows mentioned above, we need to do this step in order for the final formatting of everything to be correct!
                    elif stat_values[0] == '' and stat_values[1] == '':
                        stat_values.insert(0, '')
                    # print("asdding!!!")
                    # print("i: ", i)
            elif trp_db == False:
                if statName == 'PTS':
                    del stat_values[:30]
                    CareerTotalList.append(CareerTotalDict.copy())
                    CareerTotalDict.clear()
                    print()

                    if len(stat_values) == 0:
                        break
                    elif stat_values[0] == '' and stat_values[1] == '':
                        stat_values.insert(0, '')

    SeasonTotalList = []
    SeasonTotalDict = {}
    print("==========================Getting per season Totals:================")
    perSeason_table_header = totals_table[1].tbody.find_all('tr')

    perSeason_HTML_tags = []
    for i in perSeason_table_header:
        perSeason_HTML_tags.append(i.find_all('th'))
        perSeason_HTML_tags.append(i.find_all('td'))

    per_season_total_stats = []

    for j in perSeason_HTML_tags:
        for i in j:
            per_season_total_stats.append(i.text)

    print(per_season_total_stats)
    print()
    for i in range((len(per_season_total_stats) // len(all_stats_names)) + 1):

        # Now we iterate through each 'statName' and 'statValue' in their corresponding listL
        for statName, statValue in zip(all_stats_names, per_season_total_stats):
            if statName == ' ':
                pass
            else:
                # Will print out the statname and value so long as they are both non-white spaces!
                print(f"{statName}: {statValue}")
                SeasonTotalDict[statName] =  statValue

            # Since players can have multiple rows of stat values, the list will also be very long, so after each iteration of 32, (which is the number of total stats there can be in any one row)
            # The program will delete the first 32 elements of the stat_values list, and will then go onto the next full iteration and repeat the process
            if trp_db == True:
                if statName == 'Trp Dbl':
                    del per_season_total_stats[:32]
                    SeasonTotalList.append(SeasonTotalDict.copy())
                    SeasonTotalDict.clear()
                    print()
                    if len(stat_values) == 0:
                        break
                    elif stat_values[0] == '' and stat_values[1] == '':
                        stat_values.insert(0, '')

            elif trp_db == False:
                if statName == 'PTS':
                    del per_season_total_stats[:30]
                    SeasonTotalList.append(SeasonTotalDict.copy())
                    SeasonTotalDict.clear()
                    print()
                    if len(stat_values) == 0:
                        break
                    elif stat_values[0] == '' and stat_values[1] == '':
                        stat_values.insert(0, '')


    print(f"Career total list:\n{CareerTotalList}")
    print()
    print(f"Season total list:\n{SeasonTotalList}")

    # Creating the stat images for the players!
    getText(CareerTotalList, query_name)
    getText(SeasonTotalList, query_name)

    # Saving the images and storing them in a list, which we will iterate through in the html file associated with this function
    imageList = os.listdir(r'static/Images')
    imagelist = ['Images/' + image for image in imageList if image.endswith('.png')]


    # Creating the shooting & defense graphs for the players!
    shootingRadar(CareerTotalList, query_name)
    shootingRadar(SeasonTotalList, query_name)
    defenseRadar(CareerTotalList, query_name)
    defenseRadar(SeasonTotalList, query_name)

    # Saving the graphs and storing them in a list, which we will iterate through in the html file associated with this function
    RadarChartImages = os.listdir(r'static/Shooting Radar Charts')
    ShootingRadarChart = ['Shooting Radar Charts/' + radar for radar in RadarChartImages if radar.endswith('.png')]

    RadarChartImages2 = os.listdir(r'static/DRB, STL, BLK Radar Charts')
    DefenseRadarChart = ['DRB, STL, BLK Radar Charts/' + radar2 for radar2 in RadarChartImages2 if radar2.endswith('.png')]
    if request.method == 'POST':
        l1 = request.form.getlist('statCheckbox')
        l2 = request.form.getlist('statGraph')
        return render_template('PlayerStats.html', all_stats_names = all_stats_names, careerStats = CareerTotalList, seasonalStats = SeasonTotalList, query = query_name, imagelist = imagelist, player_image = player_image, zip = zip, enumerate = enumerate, ShootingRadarChart = ShootingRadarChart, DefenseRadarChart = DefenseRadarChart, player_stats_link = player_stats_link, l1=l1, l2=l2)

    return render_template('PlayerStats.html', all_stats_names = all_stats_names, careerStats = CareerTotalList, seasonalStats = SeasonTotalList, query = query_name, imagelist = imagelist, player_image = player_image, zip = zip, enumerate = enumerate, ShootingRadarChart = ShootingRadarChart, DefenseRadarChart = DefenseRadarChart, player_stats_link = player_stats_link)