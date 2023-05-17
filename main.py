from flask import Flask, request, render_template
from models.t20 import player_recommendation as t20_p_rec
from models.t20 import t20_players,team_recom as t20_team
from models.odi import player_recommendation as odi_p_rec
from models.odi import odi_players,team_recom as odi_team
from models.test import player_recommendation as test_p_rec
from models.test import test_players,team_recom as test_team
from models.t20 import player_in_team as t20_same_team
from models.odi import player_in_team as odi_same_team
from models.test import player_in_team as test_same_team



app = Flask(__name__,template_folder='templates')

def player_duplicate(lst):    
    duplicates = []
    for item in lst:
        if lst.count(item) > 1 and item not in duplicates:
            duplicates.append(item)
    return duplicates


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player')
def player():
    return render_template('player.html', t20_players=t20_players, odi_players=odi_players, test_players=test_players)

@app.route('/team')
def team():
    return render_template("team.html",t20_players=t20_players, odi_players=odi_players, test_players=test_players)

@app.route('/give_team',methods=['POST'])
def predict_team():
    if request.method == 'POST':
        formats = request.form['format']
        pl1 = str(request.form['player_1'])
        pl2 = str(request.form['player_2'])
        pl3 = str(request.form['player_3'])
        pl4 = str(request.form['player_4'])
        pl5 = str(request.form['player_5'])
        pl6 = str(request.form['player_6'])
        pl7 = str(request.form['player_7'])
        pl8 = str(request.form['player_8'])
        pl9 = str(request.form['player_9'])
        pl10 = str(request.form['player_10'])
        pl11 = str(request.form['player_11'])
        opp_team = [pl1,pl2,pl3,pl4,pl5,pl6,pl7,pl8,pl9,pl10,pl11]
        
        if formats == 'Test':
            try:        
                our_team = test_team(opp_team)
            except AttributeError:
                return render_template('error_handle.html')
        elif formats == 'ODI':
            try:
                our_team = odi_team(opp_team)
            except AttributeError:
                return render_template('error_handle.html')    
        else:
            try:
                our_team = t20_team(opp_team)
            except AttributeError:
                return render_template('error_handle.html')
        
        if len(player_duplicate(opp_team)) != 0:
            return render_template('duplicate_error.html', dup_players = player_duplicate(opp_team))
        


    return render_template('result_team.html',pl_list=our_team)
    
        




@app.route('/recommend', methods=['POST'])
def predict():
    if request.method == 'POST':
        formats = request.form['format']
        team_ = request.form['within_team_country']

        if team_ == 'No':
            if formats == 'Test':
                name = str(request.form['player_name'])
                try:
                    pl_list = test_p_rec(name)
                except AttributeError:
                    return render_template('error_handle.html')
            elif formats == 'ODI':
                name = str(request.form['player_name'])
                try:
                    pl_list = odi_p_rec(name)
                except AttributeError:
                    return render_template('error_handle.html')
            else:
                name = str(request.form['player_name'])
                try:
                    pl_list = t20_p_rec(name)
                except AttributeError:
                    return render_template('error_handle.html')
        else:
            if formats == 'Test':
                name = str(request.form['player_name'])
                try:
                    pl_list = test_same_team(name)
                except AttributeError:
                    return render_template('error_handle.html')
            elif formats == 'ODI':
                name = str(request.form['player_name'])
                try:
                    pl_list = odi_same_team(name)
                except AttributeError:
                    return render_template('error_handle.html')
            else:
                name = str(request.form['player_name'])
                try:
                    pl_list = t20_same_team(name)
                except AttributeError:
                    return render_template('error_handle.html')

    return render_template('result.html',pl_list=pl_list)





if __name__ == '__main__':
    app.run(debug=True)
