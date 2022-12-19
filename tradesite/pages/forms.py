from django import forms
from .models import Portfolio, Time_model
import requests
import json

class CoinForm(forms.ModelForm):
    w = (forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'volume e.g. 0.4'}))
    w1 = (forms.TextInput(attrs={'class': 'form-control'}))
    bitcoin = forms.FloatField(help_text="Volume", label = 'bitcoin', widget=w, required = False)
    ethereum = forms.FloatField(help_text="Volume", label = 'ethereum', widget=w1, required = False)
    tether = forms.FloatField(help_text="Volume", label = 'tether', widget=w1, required = False)
    usd_coin= forms.FloatField(help_text="Volume", label = 'usd-coin', widget=w1, required = False)
    binancecoin= forms.FloatField(help_text="Volume", label = 'binancecoin', widget=w1, required = False)
    binance_usd= forms.FloatField(help_text="Volume", label = 'binance-usd', widget=w1, required = False)
    ripple= forms.FloatField(help_text="Volume", label = 'ripple', widget=w1, required = False)
    dogecoin= forms.FloatField(help_text="Volume", label = 'dogecoin', widget=w1, required = False)
    cardano= forms.FloatField(help_text="Volume", label = 'cardano', widget=w1, required = False)
    matic_network= forms.FloatField(help_text="Volume", label = 'matic-network', widget=w1, required = False)
    staked_ether= forms.FloatField(help_text="Volume", label = 'staked-ether', widget=w1, required = False)
    polkadot= forms.FloatField(help_text="Volume", label = 'polkadot', widget=w1, required = False)
    litecoin= forms.FloatField(help_text="Volume", label = 'litecoin', widget=w1, required = False)
    okb= forms.FloatField(help_text="Volume", label = 'okb', widget=w1, required = False)
    dai= forms.FloatField(help_text="Volume", label = 'dai', widget=w1, required = False)
    shiba_inu= forms.FloatField(help_text="Volume", label = 'shiba-inu', widget=w1, required = False)
    tron= forms.FloatField(help_text="Volume", label = 'tron', widget=w1, required = False)
    solana= forms.FloatField(help_text="Volume", label = 'solana', widget=w1, required = False)
    uniswap= forms.FloatField(help_text="Volume", label = 'uniswap', widget=w1, required = False)
    avalanche_2= forms.FloatField(help_text="Volume", label = 'avalanche-2', widget=w1, required = False)
    leo_token = forms.FloatField(help_text="Volume", label = 'leo-token', widget=w1, required = False)
    wrapped_bitcoin = forms.FloatField(help_text="Volume", label = 'wrapped-bitcoin', widget=w1, required = False)
    the_open_network = forms.FloatField(help_text="Volume", label = 'the-open-network', widget=w1, required = False)
    chainlink = forms.FloatField(help_text="Volume", label = 'chainlink', widget=w1, required = False)

    class Meta():
        model = Portfolio 
        exclude = ('user',)



class Time(forms.ModelForm):
    w = (forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'days'}))
    days = forms.IntegerField(help_text="Days", label = 'Days', widget=w, required = False)
    
    class Meta():
        model = Time_model 
        exclude = ('user',)

class Timecoin(forms.Form):
    w = (forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'days'}))
    days = forms.IntegerField(help_text="Days", label = 'Days', widget=w, required = False)