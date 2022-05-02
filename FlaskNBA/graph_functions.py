import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


DRB_STL_BLK_radarChart_savePath = r"C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\DRB, STL, BLK Radar Charts"

def shootingRadar(stat_list, query_name):
    made = ['FT', '2P', '3P']
    shooting_radarChart_savePath = r"C:\Users\Owner\Documents\Python Projects\FlaskNBA\static\Shooting Radar Charts"

    for i in stat_list:
        try:
            FTA = float(i['FTA'])
        except:
            FTA = None
        try:
            TwoPA = float(i['2PA'])
        except:
            TwoPA = None
        try:
            ThreePA = float(i['3PA'])
        except:
            ThreePA = None
        attempts = [FTA, TwoPA, ThreePA]

        try:
            FT = float(i['FT'])
        except:
            FT = None
        try:
            TwoP = float(i['2P'])
        except:
            TwoP = None
        try:
            ThreeP = float(i['3P'])
        except:
            ThreeP = None

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=attempts,
            theta=made,
            fill='toself',
            name='Shots Attempted'

        ))
        fig.add_trace(go.Scatterpolar(
            r=[FT, TwoP, ThreeP],
            theta=made,
            fill='toself',
            name='Shots Made'
        ))

        fig.update_layout(
            title=dict(
                text=f"{query_name.upper()} {i['Season']} {i['Tm']} {i['Lg']} (2P, 3P, FT)"
            ),
            polar=dict(
                radialaxis=dict(
                    visible=True,

                )),

            showlegend=True

        )
        if i['Tm'] != '' and i['Season'] != '':
            # h.append(fig.to_html())
            fig.write_image(f"{shooting_radarChart_savePath}/{query_name.upper()} {i['Season']} {i['Tm']}.png")
        elif i['Tm'] == '' and i['Season'] != '' and i['Lg'] == 'TOT':
            # h.append(fig.to_html())
            fig.write_image(f"{shooting_radarChart_savePath}/{query_name.upper()} {i['Season']} {i['Lg']}AL.png")
        elif i['Tm'] == '' and i['Season'] == '' and i['Lg'] != 'TOT' and i['Lg'] != '':
            # h.append(fig.to_html())
            fig.write_image(f"{shooting_radarChart_savePath}/{query_name.upper()} Career {i['Lg']}.png")
        elif i['Tm'] == '' and i['Season'] != '' and i['Lg'] != 'TOT' and i['Lg'] != '':
            fig.write_image(f"{shooting_radarChart_savePath}/{query_name.upper()} {i['Season']}.png")
        else:
            pass



def defenseRadar(stat_list, query_name):
    for i in stat_list:
        try:
            DRB = float(i['DRB'])
        except:
            DRB = None
        try:
            STL = float(i['STL'])
        except:
            STL = None
        try:
            BLK = float(i['BLK'])
        except:
            BLK = None

        df = pd.DataFrame(dict(
            values =[DRB, STL, BLK],
            theta =['DRB', 'STL', 'BLK']))
        fig = px.line_polar(df, r='values', theta='theta', line_close=True, markers=True, hover_name='theta',
                            hover_data={'theta': False}, title = f"{query_name.upper()} {i['Season']} {i['Tm']} {i['Lg']} (DRB, STL, BLK)")
        fig.update_traces(fill='toself')


        if i['Tm'] != '' and i['Season'] != '':
            # h.append(fig.to_html())
            fig.write_image(f"{DRB_STL_BLK_radarChart_savePath}/{query_name.upper()} {i['Season']} {i['Tm']}.png")
        elif i['Tm'] == '' and i['Season'] != '' and i['Lg'] == 'TOT':
            # h.append(fig.to_html())
            fig.write_image(f"{DRB_STL_BLK_radarChart_savePath}/{query_name.upper()} {i['Season']} {i['Lg']}AL.png")
        elif i['Tm'] == '' and i['Season'] == '' and i['Lg'] != 'TOT' and i['Lg'] != '':
            # h.append(fig.to_html())
            fig.write_image(f"{DRB_STL_BLK_radarChart_savePath}/{query_name.upper()} Career {i['Lg']}.png")
        elif i['Tm'] == '' and i['Season'] != '' and i['Lg'] != 'TOT' and i['Lg'] != '':
            fig.write_image(f"{DRB_STL_BLK_radarChart_savePath}/{query_name.upper()} {i['Season']}.png")
        else:
            pass

