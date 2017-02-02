import os
import json
import requests
import ConfigParser
from easydict import EasyDict as edict
from datetime import datetime
from dacs import iso2DACS


#funtions for debugging
def pp(output):
	print (json.dumps(output, indent=2))
def serializeOutput(filePath, output):
	f = open(filePath, "w")
	f.write(json.dumps(output, indent=2))
	f.close
	
#error handler
def checkError(response):
	if not response.status_code == 200:
		print ("ERROR: HTTP Response " + str(response.status_code))
		try:
			pp(response.json())
			log = open("aspace.log", "a")
			log.write("\n" + str(datetime.now()) + "  --  " + "ERROR: HTTP Response " + str(response.status_code) + "\n" + json.dumps(response.json(), indent=2))
			log.close()
		except:
			print (response.status_code)
			log = open("aspace.log", "a")
			log.write("\n" + str(datetime.now()) + "  --  " + "ERROR: HTTP Response " + str(response.status_code))
			log.close()
	
#reads config file for lower functions
def readConfig():
	__location__ = os.path.dirname(os.path.realpath(__file__))

	#load config file from same directory
	configPath = os.path.join(__location__, "local_settings.cfg")
	config = ConfigParser.ConfigParser()
	config.read(configPath)
	return config
	
#writes the config file back
def writeConfig(config):
	__location__ = os.path.dirname(os.path.realpath(__file__))

	#load config file from same directory
	configPath = os.path.join(__location__, "local_settings.cfg")
	with open(configPath, 'w') as f:
		config.write(f)
	
#basic function to get ASpace login details from a config file
def getLogin():
	config = readConfig()
	
	#make dictionary with basic ASpace login info
	aspaceLogin = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'user': config.get('ArchivesSpace', 'user'), 'password': config.get('ArchivesSpace', 'password')}
	return aspaceLogin

	
#function to update the URL in the config file
def setURL(URL):
	config = readConfig()
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'baseURL', URL)
	writeConfig(config)
	print "URL path updated"

#function to update the user in the config file
def setUser(user):
	config = readConfig()
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'user', user)
	writeConfig(config)
	print "User updated"
	
#function to update the URL in the config file
def setPassword(password):
	config = readConfig()	
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'password', password)
	writeConfig(config)
	print "Password updated"

#function to get an ArchivesSpace session
def getSession():

	#get dictionary of login details
	aspaceLogin = getLogin()
		
	#inital request for session
	r = requests.post(aspaceLogin["baseURL"] + "/users/" + aspaceLogin["user"]  + "/login", data = {"password":aspaceLogin["password"]})
	checkError(r)	
	print ("ASpace Connection Successful")
	sessionID = r.json()["session"]
	session = {'X-ArchivesSpace-Session':sessionID}
	return session
		


#gets an indented list of keys from a ASpace json object
def fields(jsonObject):
	fieldsSet = ""
	def listFields(jsonObject, fieldList):
		if not isinstance(jsonObject, dict):
			for item in jsonObject:
				for key, value in item.items():
					if key.lower() == "type":
						fieldList = fieldList + "\n		" + key + ": " + value
					else:
						fieldList = fieldList + "\n		" + key
		else:
			for key, value in jsonObject.items():
				if isinstance(jsonObject[key], dict) or isinstance(jsonObject[key], list):
					field = key + "\n	" + listFields(jsonObject[key], "")
				else:
					field = key
					
				if len(fieldList) == 0:
					fieldList = "	" + field
				else:
					fieldList = fieldList + "\n	" + field
		return fieldList
	fieldsSet = listFields(jsonObject, fieldsSet)	
	return fieldsSet

	
def makeObject(jsonData):
	#handles paginated returns
	if "results" in jsonData:
		jsonData = jsonData["results"]
		
	if isinstance(jsonData, list):
	
		itemList = []
		#checks if list of json objects or just a single one
		for thing in jsonData:
			object = edict(thing)
			object.fields = fields(thing)
			object.json = thing
			itemList.append(object)
		return itemList

	else:
		#single json object
		object = edict(jsonData)
		object.fields = fields(jsonData)
		object.json = jsonData
		return object
		
################################################################
#OBJECTS
################################################################	

