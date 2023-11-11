#Importing necessary libraries
import numpy as np


#Defining the logistic function
def logistic(x):
    return 1 / (1 + np.exp(-x))

#Defining the main function to calculate probabilities
def calculate_probabilities(parameters, data, utilities):
    # Error handling
    for utility in utilities:
        # Extracting the variable names from the utility function
        variable_names = [var for var in utility.__code__.co_varnames if var != 'data_point']
        if not all(var in data for var in variable_names):
            raise ValueError("Mismatched variables between utility functions and data.")

    # Initializing an empty dictionary to store probabilities
    probabilities = {}

    # Looping through each utility function
    for utility in utilities:
        # Extracting variable names from the utility function
        variable_names = [var for var in utility.__code__.co_varnames if var != 'data_point']

        # Calculating deterministic utility for each data point
        v_values = np.array([utility(**{var: data[var][i] for var in variable_names}) for i in range(len(data['X1']))])

        # Calculating the denominator for the probabilities
        denominator = np.sum(np.exp(v_values))

        # Calculating probabilities using the logistic function
        probabilities[utility.__name__] = logistic(v_values) / denominator

    return probabilities

# Defining the sample data and parameters
data = {
    'X1': [2, 3, 5, 7, 1, 8, 4, 5, 6, 7],
    'X2': [1, 5, 3, 8, 2, 7, 5, 9, 4, 2],
    'Sero': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

parameters = {
    'beta_01': 0.1,
    'beta_1': 0.5,
    'beta_2': 0.5,
    'beta_02': 1,
    'beta_03': 0
}

# Defining utility functions based on the given formulas
def utility_1(X1, X2):
    return parameters['beta_01'] + parameters['beta_1'] * X1 + parameters['beta_2'] * X2

def utility_2(X1, X2):
    return parameters['beta_02'] + parameters['beta_1'] * X1 + parameters['beta_2'] * X2

def utility_3(Sero):
    return parameters['beta_03'] + parameters['beta_1'] * Sero + parameters['beta_2'] * Sero

# Calling the main function and save the output to a text file
utilities = [utility_1, utility_2, utility_3]
probabilities = calculate_probabilities(parameters, data, utilities)

# Saving the output to a text file
with open('output.txt', 'w') as f:
    for utility, probs in probabilities.items():
        f.write(f'{utility}: {probs}\n')
