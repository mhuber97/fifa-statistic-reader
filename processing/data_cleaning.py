import re

import numpy as np
from utils.regex_matcher import REMatcher


def transformation_row_home_possession(r):
    if (r.h_possession == -1) and (r.a_possession > 0) and (r.a_possession < 100):
        r.h_possession = 100 - r.a_possession 
    return r

def transformation_row_away_possession(r):
    if (r.a_possession == -1) and (r.h_possession > 0) and (r.h_possession < 100):
        r.a_possession = 100 - r.h_possession 
    return r

def correct_time(r):
    if ("ET" in r.time):
        r.time = "120:00"

    if ("PEN" in r.time):
        m = REMatcher(r.time)
        if m.match(r"(\d+)\W(\d+)"):
            r.h_penalty_score = int(m.group(1))
            r.a_penalty_score = int(m.group(2))
        else:
            r.h_penalty_score = 0
            r.a_penalty_score = 0
        r.time = "120:00"

    return r

def correcting_data(df):

  # fill in missing home possession given away possession
  df = df.apply(
      transformation_row_home_possession,
      axis=1
  )

  # fill in missing away possession given away possession
  df = df.apply(
      transformation_row_away_possession,
      axis=1
  )
  
  # correct time
  df["h_penalty_score"], df["a_penalty_score"] = [np.nan, np.nan]
  df = df.apply(
      correct_time,
      axis=1
  )

  return df
