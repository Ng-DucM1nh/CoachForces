import requests
import json

def analyze_user(handle):
  if not isinstance(handle, str):
    print("invalid handle, expected a string value")
    return -1
  
  url = f"https://codeforces.com/api/user.status?handle={handle}"

  response = requests.get(url)

  if response.status_code != 200:
    print("HTTP error")
    return -1

  data = response.json()
  # print(len(data["result"]))
  # print(json.dumps(data, indent=2))

  solved_problem = set(())
  tag_stat = {}

  # grab all solved problems
  for submission in data["result"]:
    if submission["verdict"] != "OK":
      continue

    problem = submission["problem"]
    problemId = str(problem["contestId"]) + "_" + problem["index"]
    # print(problemId)
    # print(json.dumps(problem, indent=2))
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

  print(f"# solved problems: {len(solved_problem)}")

  tag_strength_value = {}

  for tag in tag_stat.keys():
    # skip irregular tags
    if tag[0] == '*':
      continue

    # calculate strength value of user for each tag
    power = 0
    count = 0
    for rating in tag_stat[tag].keys():
      thisCount = tag_stat[tag][rating]
      power += rating * thisCount
      count += thisCount
    tag_strength_value[tag] = power / count

  return tag_strength_value



handle = input("enter handle: ")

tag_strength = analyze_user(handle)
if tag_strength == -1:
  exit()

for tag in tag_strength.keys():
  print(f"{tag}: {tag_strength[tag]}")