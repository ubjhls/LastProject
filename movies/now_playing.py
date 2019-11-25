import http.client
import pprint
import json

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/movie/now_playing?page=1&language=ko-KR&api_key=1dfd52c8a24a0f38f40efe41c86be13b", payload)

res = conn.getresponse()
data = res.read()
data = data.decode("utf-8")
pprint.pprint(data)

with open('nowplay.json', 'w', encoding='utf-8') as make_file:
    json.dump(data, make_file,ensure_ascii=False, indent="\t")
