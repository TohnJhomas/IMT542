import pandas as pd

time_df = pd.read_excel("./Scratch/570data.xlsx")
time_df = time_df.drop(["County"], axis=1)

print(time_df.shape)

time_df.drop_duplicates(inplace=True)

print(time_df.shape)
