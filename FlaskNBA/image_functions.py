import os
from PIL import Image, ImageFont, ImageDraw

img_NBA = Image.open(r'C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Images\NBA stats template.jpg')
img_ABA = Image.open(r'C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Images\ABA stats template.jpg')
img_default = Image.open(r'C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Images\default stats template.jpg')

font_season = ImageFont.truetype('Basketball.ttf', 175)
font_stats = ImageFont.truetype('Helvetica Black.ttf', 70)

image_save_path = r"C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Images"

def deleteImages():
    for images in os.listdir(r"C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Images"):
        if images.endswith('.png'):
            os.remove(os.path.join(r"C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Images", images))

    for radarChart in os.listdir(r"static/Shooting Radar Charts"):
        if radarChart.endswith('.png'):
            os.remove(os.path.join(r"static/Shooting Radar Charts", radarChart))

    for radarChart in os.listdir(r"static/DRB, STL, BLK Radar Charts"):
        if radarChart.endswith('.png'):
            os.remove(os.path.join(r"static/DRB, STL, BLK Radar Charts", radarChart))




def getText(stat_list, playerName):
    for i in stat_list:
        try:
            twoP = i['2P']
        except:
            twoP = "N/A"
        try:
            twoPA = i['2PA']
        except:
            twoPA = "N/A"
        try:
            twoPrec = i['2P%']
        except:
            twoPrec = "N/A"
        try:
            threeP = i['3P']
        except:
            threeP = "N/A"
        try:
            threePA = i['3PA']
        except:
            threePA = "N/A"
        try:
            threePrec = i['3P%']
        except:
            threePrec = "N/A"
        try:
            effective_FG_prec = i['eFG%']
        except:
            effective_FG_prec = "N/A"
        try:
            PF = i['PF']
        except:
            PF = "N/A"
        try:
            TOV = i['TOV']
        except:
            TOV = "N/A"
        try:
            TrpDbl = i['Trp Dbl']
        except:
            TrpDbl = "N/A"

        c1 = f"""
                Age: {i['Age']}
                Pos: {i['Pos']}
                G: {i['G']}
                GS: {i['GS']}
                MP: {i['MP']}
                FG: {i['FG']}
                FGA: {i['FGA']}
                FG%: {i['FG%']}
                3P: {threeP}
                """
        c2 = f"""
                3PA: {threePA}
                3P%: {threePrec}
                2P: {twoP}
                2PA: {twoPA}
                2P%: {twoPrec}
                eFG%: {effective_FG_prec}
                FT: {i['FT']}
                FTA: {i['FTA']}
                FT%: {i['FT%']}
                """

        c3 = f"""
                ORB: {i['ORB']}
                DRB: {i['DRB']}
                TRB: {i['TRB']}
                AST: {i['AST']}
                STL: {i['STL']}
                BLK: {i['BLK']}
                TOV: {TOV}
                PF: {PF}
                PTS: {i['PTS']}
                Trp Dbl: {TrpDbl}
                """
        if i['Lg'] == "NBA":
            copy = img_NBA.copy()
        elif i['Lg'] == "ABA":
            copy = img_ABA.copy()
        elif i['Lg'] != "NBA" and i['Lg'] != "ABA":
            copy = img_default.copy()
        W,H = imageSize(copy)
        # print("wiff::::")
        # print(W)
        # print()
        # season = i['Season']
        # print("ssn:")
        # print(seasonn)
        # print()
        # teamm = i['Tm']
        # print("tm:")
        # print(teamm)
        # leaguee = i['Lg']
        # print("LEAGUEEEEE:")
        # print(leaguee)
        # print()
        if i['Season'] != '' or i['Tm'] != '' or  i['Lg'] != '':
            title, season, team, league = getImageTitle(i['Season'], i['Tm'], i['Lg'])
            print("this is title:::")
            print(title)
            drawImg(c1, c2, c3, title, W, copy, playerName, season, team, league)
        else:
            continue
    # return getImageTitle(c1, c2, c3, i['Season'], i['Tm'], i['Lg'], copy)

    # return c1, c2, c3, copy

def imageSize(img):
    W,H = img.size
    return W,H


        # draw = ImageDraw.Draw(copy)


def getImageTitle(season, team, league):
    if season != '' and team != '':
        title = f"{season} ({team})"
        return title, season, team, league
    elif team == '':
        if season != '':
            if league == "TOT":
                title = f"{season} ({league}AL)"
                print("ITS OKAY")
                return title, season, team, league
            else:
                title = f"{season}"
                return title, season, team, league
        elif season == '' and league != '':
            title = f"Career ({league})"
            return title, season, team, league
    elif season == '' and team == '' and league == '':
        title = "test"
        return title, season, team, league





def drawImg(text1, text2, text3,title, W, imgCopy, query_name, season, team, league):
    draw = ImageDraw.Draw(imgCopy)
    w, h = draw.textsize(title, font=font_season)
    draw.text(xy=((W - w) / 2, 5), text=title, fill=(255, 69, 0), font=font_season)
    draw.text(xy=(-200, 120), text=text1, fill=(255, 255, 255), font=font_stats)
    draw.text(xy=(425, 120), text=text2, fill=(255, 255, 255), font=font_stats)
    draw.text(xy=(1050, 120), text=text3, fill=(255, 255, 255), font=font_stats)
    if season != '' and team != '':
        imgCopy.save(f"{image_save_path}/ {query_name} {season} {team}.png")
    elif team == '':
        if season != '':
            if league == "TOT":
                imgCopy.save(f"{image_save_path}/ {query_name} {season} ({league}AL).png")
            else:
                imgCopy.save(f"{image_save_path}/ {query_name} {season}.png")
        elif season == '' and league != '':
            imgCopy.save(f"{image_save_path}/ {query_name} Career ({league}).png")
        else:
            pass
    else:
        pass
