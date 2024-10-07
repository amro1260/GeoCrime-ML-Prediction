# Geospatial Analysis & Machine Learning for Crime Prediction
## Project Overview
This repository contains the code for the dissertation project I completed for my Master's degree, where I achieved distinction. The project focuses on geospatial analysis and the use of machine learning models to predict street-level crime patterns by integrating health and hazard datasets (AHAH data) with crime data. This project bridges the gap between public health, urban planning, and crime prevention, providing insightful analysis that can inform better policymaking.

## Key Components
Data Preparation (data_preparation.py):

This script preprocesses the datasets for further analysis. It handles tasks such as cleaning, transforming, and merging the health (AHAH) data and crime data to ensure compatibility.
Features:
Data Cleaning and Imputation
Feature Selection and Transformation
Dataset Splitting for Machine Learning
Data Exploration (data_exploration_v2.py):

This script explores the datasets to gain a better understanding of the distribution and characteristics of health assets, hazards, and crime incidents.
Features:
Descriptive Statistics
Data Visualization (e.g., histograms, correlation heatmaps)
Exploratory Geospatial Analysis (crime hotspots, health resource distribution)
Geospatial Analysis & Machine Learning (geospatial_analysis_&_ml.py):

This is the main script where machine learning models are trained and evaluated to predict crime rates based on the geospatial distribution of health assets and hazards.
Features:
Geospatial Mapping using GIS libraries
Model Training and Validation (Random Forest, Linear Regression, etc.)
Predictive Modeling of Crime Incidents
Model Evaluation and Tuning
