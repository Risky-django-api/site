from django.shortcuts import render
import requests
import json
from django.views.generic import TemplateView
import time
import datetime as dt
from dateutil.parser import parse
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime
import scipy.stats as ss
import scipy.integrate
from django.contrib.auth.decorators import login_required
from .forms import CoinForm, Time, Timecoin
from django.contrib import messages
from .models import Portfolio, Time_model


# Create your views here.
def hello(request):
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=true'
    data = requests.get(url)
    data = data.json()

    coin_list = {'id1': data[0]['id'], 'image1': data[0]['image'], 'data': data}


    data = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30')

    t = list(map(lambda x: datetime.datetime.fromtimestamp(x // 1000), np.array(data.json()['prices'])[:,0]))
    p = np.array(data.json()['prices'])[:,1]

    trace1 = go.Scatter(x=t, y=p,  
                        line=dict(color='rgb(38, 94, 11)', width=2))
    layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20),
                    )

    figure=go.Figure(data=trace1,layout=layout)

    coin_list['graph'] = figure.to_html()


    return render(request, 'pages/hello.html', coin_list)

def coin(request, parameter):

    days = 30
    if request.method == 'POST':
        form = Timecoin(request.POST or None)
        if form.is_valid():
            days = form.cleaned_data['days']
            if days is None:
                days = 30
    else:
        form = Timecoin()

    url = 'https://api.coingecko.com/api/v3/coins/'+parameter+'?localization=false&community_data=false&developer_data=false&sparkline=false'
    data = requests.get(url)
    coin = data.json()

    data = requests.get('https://api.coingecko.com/api/v3/coins/'+parameter+'/market_chart?vs_currency=usd&days='+str(days))

    t = list(map(lambda x: datetime.datetime.fromtimestamp(x // 1000), np.array(data.json()['prices'])[:,0]))
    p = np.array(data.json()['prices'])[:,1]
    data = pd.DataFrame(p, columns = ['price'], index = t)
    data = data.pct_change().dropna()

    #Graph 1
    trace1 = go.Scatter(x=t, y=p,  
                        line=dict(color='rgb(38, 94, 11)', width=2))
    layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20),
                    )

    fig1=go.Figure(data=trace1,layout=layout)

    #Graph 2
    trace1 = go.Scatter(x=t, y=data['price'],  
                        line=dict(color='rgb(38, 94, 11)', width=1))
    layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20),
                    )

    fig2=go.Figure(data=trace1,layout=layout)

    #Graph 3
    # Lets fit t-student distribution
    level = 0.95
    fitted_dist = ss.norm(*ss.norm.fit(data.values)) # this is an instance of the specified distribution

    # note that level here is inherited from the calculation above
    VaR_param = - fitted_dist.ppf(1-level) # ppf - percent point function

    VaR_HS = -data.quantile(1 - level, interpolation = 'higher')

    fig3 = make_subplots()

    trace1 = go.Histogram(x=data['price'], marker_color='rgb(138, 89, 150)', name="Returns' frequency") 
    x = np.linspace(data['price'].min(), data['price'].max())
    trace2 = go.Scatter(x=x, y=fitted_dist.pdf(x),  
                        line=dict(color='rgb(72, 74, 67)', width=1), name='Fitted pdf')  
    y1 = np.linspace(0, fitted_dist.pdf(x).max()+2)
    y2 = np.linspace(0, fitted_dist.pdf(x).max()+20)

    trace3 = go.Scatter(x=[-VaR_HS.values[0]]*len(y1), y=y1,  
                        line=dict(color='rgb(101, 140, 81)', width=3), name="Empirical VaR 95%: {:.2f}%".format(100 * VaR_HS.values[0])) 
    trace4 = go.Scatter(x=[-VaR_param]*len(y2), y=y2,  
                        line=dict(color='rgb(119, 117, 199)', width=3), name="Parametric VaR 95%: {:.2f}%".format(100 * VaR_param))

    layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20)
                    )
    fig3.add_trace(trace1)
    fig3.add_trace(trace2) 
    fig3.add_trace(trace3)
    fig3.add_trace(trace4)
    fig3.update_layout(layout)

    #Graph 4
    ES_HS = -data[data < -VaR_HS].mean()
    ES_param, _ = scipy.integrate.quad(
        lambda x: - x * fitted_dist.pdf(x) / (1 - level),- np.inf,- VaR_param,)

    fig4 = make_subplots()

    trace1 = go.Histogram(x=data['price'], marker_color='rgb(138, 89, 150)', name="Returns' frequency") 
    x = np.linspace(data['price'].min(), data['price'].max())
    trace2 = go.Scatter(x=x, y=fitted_dist.pdf(x),  
                        line=dict(color='rgb(72, 74, 67)', width=1), name='Fitted pdf')  

    y1 = np.linspace(0, fitted_dist.pdf(x).max()+20)
    y2 = np.linspace(0, fitted_dist.pdf(x).max()+2)

    trace3 = go.Scatter(x=[-ES_HS.values[0]]*len(y1), y=y1,  
                        line=dict(color='rgb(224, 217, 11)', width=3), name="Empirical ES 95%: {:.2f}%".format(100 * ES_HS.values[0])) 
    trace4 = go.Scatter(x=[-ES_param]*len(y2), y=y2,  
                        line=dict(color='rgb(224, 178, 11)', width=3), name="Parametric ES 95%: {:.2f}%".format(100 * ES_param))

    layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20),
                    )
    fig4.add_trace(trace1)
    fig4.add_trace(trace2) 
    fig4.add_trace(trace3)
    fig4.add_trace(trace4)
    fig4.update_layout(layout)

    coin_list = {'image':  coin['image']['small'], \
        'price': coin['market_data']['current_price']['usd'],\
        'high_24h': coin['market_data']['high_24h']['usd'],\
        'low_24h': coin['market_data']['low_24h']['usd'],\
        'market_cap_change_percentage_24h': coin['market_data']['market_cap_change_percentage_24h'],\
        'total_volume': coin['market_data']['total_volume']['usd']}
    coin_list['graph1'] = fig1.to_html()
    coin_list['graph2'] = fig2.to_html()
    coin_list['graph3'] = fig3.to_html()
    coin_list['graph4'] = fig4.to_html()
    coin_list['var'] = round(VaR_param * 100, 2)
    coin_list['es'] = round(ES_param * 100, 2)
    coin_list['id'] = parameter
    coin_list['form'] = form
    coin_list['days'] = days


    return render(request, 'pages/coin.html', coin_list)



