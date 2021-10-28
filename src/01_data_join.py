import pandas as pd
import seaborn as sns
import numpy as np

df_intakes = pd.read_csv("../data/Austin_Animal_Center_Intakes.csv")
df_outcomes = pd.read_csv("../data/Austin_Animal_Center_Outcomes.csv")

# Some repetitive `Animal ID`, what do we do?
# Step1:
# Vertically stack intakes and outcomes (130k rows + 130k rows = 265k rows)
# Action_type = intake_type U outcome_type (9 types)
# e.g.
# Animal ID，datetime, action_type, XXX, XXX, XXX\
# A12345, 08/09/2019, intake,           aa,  aa, aa\
# A12345, 09/09/2019, outcome,           aa,  aa, aa\
# A12345, 10/12/2019, intake,           aa,  aa, aa\
# A12345, 10/15/2019, outcome,           aa,  aa, aa\
# A23456, 05/04/2019, intake ,          aa, aa, aa\

df_join = df_intakes.append(df_outcomes, sort=False)
mask = df_join['Intake Type'].isna()
df_join['action_type'] = "nan"
df_join['action_type'][mask] = "outcome"
df_join['action_type'][~mask] = "intake"
df_join = df_join.reset_index(drop=True)
df_join['DateTime'] = pd.to_datetime(df_join['DateTime'])  # make sure DateTime is datetime
df_join_sorted = df_join.sort_values(by=['Animal ID', 'DateTime'])

# merge two "neighboring" rows

df_join_sorted = df_join_sorted.reset_index(drop=True)

prev = ""
prevId = ""
data_in_out = []
data_row = []
incolumns = ['Animal ID', 'Name', 'DateTime', 'Found Location',
             'Intake Type', 'Intake Condition', 'Animal Type', 'Sex upon Intake',
             'Age upon Intake', 'Breed', 'Color']

outcolumns = ['DateTime', 'Date of Birth', 'Outcome Type',
              'Outcome Subtype', 'Sex upon Outcome', 'Age upon Outcome']
for idx, row in df_join_sorted.iterrows():
    t, tid = row['action_type'], row['Animal ID']
    if tid == prevId and t == "outcome" and prev == "intake":
        # combine and append
        data_row.extend(row[outcolumns].values.tolist())
        data_in_out.append(data_row)
        data_row = []
    else:
        if len(data_row) != 0:
            if prev == "intake":
                tmp = df_join_sorted.iloc[idx - 1][outcolumns].values.tolist()
                tmp[0] = np.nan
                data_row.extend(tmp)
            data_in_out.append(data_row)
            data_row = []

        if t == "intake":
            data_row = row[incolumns].values.tolist()
        elif t == "outcome":
            tmp = row[incolumns].values.tolist()
            tmp[2] = np.nan
            data_row = tmp
            data_row.extend(row[outcolumns].values.tolist())
            data_in_out.append(data_row)
            data_row = []
        # anyways, we need incolumns
    prev, prevId = t, tid
if len(data_row) != 0:
    data_row.extend(df_join_sorted.iloc[-1][outcolumns].values.tolist())
    data_in_out.append(data_row)

df_in_out = pd.DataFrame(data_in_out, columns=['animal_id', 'name', 'intake_datetime', 'found_location',
                                               'intake_type', 'intake_condition', 'animal_type', 'sex_upon_intake',
                                               'age_upon_intake', 'breed', 'color', 'outcome_datetime', 'date_of_birth',
                                               'outcome_type',
                                               'outcome_subtype', 'sex_upon_outcome', 'age_upon_outcome'])

df_in_out.to_csv("../data/Austin_Animal_Center_Joined.csv", index=False)
