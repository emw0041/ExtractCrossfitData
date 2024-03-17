from sqlalchemy.types import *

athlete = {
    "competitorid": Integer,
    "competitorname": VARCHAR,
    "firstname": VARCHAR,
    "lastname": VARCHAR,
    "gender": VARCHAR,
    "profilepics3key": VARCHAR,
    "countryoforigincode":VARCHAR,
    "countryoforiginname": VARCHAR,
    "regionid": Integer,
    "regionname": VARCHAR,
    "divisionid": Integer,
    "affiliateid": Integer,
    "affiliatename": VARCHAR,
    "age": Integer,
    "height": Integer,
    "weight": VARCHAR
}

score = {
    "event": Integer,
    "rank": Integer,
    "total_score": Integer,
    "event_score": VARCHAR,
    "scaled": Integer,
    "reps": VARCHAR,
    "affiliate": VARCHAR,
    "competitorid": Integer
}
