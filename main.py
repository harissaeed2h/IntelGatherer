import time

from selenium import webdriver
from defines import *

driver = webdriver.Firefox()

#Template ===> query = {"sites":[], "keywords":[], "include":[], "exclude":[]}

def dryRun():
	query = "Gruppe 6"
	url = makeSearchURL(query)
	driver.get(url)
	input("Press enter if captcha is solved..._")

def loadPlan():
	def processRawPlans(planRaw):
		planSplitTemp = planRaw.split("---Plan---")
		sites = planSplitTemp[0].split("\n")
		urlIncludes = planSplitTemp[1].split("\n")
		urlExcludes = planSplitTemp[2].split("\n")
		return sites, urlIncludes, urlExcludes
	try:
		with open("plan.p", "r") as f:
			planRaw = f.read()
	except:
		print("Error 001: Unable to load plan file")

	sites, urlIncludes, urlExcludes = processRawPlans(planRaw)
	plan = {"sites":sites, "urlIncludes":urlIncludes, "urlExcludes":urlExcludes}
	return plan

def buildQuery(plan):
	sites = plan["sites"]
	urlIncludes = plan["urlIncludes"]
	urlExcludes = plan["urlExcludes"]
	sitesIncludeString = ""
	urlIncludeString = ""
	urlExcludeString = ""
	for site in sites:
		if not site == "":
			sitesIncludeString += f"site:{site}"
	for urlInclude in urlIncludes:
		if not urlInclude == "":
			urlIncludeString += f"'{urlInclude}'"
	for urlExclude in urlExcludes:
		if not urlExclude == "":
			urlExcludeString += f"-'{urlExclude}'"
	query = f"{sitesIncludeString} {urlIncludeString} {urlExcludeString}"
	return query

def makeSearchURL(query, templateName="google"):
	GoogleURLTemplate = f"https://www.google.com/search?q={query}"
	YandexURLTemplate = f"https://yandex.com/search?text={query}"
	DuckDuckGoTemplate = f"https://www.duckduckgo.com/?q={query}"
	BingURLTemplate = f"https://www.bing.com/search?q={query}"
	templates = {"google":GoogleURLTemplate, "yandex":YandexURLTemplate, "duckduckgo":DuckDuckGoTemplate, "bing":BingURLTemplate}
	return templates[templateName]

def getUrlContent(url): #no need to call this, call getContent instead
	driver.get(url)
	time.sleep(0.5)
	contentText = driver.page_source
	return contentText

def getContent(query):
	url = makeSearchURL(query)
	contentText = getUrlContent(url)
	time.sleep(0.5)
	return contentText

def saveContentText(contentText, query):
	with open(f"output/{query.replace("/", "!")}", "w") as f:
		f.write(contentText)
		return 0

def main():
	dryRun()
	plan = loadPlan()
	query = buildQuery(plan)
	contentText = getContent(query)
	saveContentText(contentText, query)

	driver.quit()

if __name__ == "__main__":
	main()