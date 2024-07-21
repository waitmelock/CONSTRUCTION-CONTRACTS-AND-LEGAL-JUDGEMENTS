import pandas as pd

# Creating the first Dataframe using dictionary
df1 = df = pd.DataFrame({"a": [1, 2, 3, 4],
                         "b": [5, 6, 7, 8]})

# Append Dict as row to DataFrame
new_row = {"a": 10, "b": 10}
df2 = df.append(new_row, ignore_index=True)

print(df2)