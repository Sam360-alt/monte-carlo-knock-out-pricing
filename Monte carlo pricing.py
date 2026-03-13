import yfinance as yf
import numpy as np
import random
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import date,timedelta

today = date.today()

dates = [
    today + timedelta(days=i)
    for i in range(365)
    if (today + timedelta(days=i)).weekday() < 5
    ]


S = float(yf.download('CL=F',period='1d',auto_adjust=True)['Close'].iloc[-1])


close = yf.download('CL=F',interval='1d',period='10mo',auto_adjust=True)['Close'].dropna()
log_returns = np.log(close/close.shift(1)).dropna()
sigma = log_returns.std()*np.sqrt(252)
mu = 0.05
rf = yf.download('^IRX',period='1d',auto_adjust=True)['Close'].iloc[-1]/100
dt = 1/252

path = {}

for sim in range(0,1000):


    list_random = []
    for i in range(0,252):
        m = random.random()
        list_random.append(m)

    epsilon = []
    for i in list_random:
        epsi = norm.ppf(i)
        epsilon.append(float(epsi))

    #stochastic part
    stochastic_part = []
    for i in range(0,252):
        stochastic = sigma*epsilon[i]*np.sqrt(dt)
        stochastic_part.append(float(stochastic.iloc[0]))

    deterministic_part = []
    for i in range(0,252):
        deterministic = (mu - 0.5*sigma**2)*dt
        deterministic_part.append(float(deterministic.iloc[0]))

    deltalog = []
    for i in range(0,252):
        deltaLn = stochastic_part[i]+deterministic_part[i]
        deltalog.append(deltaLn)


    S_1 = S*np.exp(deltalog[0])
    spot = []
    spot.append(S)
    spot.append(S_1)
    for i in range(2,252):
        monte_carlo = spot[i-1]*np.exp(deltalog[i])
        spot.append(monte_carlo)

    path[sim] = spot


for sim, spot in path.items():
    plt.plot(dates[:len(spot)], spot, alpha=0.3)

plt.xlabel("Date")
plt.ylabel("Spot")
plt.show(block=True)


def european_option(T=1,rf=rf,option_type='call'):
    last_price = []
    payoff = []
    K = input('Enter the strike: ')
    K = float(K)
    for i in range(0,len(path)):
        last_price.append(path[i][-1])

    if option_type.lower() == 'call':
        for p in last_price:
            payoff.append(max(0,p-K))
    elif option_type.lower() == 'put':
        for p in last_price:
            payoff.append(max(0,K-p))
    else:
        print('Only call and put are accepted as option type for this function')

    price = np.mean(payoff)*np.exp(-rf*T)
    return price




def european_knock_out(T=1,rf=rf,option_type='up-and-out call'):
    path_up = {}
    path_down = {}
    last_price_up = []
    last_price_down = []
    payoff = []
    B = float(input('Enter the barrier level: '))
    K = float(input('Enter the strike: '))


    if option_type[:2] == 'up':
        for i in range(0,len(path)):
            if any(n > B for n in path[i]) == False:
                path_up[i] = path[i]
                last_price_up.append(path_up[i][-1])
            else:
                pass
    else:
        for i in range(0,len(path)):
            if any(n < B for n in path[i]) == False:
                path_down[i] = path[i]
                last_price_down.append(path_down[i][-1])
            else:
                pass


    if option_type.lower() == 'up-and-out call':
        for p in last_price_up:
            payoff.append(max(0,p-K))
    elif option_type.lower() == 'up-and-out put':
        for p in last_price_up:
            payoff.append(max(0,K-p))
    elif option_type.lower() == 'down-and-out call':
        for p in last_price_down:
            payoff.append(max(0,p-K))
    elif option_type.lower() == 'down-and-out put':
        for p in last_price_down:
            payoff.append(max(0,K-p))


    price = np.exp(-rf*T)*np.mean(payoff)
    return price


price1 = european_option()
price = european_knock_out(option_type = 'down-and-out call')

print(price1)
print(price)

    
    




