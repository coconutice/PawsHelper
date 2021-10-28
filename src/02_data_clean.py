import pandas as pd
import seaborn as sns
import numpy as np
df_join = pd.read_csv("../data/Austin_Animal_Center_Joined.csv")

df_clean = df_join[(~df_join.sex_upon_intake.isnull()) | (~df_join.intake_datetime.isnull())]
df_clean['intake_datetime'] = pd.to_datetime(df_clean['intake_datetime'])
df_clean['outcome_datetime'] = pd.to_datetime(df_clean['outcome_datetime'])
df_clean['date_of_birth'] = pd.to_datetime(df_clean['date_of_birth'])

df_clean.loc[df_clean['name'].isnull(), "has_name"] = 0
df_clean.loc[df_clean['name'] == df_clean['animal_id'], "has_name"] = 0
df_clean.loc[~df_clean['name'].isnull(), "has_name"] = 1

def convertAge(age):
  age = str(age).lower()
  if age != "nan":
    age_list = age.split()
    if "year" in age:
      return int(age_list[0])*365
    elif "month" in age:
      return int(age_list[0])*30
    elif "week" in age:
      return int(age_list[0])*7
    elif "day" in age:
      return int(age_list[0])*1
    else:
      return np.nan
  return np.nan

def getBirthSex(sex_upon_intake):
  sex_upon_intake = str(sex_upon_intake)
  if "Male" in sex_upon_intake:
    return "Male"
  elif "Female" in sex_upon_intake:
    return "Female"
  return np.nan

def isPureColor(color):
  color = str(color)
  if color != "nan":
    color_list = color.split("/")
    if "Tricolor" in color_list:
      return 0
    if len(color_list) > 1:
      return 0
    else:
      return 1
  else:
    return np.nan


def sex_changed(sex_upon_outcome):
  sex = str(sex_upon_outcome).lower()
  if ("splayed" in sex) or ("neutered" in sex):
    return 1
  elif ("unknown" in sex) or ("nan" in sex):
    return np.nan
  return 0


df_clean['age_upon_intake_day'] = df_clean.age_upon_intake.apply(convertAge)
df_clean['age_upon_outcome_day'] = df_clean.age_upon_outcome.apply(convertAge)
# 8 rows having negatives
df_clean = df_clean[(df_clean.age_upon_intake_day >=0) | (df_clean.age_upon_intake_day.isnull()) ]
df_clean = df_clean[(df_clean.age_upon_outcome_day >=0) | (df_clean.age_upon_outcome_day.isnull()) ]
df_clean['birth_sex'] = df_clean.sex_upon_intake.apply(getBirthSex)
df_clean['pure_color'] = df_clean.color.apply(isPureColor)
df_clean['sex_changed'] = df_clean.sex_upon_outcome.apply(sex_changed)

df_clean.to_csv("../data/Austin_Animal_Center_Cleaned.csv", index=False)
