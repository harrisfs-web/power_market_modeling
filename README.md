# Stochastic CVaR Energy Planning

This repository contains a Python script that uses Gurobi to solve a stochastic energy planning problem with Conditional Value at Risk (CVaR) optimization. The script models energy production and trading across two regions using two technologies under different demand and capacity scenarios.

## Problem Description

The problem is formulated as a stochastic optimization model with the following features:

- **Regions**: Two regions, `Region1` and `Region2`.
- **Technologies**: Two technologies, `Tech1` and `Tech2`.
- **Scenarios**: Three scenarios representing different levels of demand and capacity:
  - Low demand, high capacity (probability 0.2)
  - Medium demand, medium capacity (probability 0.5)
  - High demand, low capacity (probability 0.3)

## Notation

- **Indices:**
  - \( r \): Index for regions (Region1, Region2)
  - \( t \): Index for technologies (Tech1, Tech2)
  - \( s \): Index for scenarios (Low, Medium, High)

- **Parameters:**
  - \( c_t \): Cost per MW for technology \( t \)
  - \( d_{rs} \): Demand in region \( r \) under scenario \( s \)
  - \( e_{rts} \): Capacity in region \( r \) for technology \( t \) under scenario \( s \)
  - \( p_s \): Probability of scenario \( s \)
  - \( \kappa \): Cost per MW of energy traded
  - \( \beta \): Risk-aversion parameter for CVaR (set to 0.95)

- **Decision Variables:**
  - \( x_{rts} \): Energy produced in region \( r \) by technology \( t \) in scenario \( s \)
  - \( y_{r1r2s} \): Energy traded from region \( r1 \) to region \( r2 \) in scenario \( s \)
  - \( \eta \): Auxiliary variable for CVaR
  - \( z_s \): Auxiliary variable for scenario-specific CVaR

## Usage

Clone the repository and navigate to the project directory.
Run the script to perform the optimization of the energy planning model.