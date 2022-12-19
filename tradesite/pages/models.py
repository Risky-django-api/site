from django.db import models
from django.contrib.auth.models import User
import requests
import json

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)    

    bitcoin = models.FloatField(help_text="Volume", default = 0, null=True)
    ethereum = models.FloatField(help_text="Volume", default = 0, null=True)
    tether = models.FloatField(help_text="Volume", default = 0, null=True)
    usd_coin = models.FloatField(help_text="Volume", default = 0, null=True)
    binancecoin = models.FloatField(help_text="Volume", default = 0, null=True)
    binance_usd = models.FloatField(help_text="Volume", default = 0, null=True)
    ripple = models.FloatField(help_text="Volume", default = 0, null=True)
    dogecoin = models.FloatField(help_text="Volume", default = 0, null=True)
    cardano = models.FloatField(help_text="Volume", default = 0, null=True)
    matic_network = models.FloatField(help_text="Volume", default = 0, null=True)
    staked_ether = models.FloatField(help_text="Volume", default = 0, null=True)
    polkadot = models.FloatField(help_text="Volume", default = 0, null=True)
    litecoin = models.FloatField(help_text="Volume", default = 0, null=True)
    okb = models.FloatField(help_text="Volume", default = 0, null=True)
    dai = models.FloatField(help_text="Volume", default = 0, null=True)
    shiba_inu = models.FloatField(help_text="Volume", default = 0, null=True)
    tron = models.FloatField(help_text="Volume", default = 0, null=True)
    solana = models.FloatField(help_text="Volume", default = 0, null=True)
    uniswap = models.FloatField(help_text="Volume", default = 0, null=True)
    avalanche_2 = models.FloatField(help_text="Volume", default = 0, null=True)
    leo_token = models.FloatField(help_text="Volume", default = 0, null=True)
    wrapped_bitcoin = models.FloatField(help_text="Volume", default = 0, null=True)
    the_open_network = models.FloatField(help_text="Volume", default = 0, null=True)
    chainlink = models.FloatField(help_text="Volume", default = 0, null=True)

class Time_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    days = models.IntegerField(help_text="Days", null=True)  