class Accession(object):

	def __init__(self):
			
		#manditory stuff
		self.id = ""
		self.id_1 = ""
		self.id_2 = ""
		self.id_3 = ""
		self.date = ""
		
		#common stuff
		self.title = ""
		self.content = ""
		self.condition = ""
		self.provenance = ""
		
		#restrictions
		self.restrictionsApply = ""
		self.accessRestrictions = ""
		self.accessRestrictions = ""
		self.useRestrictions = ""
		self.useRestrictions = ""
		
		#if you really need them
		self.acquisitionType = ""
		self.resourceType = ""
		self.disposition = ""
		self.inventory = ""
		self.retentionRule = ""
		
		#full json set
		self.json = {}
		
	def toJSON(self):
		pass
		
	def fromJSON(self, jsonSet):
		pass
		




################################################################
#GETTING LIST OF LARGE SETS: ACCESSIONS, RESOURCES, etc.
################################################################	

def getResourceList(session, repo):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	resourceData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources?all_ids=true",  headers=session)
	checkError(resourceData)
	return resourceData.json()
	
#get a list of accession numbers
def getAccessionList(session, repo):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	accessionData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/accessions?all_ids=true",  headers=session)
	checkError(accessionData)
	return accessionData.json()
		
################################################################
#REQUEST FUNCTIONS
################################################################	
		
def singleRequest(session, repo, number, requestType):
	#get ASpace Login info
	aspaceLogin = getLogin()

	requestData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/" + requestType + "/" + str(number),  headers=session)
	checkError(requestData)
	returnList = makeObject(requestData.json())
	return returnList
		
def multipleRequest(session, repo, param, requestType):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	#get list of all resources and loop thorugh them
	if param.lower().strip() == "all":
		if requestType.lower() == "resources":
			numberSet = getResourceList(session, repo)
		elif requestType.lower() == "accessions":
			numberSet = getAccessionList(session, repo)
		returnList = []
		for number in numberSet:
			requestData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/" + requestType + "/" + str(number),  headers=session)
			checkError(requestData)
			asObject = makeObject(requestData.json())
			returnList.append(asObject)
		return returnList
	else:
		if "-" in param:
			range = int(param.split("-")[1]) - int(param.split("-")[0])
			page = int(param.split("-")[0]) / range
			limiter = "page=" + str(page + 1) + "&page_size=" + str(range)
		elif "," in param:
			limiter = "id_set=" + param.replace(" ", "")
		else:
			print ("Invalid parameter, requires 'all', set (53, 75, 120), or paginated (1-100")
		
		requestData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/" + requestType + "?" + limiter,  headers=session)
		checkError(requestData)
		returnList = makeObject(requestData.json())
		return returnList
		
def postObject(session, object):

	#get ASpace Login info
	aspaceLogin = getLogin()
			
	uri = object.uri
	del object['fields']
	del object['json']
	objectString = json.dumps(object)
	
	postData = requests.post(aspaceLogin["baseURL"] + str(url), data=objectString, headers=session)
	checkError(postData)
	if postData.status_code == 200:
		print (str(uri) + " posted back to ArchivesSpace")
		
def deleteObject(session, object):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	uri = object.uri
	deleteRequest = requests.delete(aspaceLogin["baseURL"] + str(uri),  headers=session)
	checkError(deleteRequest)
	if deleteRequest.status_code == 200:
		print (str(URI) + " Deleted")
		
		
################################################################
#REPOSITORIES
################################################################
		
def getRepositories(session):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	repoData = requests.get(aspaceLogin["baseURL"] + "/repositories",  headers=session)
	checkError(repoData)
	repoList = makeObject(repoData.json())
	return repoList


################################################################
#RESOURCES
################################################################
		

#returns a list of resources you can iterate though with all, a set, or a range of resource numbers
def getResources(session, repo, param):

	resourceList = multipleRequest(session, repo, param, "resources")
	return resourceList
		
#return resource object with number
def getResource(session, repo, number):

	resourceList = singleRequest(session, repo, number, "resources")
	return resourceList
	
#creates an empty resource
def makeResource():
	resourceString = '{"jsonmodel_type":"resource","external_ids":[],"subjects":[],"linked_events":[],"extents":[],"dates":[],"external_documents":[],"rights_statements":[],"linked_agents":[],"restrictions":false,"revision_statements":[],"instances":[],"deaccessions":[],"related_accessions":[],"classifications":[],"notes":[],"title":"","id_0":"","level":"","language":"","ead_id":"","finding_aid_date":"","ead_location":""}'
	emptyResource = json.loads(resourceString)
	resourceObject = makeObject(emptyResource)
	return resourceObject
	
