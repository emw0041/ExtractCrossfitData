import convert
import pandas as pd

def athlete(ath: pd.DataFrame,drop_cols: list) -> pd.DataFrame:
    ath.replace('',pd.NA, inplace=True)
    ath.columns = map(str.lower, ath.columns)
    ath['affiliateid'].replace('None',999999,inplace=True)
    ath.drop(ath.columns[drop_cols],axis=1,inplace=True)
    ath['height'] = ath['height'].map(convert.height,na_action='ignore')
    ath['weight'] = ath['weight'].map(convert.weight,na_action='ignore')
    return ath

def comp_id(comp: pd.DataFrame) -> pd.DataFrame:
    comp = pd.concat([comp, comp], axis=0, ignore_index=True)
    comp = comp.astype(int)
    comp = comp.rename(columns={0:'competitorId'})
    return comp

def score(score: pd.DataFrame, drop_cols: list) -> pd.DataFrame:
    score.columns = map(str.lower, score.columns)
    score.drop(columns=drop_cols,inplace=True,errors='ignore')
    score.replace('',pd.NA, inplace=True)
    score = score.rename(columns={'ordinal': 'event', 'score': 'total_score', 'scoredisplay': 'event_score', 'breakdown': 'reps'})
    return score
