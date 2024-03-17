import pandas as pd
from sqlalchemy import create_engine, text
import grequests
import requests
import time
import clean
import schema

#Divisions: 1=male, 2=female. 
#Regions: world=0, Africa=30, Asia=28, Europe=29, Oceania=32, South America=33, North America East=35, North America West=34
time_start = time.time()
engine = create_engine('postgresql://postgres:password@localhost:5432/crossfit') #Define the sql database connection

def exception_handler(request, exception):
	print(exception)

with engine.begin() as cnx:
				cnx.execute(text(f'DROP TABLE IF EXISTS athletes'))
				cnx.execute(text(f'DROP TABLE IF EXISTS scores'))

for j in range(1,3):
	division = j
	base_url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/open/2024/leaderboards'
	main_query = f'view=0&division={division}&region=0&scaled=0&sort=0&page='
	r = requests.get(str(f'{base_url}?{main_query}1'))
	data = r.json()
	page_count = data['pagination']['totalPages']
	print(division)
	print(page_count)
	page_count = 1
	max_async_req = 50 #Used to ensure response from grequests does not return None for some links
	blocks = page_count // max_async_req #Separate the total number of pages into distinct sets to be sent to grequest
	blocks = blocks + 1 if page_count % max_async_req != 0 else blocks #Add 1 additional block for the final page which doesnt contain a full 50 entries
	url_start = 1

	for n in range(1,blocks+1):
		if n == blocks:
			url_end = page_count + 1
		else:
			url_end = max_async_req * n + 1
		urls = [f'{base_url}?{main_query}{k}' for k in range(url_start,url_end)]
		reqs = [grequests.get(link) for link in urls]
		responses = grequests.map(reqs, exception_handler=exception_handler)
		url_start += max_async_req
		print(' ')
		print('Extracting Block ',n,'...')
		print(' ')
		for idx,response in enumerate(responses,start=1):
			if response == 'None':
				raise Exception('ERROR, RETURNING NONE')
			data = response.json()
			athletes = pd.DataFrame(data["leaderboardRows"][i]["entrant"] for i in range(len(data["leaderboardRows"])))
			athletes = clean.athlete(athletes,[4,5,10,19])
			competitorId = pd.DataFrame(data["leaderboardRows"][k]["entrant"]["competitorId"] for k in range(len(data["leaderboardRows"])))
			competitorId = clean.comp_id(competitorId)
			scores = pd.concat([pd.DataFrame(data["leaderboardRows"][m]["scores"][p] for p in range (0,2) for m in range(len(data["leaderboardRows"]))),competitorId], axis=1)
			scores = clean.score(scores,[3,5,6,8,9,10,12,13,14])
			scores.to_sql(f'scores',engine,if_exists='append',dtype=schema.score,index=False)
			athletes.to_sql(f'athletes',engine,if_exists='append',dtype=schema.athlete,index=False)
			
print("Time Elapsed:",time.time()-time_start)