def postResource(session, repo, resoruceObject):

	#get ASpace Login info
	aspaceLogin = getLogin()
			
	del resoruceObject['fields']
	del resoruceObject['json']
	resourceString = json.dumps(resoruceObject)
	
	postResource = requests.post(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources", data=resourceString, headers=session)
	checkError(postResource)
	if postResource.status_code == 200:
		print ("New resource posted to ArchivesSpace")

#return resource tree object
def getTree(session, resourceObject):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	uri = resourceObject.uri	
	
	treeData = requests.get(aspaceLogin["baseURL"] + str(uri) + "/tree",  headers=session)
	checkError(treeData)
	treeObject = makeObject(treeData.json())
	return treeObject
	
################################################################
#ARCHIVAL OBJECTS
################################################################
	
#return resource tree object
def getArchObj(session, recordUri):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	aoData = requests.get(aspaceLogin["baseURL"] + str(recordUri),  headers=session)
	checkError(aoData)
	aoObject = makeObject(aoData.json())
	return aoObject
	
	
################################################################
#ACCESSIONS
################################################################

#returns a list of accessions you can iterate though with all, a set, or a range of resource numbers
def getAccessions(session, repo, param):

	accessionList = multipleRequest(session, repo, param, "accessions")
	return accessionList

#return accession object with number
def getAccession(session, repo, number):

	resourceObject = singleRequest(session, repo, number, "accessions")
	return resourceObject
	
#makes an empty accession object
def makeAccession():
	accessionString = '{"external_ids":[], "related_accessions":[], "classifications":[], "subjects":[], "linked_events":[], "extents":[], "dates":[], "external_documents":[], "rights_statements":[], "deaccessions":[], "related_resources":[], "restrictions_apply":false, "access_restrictions":false, "use_restrictions":false, "linked_agents":[], "instances":[], "id_0":"", "id_1":"", "title":"","content_description":"","condition_description":"","accession_date":""}'
	emptyAccession = json.loads(accessionString)
	accessionObject = makeObject(emptyAccession)
	accessionObject.accession_date = datetime.now().isoformat().split("T")[0]
	return accessionObject
	
def postAccession(session, repo, accessionObject):

	#get ASpace Login info
	aspaceLogin = getLogin()
			
	del accessionObject['fields']
	del accessionObject['json']
	accessionString = json.dumps(accessionObject)
	
	postAccession = requests.post(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/accessions", data=accessionString, headers=session)
	checkError(postAccession)
	if postAccession.status_code == 200:
		print ("New accession posted to ArchivesSpace")
		
		
################################################################
#EXTENTS AND DATES
################################################################

#adds an extent object
def makeExtent(object, number, type):
	extent = {"jsonmodel_type":"extent", "portion":"whole","number":str(number),"extent_type":str(type)}
	if object.extents is None:
		object.extents = [extent]
	else:
		object.extents.append(extent)
	return object


#adds a date object
def makeDate(object, dateBegin, dateEnd):
	if len(dateEnd) > 0:
		date = {"jsonmodel_type":"date","date_type":"inclusive","label":"creation","begin":str(dateBegin),"end":str(dateEnd),"expression":iso2DACS(str(dateBegin) + "/" + str(dateEnd))}
	else:
		date = {"jsonmodel_type":"date","date_type":"inclusive","label":"creation","begin":str(dateBegin),"expression":iso2DACS(str(dateBegin))}
	if object.dates is None:
		object.dates = [date]
	else:
		object.dates.append(date)
	return object
	
#adds a single part notes
def makeSingleNote(object, type, text):
	note = {"type": type, "jsonmodel_type": "note_singlepart", "content": [text]}
	if object.notes is None:
		object.notes = [note]
	else:
		object.notes.append(note)
	return object
	
#add a container instance with a location
def addContainerLocation(object, containerName, location):
	instance = {"jsonmodel_type":"instance", "is_representative":False,"instance_type":"mixed_materials"}
	instance["container"] = 
	
	