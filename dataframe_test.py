import pandas as pd
import plotly.express as px
import matplotlib as mpl
import random
pd.options.plotting.backend = "plotly"



# def create_data_frameminutes(self) -> :
#     __col_lst = [str(i) for i in range(0,60)] 
#     df = pd.DataFrame(__col_lst)
#     return df

__col_lst = [i for i in range(0,60)] 
df = pd.DataFrame(columns=[i for i in range(0,60)])

# df = create_data_frameminutes()

new_row = [0]*60

df.loc['event_type1'] = new_row
df.loc['event_type2'] = new_row
df.loc['event_type3'] = new_row

# df.loc['event_type1'][57] = 3
for i in range(0,60):
    df.loc['event_type1'][i] = random.randint(0,10)
    df.loc['event_type2'][i] = random.randint(0,10)
    df.loc['event_type3'][i] = random.randint(0,10)

df[58] = 5


fig = df.T.plot.bar()

fig.show()