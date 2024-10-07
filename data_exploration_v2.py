# -*- coding: utf-8 -*-
"""Data Exploration - v2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p-vP9YfsXquCyHmyJC1B50rtfEETiEB8

# Data Exploration and Preliminary Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import pearsonr
import geopandas as gpd
from statsmodels.graphics.regressionplots import plot_leverage_resid2
from statsmodels.api import OLS, add_constant
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.graphics.regressionplots import influence_plot

# Load the CSV file to examine the contents
data = pd.read_csv('combined_health_crime_data.csv')

# Display the first few rows of the dataframe
data.head()

# Selecting the variables of interest for exploratory analysis
selected_variables = ['ah3h', 'ah3g', 'ah3e', 'ah3r', 'ah3ahah', 'Average Crimes']

# Create a subset of the data with the selected variables
data_subset = data[selected_variables]

# Check for any missing values in the selected variables
data_subset.isnull().sum()

# Display the missing values information and the first few rows of the subset
data_subset.head()

"""### Exploratory Data Analysis"""

# Generate a statistical summary of the dataset
data_subset.describe()

# Creating a correlation matrix for these top variables
corr_matrix = data_subset[selected_variables].corr()

# Plotting the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title("Correlation Matrix of Selected Variables")
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Histograms for the selected domain scores and average crime rates
# Setting up the figure size and layout
fig, axes = plt.subplots(3, 2, figsize=(14, 12))

# Health Domain Score
sns.histplot(data_subset['ah3h'], bins=30, ax=axes[0, 0], kde=True)
axes[0, 0].set_title('Histogram of Health Domain Score')

# Green/Bluespace Domain Score
sns.histplot(data_subset['ah3g'], bins=30, ax=axes[0, 1], kde=True)
axes[0, 1].set_title('Histogram of Green/Bluespace Domain Score')

# Air Quality Domain Score
sns.histplot(data_subset['ah3e'], bins=30, ax=axes[1, 0], kde=True)
axes[1, 0].set_title('Histogram of Air Quality Domain Score')

# Retail Domain Score
sns.histplot(data_subset['ah3r'], bins=30, ax=axes[1, 1], kde=True)
axes[1, 1].set_title('Histogram of Retail Domain Score')

# Access to Healthy Assets and Hazards Index Score
sns.histplot(data_subset['ah3ahah'], bins=30, ax=axes[2, 0], kde=True)
axes[2, 0].set_title('Histogram of Access to Healthy Assets and Hazards Index Score')

# Average Crime Rates
sns.histplot(data_subset['Average Crimes'], bins=30, ax=axes[2, 1], kde=True)
axes[2, 1].set_title('Histogram of Average Crime Rates')

# Tidy up the layout
plt.tight_layout()
plt.show()

"""- Health Domain Score (ah3h) distribution appears to be roughly bell-shaped, suggesting a normal distribution of health domain scores across the areas.
- Green/Bluespace Domain Score (ah3g) distribution is also approximately normal, indicating a balance of areas with varying levels of access to green and blue spaces.
- Air Quality Domain Score (ah3e) has a similar bell-shaped distribution, which suggests that air quality scores are normally distributed across the dataset.
- Retail Domain Score (ah3r) also appears to have a normal distribution, with most areas having a moderate score and fewer areas at the extremes.
- Access to Healthy Assets and Hazards Index Score (ah3ahah) distribution is skewed to the right, with more areas having lower scores and fewer areas with high scores.
- Average Crime Rates has a right-skewed distribution for average crime rates, with most areas experiencing lower crime rates and a few areas with very high crime rates.
"""

# Scatter plots to explore potential relationships between domain scores and average crime rates

# Setting up the figure size and layout
fig, axes = plt.subplots(2, 3, figsize=(15,9))

# Mapping each domain score to a plot
domain_to_axis = zip(selected_variables[:-1], [ax for row in axes for ax in row])

# Creating scatter plots for each domain score against average crime rates
for domain, ax in domain_to_axis:
    sns.scatterplot(x=domain, y='Average Crimes', data=data_subset, ax=ax)
    ax.set_title(f'{domain} vs. Average Crime Rates')
    # Compute and display the Pearson correlation coefficient
    corr, _ = pearsonr(data_subset[domain], data_subset['Average Crimes'])
    ax.text(0.05, 0.95, f'Corr: {corr:.2f}', transform=ax.transAxes, verticalalignment='top')

