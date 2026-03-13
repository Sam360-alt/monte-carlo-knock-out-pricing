Monte Carlo Option Pricing (Python)

This project implements a Monte Carlo simulation framework for pricing derivatives using Python.
It simulates possible future price paths for crude oil futures and prices:

European options

Barrier options (knock-out)

The simulation uses Geometric Brownian Motion (GBM) and real market data retrieved from Yahoo Finance.

Features

Monte Carlo simulation of asset price paths

Uses real market data via Yahoo Finance

Visualizes simulated price paths

Prices:

European Call / Put options

Barrier knock-out options

Up-and-out

Down-and-out

Risk-free rate retrieved from US Treasury data (^IRX)

Volatility estimated from historical log returns

Mathematical Model

The asset price follows a Geometric Brownian Motion process.
