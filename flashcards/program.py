import pandas as pd
df = pd.read_csv('words.csv')

for i in range(0, len(df)):
    print(df['word'][i])
    ip = input('Enter anything to see the answer: ')
    print(df['meaning'][i] + '\n\n')