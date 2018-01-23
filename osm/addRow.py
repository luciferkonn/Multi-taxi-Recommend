import pandas as pd

reader = pd.read_csv('13_01_01_sorted.csv', iterator=True)

header = True
try:
    df = reader.get_chunk(500000)
    df['new column'] = 'a'
    df.to_csv('13_01_01_new.csv', mode='a', index=False, header = header)

    header = False

except StopIteration as err:
    print("StopIteration:"+ str(err))