# Tidy up the layout
plt.tight_layout()
plt.show()

"""### Multivariate Regression Analysis"""

# Prepare the data for multivariate regression analysis
X = data_subset[selected_variables[:-1]]  # Independent variables (all domain scores)
y = data_subset['Average Crimes']          # Dependent variable (average crime rates)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
multivar_lin_reg = LinearRegression()

# Fit the model on the training data
multivar_lin_reg.fit(X_train, y_train)

# Predict on the test set
y_pred = multivar_lin_reg.predict(X_test)

# Evaluate the model's performance
multivar_mse = mean_squared_error(y_test, y_pred)
multivar_r2 = r2_score(y_test, y_pred)

# Coefficients of the model for each domain
coefficients = multivar_lin_reg.coef_

multivar_mse

multivar_r2

coefficients

"""The Mean Squared Error (MSE) of the model is approximately 5804.65. This is lower than the MSE from the simple linear regression model, suggesting a better fit to the data.

The R-squared (R²) value is approximately 0.221. This indicates that about 22.1% of the variability in the average crime rates can be explained by the combined domain scores. This is an improvement over the simple linear regression model, indicating a better explanatory power of the model when multiple factors are considered.

The coefficients for the domain scores are as follows:
- Health Domain Score (ah3h): -23.80
- Green/Bluespace Domain Score (ah3g): -12.18
- Air Quality Domain Score (ah3e): -21.20
- Retail Domain Score (ah3r): 15.12
- Access to Healthy Assets and Hazards Index Score (ah3ahah): 3.64

These coefficients indicate the expected change in the average crime rates for a one-unit change in the domain scores, holding all other scores constant. The negative coefficients for the health, green/bluespace, and air quality scores suggest that higher scores in these domains are associated with lower crime rates. Conversely, the positive coefficients for the retail domain score and the Access to Healthy Assets and Hazards Index Score suggest that higher scores in these domains are associated with higher crime rates.
"""

# Predict on the test set
y_pred = multivar_lin_reg.predict(X_test)

# Adding a constant for OLS regression
X_train_const = add_constant(X_train)

# Fit OLS regression
# Fit OLS regression to get the regression equation
ols_model = OLS(y_train, X_train_const).fit()

# Residuals
residuals = y_test - y_pred

# Plotting residual diagnostics along with the regression plot including the regression equation
plt.figure(figsize=(12, 8))

# Regression plot with regression equation
plt.subplot(2, 2, 1)
sns.regplot(x=X_test.iloc[:, 0], y=y_test, ci=None, label='Actual')
plt.scatter(X_test.iloc[:, 0], y_pred, color='r', label='Predicted')
plt.title('Regression Plot')
plt.xlabel('Independent Variable')
plt.ylabel('Dependent Variable')
plt.legend()

# Add the regression equation to the plot
eq = 'y = {:.2f} + {:.2f}X1 + {:.2f}X2 + ...'.format(ols_model.params[0],
                                                      *ols_model.params[1:3])
plt.text(min(X_test.iloc[:, 0]), max(y_test), eq, fontsize=12, color='blue')

# Residuals vs Fitted
plt.subplot(2, 2, 2)
sns.residplot(x=y_pred, y=residuals, lowess=True, line_kws={'color': 'red', 'lw': 1})
plt.title('Residuals vs Fitted')
plt.xlabel('Predicted')
plt.ylabel('Residuals')

# Q-Q plot
plt.subplot(2, 2, 3)
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Normal Q-Q')

# Scale-Location (Spread-Location)
plt.subplot(2, 2, 4)
plt.scatter(y_pred, residuals**0.5, alpha=0.5)
sns.regplot(x=y_pred, y=residuals**0.5, scatter=False, ci=False, lowess=True,
            line_kws={'color': 'red', 'lw': 1})
plt.title('Scale-Location')
plt.xlabel('Predicted')
plt.ylabel('Sqrt(Residuals)')

plt.tight_layout()
plt.show()

