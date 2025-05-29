import pandas as pd
import numpy as np
import statsmodels.api as sm


if __name__ == "__main__":
    time_df = pd.read_excel("./Scratch/570data.xlsx")
    time_df = time_df.drop(["County", "State", "Region"], axis=1)
    time_df.drop_duplicates(inplace=True)

    screen_time = time_df["Screen time hours"].dropna()
    mood_percentage = time_df["Poor mood percent of time"].dropna()
   

    correlation = screen_time.corr(mood_percentage)
    print("Correlation between screen time and mood: " + str(correlation))
    
    # Perform linear regression
    x = sm.add_constant(screen_time)
    y = mood_percentage

    model = sm.OLS(y, x).fit()

    print("Linear Regression Results:")
    print(model.summary())
    # Predict mood percentage based on screen time



