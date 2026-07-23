import requests
import json

handle = input("enter handle: ")

url = f"https://codeforces.com/api/user.status?handle={handle}"

response = requests.get(url)

if response.status_code != 200:
  print("HTTP error")
  exit()

data = response.json()
# print(len(data["result"]))
# print(json.dumps(data, indent=2))

solved_problem = set(())
tag_stat = {}

for submission in data["result"]:
  if submission["verdict"] != "OK":
    continue
  problem = submission["problem"]
  problemId = str(problem["contestId"]) + "_" + problem["index"]
  print(problemId)
  print(json.dumps(problem, indent=2))
  if "rating" not in problem:
    continue
  rating = problem["rating"]
  if problemId in solved_problem:
    continue
  solved_problem.add(problemId)
  for tag in problem["tags"]:
    if tag not in tag_stat:
      tag_stat[tag] = {}

    if rating in tag_stat[tag]:
      tag_stat[tag][rating] += 1
    else:
      tag_stat[tag][rating] = 1

# print(solved_problem)
print(f"# solved problems: {len(solved_problem)}")

tag_power = {}

for tag in tag_stat.keys():
  power = 0
  count = 0
  for rating in tag_stat[tag].keys():
    thisCount = tag_stat[tag][rating]
    power += rating * thisCount
    count += thisCount
  tag_power[tag] = power / count


print(tag_power)