@login_required
def portfolio(request):

    if request.method == 'POST':
        form = CoinForm(request.POST or None)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
        else:
            messages.success(request, f'Fill the form')
    else:
        form = CoinForm()

    if request.method == 'POST':
        form2 = Time(request.POST or None)
        if form2.is_valid():
            time_model = form2.save(commit=False)
            time_model.user = request.user
            time_model.save()
    else:
        form2 = Time()

    days = Time_model.objects.filter(user=request.user).last()
    user_data = Portfolio.objects.filter(user=request.user).last()

    if user_data is not None:
        days = Time_model._meta.get_field('days').value_from_object(days)
        if days is None:
            days = 30

        
        composition = {}
        i = 1
        names = [field.name for field in Portfolio._meta.get_fields()][2:]
        for nam in names:
            n = nam.replace('_', '-')
            field_object = Portfolio._meta.get_field(nam)
            vol = field_object.value_from_object(user_data)
            if i == 1 and vol is not None:
                composition[n] = vol

                url = 'https://api.coingecko.com/api/v3/coins/'+n+'?localization=false&community_data=false&developer_data=false&sparkline=false'
                data = requests.get(url)
                coin = data.json()

                coin_list = {'id': coin['id'], 'image':  coin['image']['small'], \
                    'price': coin['market_data']['current_price']['usd'],\
                    'high_24h': coin['market_data']['high_24h']['usd'],\
                    'low_24h': coin['market_data']['low_24h']['usd'],\
                    'market_cap_change_percentage_24h': coin['market_data']['market_cap_change_percentage_24h'],\
                    'total_volume': coin['market_data']['total_volume']['usd'], 'vol': vol}
                coins = [coin_list]

                data = requests.get('https://api.coingecko.com/api/v3/coins/'+n+'/market_chart?vs_currency=usd&days='+str(days))
                data = data.json()
                t = list(map(lambda x: datetime.datetime.fromtimestamp(x // 1000).replace(second=0, minute=0), np.array(data['prices'])[:,0]))
                p = np.array(data['prices'])[:,1] 
                data_coins = pd.DataFrame(p, columns = [n], index = t)
                i = 0
            elif vol is not None:
                composition[n] = vol

                url = 'https://api.coingecko.com/api/v3/coins/'+n+'?localization=false&community_data=false&developer_data=false&sparkline=false'
                data = requests.get(url)
                coin = data.json()

                coin_list = {'id': coin['id'], 'image':  coin['image']['small'], \
                        'price': coin['market_data']['current_price']['usd'],\
                        'high_24h': coin['market_data']['high_24h']['usd'],\
                        'low_24h': coin['market_data']['low_24h']['usd'],\
                        'market_cap_change_percentage_24h': coin['market_data']['market_cap_change_percentage_24h'],\
                        'total_volume': coin['market_data']['total_volume']['usd'], 'vol': vol}
                coins += [coin_list]
               

                data = requests.get('https://api.coingecko.com/api/v3/coins/'+n+'/market_chart?vs_currency=usd&days='+str(days))
                data = data.json()
                t = list(map(lambda x: datetime.datetime.fromtimestamp(x // 1000).replace(second=0, minute=0), np.array(data['prices'])[:,0]))
                p = np.array(data['prices'])[:,1] 
                data = pd.DataFrame(p, columns = [n], index = t)
                data_coins = pd.merge(data_coins, data ,left_index=True, right_index=True, how = 'inner')
                data_coins = data_coins.dropna()


        summa = data_coins @ pd.Series(composition) 

        data_new = data_coins.copy()
        for col in data_new.columns:
            data_new[col] = data_new[col] * pd.Series(composition).loc[col]

        #Graph 1
        fig1 = go.Figure()
        for col in data_new.columns:
            trace1 = go.Scatter(x=data_new.index, y=data_new[col]/data_new[col][0], line=dict(width=1), name=col)
            fig1.add_trace(trace1)
        layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20),)
        trace1 = go.Scatter(x=summa.index, y=summa.values/summa.values[0], line=dict(color='rgb(122, 20, 20)', width=2), name='Sum')
        fig1.add_trace(trace1)
        fig1.update_layout(layout)

        #Graph 2
        returns_new = data_new.pct_change().dropna()
        fig2 = go.Figure()
        for col in returns_new.columns:
            trace1 = go.Scatter(x=returns_new.index, y=returns_new[col], line=dict(width=1), name = col)
            fig2.add_trace(trace1)
        trace1 = go.Scatter(x=summa.index, y=summa.pct_change().dropna().values, line=dict(color='rgb(122, 20, 20)', width=1), name='Sum')
        fig2.add_trace(trace1)

        layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(146, 126, 148, 0.15)',
                    margin=dict(l=10, r=10, b=50, t=20),)
        fig2.update_layout(layout)

        #Graph 3
        df_corr = data_coins.corr()

        fig3 = go.Figure()
        fig3.add_trace(
            go.Heatmap(
                x = df_corr.columns,
                y = df_corr.index,
                z = np.array(df_corr),
                text=df_corr.values,
                texttemplate='%{text:.2f}'
            )
        )
        fig3.update_layout(layout)

        returns = data_coins.pct_change().dropna()

        #More - graph 4 and 5
        portfolio_dollar_composition = pd.Series(composition) * data_coins.loc[data_coins.index.max(),composition.keys()].mean(axis=0)
        portfolio_value = portfolio_dollar_composition.sum()
        weights = portfolio_dollar_composition / portfolio_value

        portfolio_scenarios =  returns @ weights
        VaR = - portfolio_scenarios.quantile(1 - 0.95, interpolation='higher')
        ES = -portfolio_scenarios[portfolio_scenarios < -VaR].mean()

        fig4 = go.Figure()
        fig4.add_trace(go.Histogram(x=portfolio_scenarios, marker_color='rgb(138, 89, 150)', name="Returns' frequency"))
        fig4.add_vline(x=-VaR, annotation_text = "Historical VaR 95%: {:.2f}%".format(100 * VaR), line_color="green", line_width = 2)
        fig4.update_layout(layout)

        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(x=portfolio_scenarios, marker_color='rgb(138, 89, 150)', name="Returns' frequency"))
        fig5.add_vline(x=-ES, annotation_text = "Historical ES 95%: {:.2f}%".format(100 * ES),  line_color="rgb(224, 217, 11)", line_width = 2)
        fig5.update_layout(layout)



        graph1 = fig1.to_html()
        graph2 = fig2.to_html()
        graph3 = fig3.to_html()
        graph4 = fig4.to_html()
        graph5 = fig5.to_html()

        fill = {'form': form, 'form2': form2, 'data': coins, 'graph1': graph1, 'graph2': graph2, \
            'graph3': graph3, 'graph4': graph4, 'graph5': graph5, 'var': round(VaR * 100, 2),\
             "var_usd": round(VaR * portfolio_value * 100, 2), 'ES': round(ES * 100, 2), "days": days}
        return render(request, 'pages/port.html', fill)
    else:
        return render(request, 'pages/port.html', {'form': form, 'form2': form2, "days": days})