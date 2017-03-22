
def mainShelf(coordinates):
	coordList = {"Building": "", "Floor": "", "Room": "", "Area": "", "Label1": "", "Place1": "", "Label2": "", "Place2": "", "Label3": "", "Place3": "", "Title": "", "Note": ""}
	if not len(coordinates.split("-")) == 4:
		print ("Error, shelf is in main storage, but is incorrect: " + coordinates)
	else:
		if coordinates.lower().strip().startswith("sb17"):
			coordList["Building"] = "Main Library"
			coordList["Floor"] = "Basement"
			coordList["Room"] = "SB17"
			coordList["Title"] = "Main Library, Basement, SB17 [Row: " + coordinates.split("-")[1] + ", Bay: " + coordinates.split("-")[2] + ", Shelf: " + coordinates.split("-")[3] + "]"
		elif coordinates.lower().strip().startswith("sb14"):
			coordList["Building"] = "Main Library"
			coordList["Floor"] = "Basement"
			coordList["Room"] = "SB14"
			coordList["Title"] = "Main Library, Basement, SB14 [Row: " + coordinates.split("-")[1] + ", Bay: " + coordinates.split("-")[2] + ", Shelf: " + coordinates.split("-")[3] + "]"
		else:
			coordList["Building"] = "Science Library"
			coordList["Floor"] = "3"
			coordList["Room"] = "Main Storage"
			coordList["Area"] = coordinates.split("-")[0]
			coordList["Title"] = "Science Library, 3, Main Storage, " + coordinates.split("-")[0] + " [Row: " + coordinates.split("-")[1] + ", Bay: " + coordinates.split("-")[2] + ", Shelf: " + coordinates.split("-")[3] + "]"
			
		coordList["Label1"] = "Row"
		coordList["Place1"] = coordinates.split("-")[1]
		coordList["Label2"] = "Bay"
		coordList["Place2"] = coordinates.split("-")[2]
		coordList["Label3"] = "Shelf"
		coordList["Place3"] = coordinates.split("-")[3]
		
	return coordList

	
def location2ASpace(coordinates, note = None):

	mainAreas = ["A", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
	
	coordList = {"Building": "", "Floor": "", "Room": "", "Area": "", "Label1": "", "Place1": "", "Label2": "", "Place2": "", "Label3": "", "Place3": "", "Title": "", "Note": ""}
	
	#check if single or range
	if "/" in coordinates:
	
		isRange = True
		totalList = []
		if "SB17" in coordinates or "SB14" in coordinates:
			highShelf = 8
		else:
			highShelf = 9
		coord1, coord2Note = coordinates.split("/")
		if "(" in coord2Note:
			coord2 = coord2Note.split("(")[0].strip()
		else:
			coord2 = coord2Note
		if coord1.split("-")[2] == coord2.split("-")[2]:
			shelf1 = int(coord1.split("-")[3])
			shelf2 = int(coord2.split("-")[3])
			for shelf in range(shelf1, shelf2 + 1):
				pred = coord1.split("-")[0] + "-" +  coord1.split("-")[1] + "-" +  coord1.split("-")[2] + "-"
				coordList = mainShelf(pred + str(shelf))
				totalList.append(coordList)
			coordList = totalList
		else:
			coordStart = coordinates.split("-")[0] + "-" + coordinates.split("-")[1] + "-"
			#SB17-A-
			bay1 = int(coord1.split("-")[2])
			#1
			bay2 = int(coord2.split("-")[2])
			#2
			shelf1 =  int(coord1.split("-")[3])
			#1
			shelf2 = int(coord2.split("-")[3])
			#3
			for bay in range(bay1, bay2 + 1):
				if bay == bay1:
					for shelf in range(shelf1, highShelf):
						coordList = mainShelf(coordStart + str(bay) + "-" + str(shelf))
						totalList.append(coordList)
				elif bay == bay2:
					for shelf in range(1, shelf2 + 1):
						coordList = mainShelf(coordStart + str(bay) + "-" + str(shelf))
						totalList.append(coordList)
				else:
					for shelf in range(1, highShelf):
						coordList = mainShelf(coordStart + str(bay) + "-" + str(shelf))
						totalList.append(coordList)
			coordList = totalList
		if "(" in coord2Note:
			coordList["Note"] = coord2Note.split("(")[1].split(")")[0].strip()
	
	else:
		#single shelf
		isRange = False
		
		
		#check if in main stacks
		area = coordinates.split("-")[0]
		
		if "(" in coordinates:
			coordinates = coordinates.split("(")[0].strip()
		
		if area in mainAreas:
			#check if correct
			
			coordList = mainShelf(coordinates)
				
		elif coordinates.lower().startswith("rr"):
		
			coordList["Building"] = "Science Library"
			coordList["Floor"] = "3"
			coordList["Room"] = "Reading Room"
			coordList["Label1"] = "Shelf"
			coordList["Place1"] = coordinates.split("RR")[1]
			coordList["Title"] = "Science Library, 3, Reading Room [Shelf: " + coordinates.split("RR")[1] + "]"	
		
		elif coordinates.lower().startswith("ccbe"):
			#check if correct
			if coordinates.lower().strip() == "ccbe":
				coordList["Building"] = "Science Library"
				coordList["Floor"] = "LL"
				coordList["Room"] = "CCBE"
				coordList["Label1"] = "Room"
				coordList["Place1"] = "CCBE"
				coordList["Title"] = "Science Library, LL, CCBE [Room: CCBE]"
			elif not len(coordinates.split("-")) == 2:
				print ("Error, shelf is in CCBE, but is incorrect: " + coordinates)
			else:
				coordList["Building"] = "Science Library"
				coordList["Floor"] = "LL"
				coordList["Room"] = "CCBE"
				coordList["Label1"] = "Row"
				coordList["Place1"] = coordinates.split("-")[1]
				coordList["Title"] = "Science Library, LL, CCBE [Row: " + coordinates.split("-")[1] + "]"
		
		elif coordinates.lower().startswith("sb"):
			coordList["Building"] = "Main Library"
			coordList["Floor"] = "Basement"			
			coordList["Room"] = coordinates[:4].upper()
			
			if len(coordinates.strip()) == 4:
				coordList["Label1"] = "Room"
				coordList["Place1"] = coordinates.upper()
				coordList["Title"] = "Main Library, Basement, " + coordinates.upper() + " [Room: " + coordinates.upper() + "]"
			elif len(coordinates.strip()) == 10:
				coordList["Label1"] = "Row"
				coordList["Place1"] = coordinates.split("-")[1]
				coordList["Label2"] = "Bay"
				coordList["Place2"] = coordinates.split("-")[2]
				coordList["Label3"] = "Shelf"
				coordList["Place3"] = coordinates.split("-")[3]
				coordList["Title"] = "Main Library, Basement, " + coordinates.split("-")[0] + " [Row: " + coordinates.split("-")[1] + ", Bay: " + coordinates.split("-")[2] + ", Shelf: " + coordinates.split("-")[3] + "]"
				
			
			else:
				print ("Error, shelf is in SB, but is incorrect: " + coordinates)
				
		elif coordinates.split("-")[0] == "L":
		
			if not len(coordinates.split("-")) == 3:
				print ("Error, shelf is in flat storage, but is incorrect: " + coordinates)
			else:
				if coordinates.split("-")[1] == "1" or coordinates.split("-")[1] == "9":
					lType = "Drawer"
				else:
					lType = "Shelf"
				coordList["Building"] = "Science Library"
				coordList["Floor"] = "3"
				coordList["Room"] = "Main Storage"
				coordList["Area"] = coordinates.split("-")[0]
				coordList["Label1"] = "Bay"
				coordList["Place1"] = coordinates.split("-")[1]
				coordList["Label2"] = lType
				coordList["Place2"] = coordinates.split("-")[2]
				coordList["Title"] = "Science Library, 3, Main Storage, " + coordinates.split("-")[0] + " [Bay: " + coordinates.split("-")[1] + ", " + lType + ": " + coordinates.split("-")[2] + "]"				
			
		elif coordinates.lower().startswith("cold"):
			coordList["Building"] = "Science Library"
			coordList["Floor"] = "3"
			coordList["Room"] = "Cold Storage"
			if len(coordinates.split("-")) == 1:
				coordList["Label1"] = "Room"
				coordList["Place1"] = "Cold"
				coordList["Title"] = "Science Library, 3, Cold Storage [Room: Cold]"
			if len(coordinates.split("-")) == 3:
				coordList["Label1"] = "Bay"
				coordList["Place1"] = coordinates.split("-")[1]
				coordList["Label2"] = "Shelf"
				coordList["Place2"] = coordinates.split("-")[2]
				coordList["Title"] = 	"Science Library, 3, Cold Storage [Bay: " + coordinates.split("-")[1] + ", Shelf: " + coordinates.split("-")[2] + "]"
			elif len(coordinates.split("-")) == 4:
				coordList["Label1"] = "Cabinet"
				coordList["Place1"] = coordinates.split("-")[1]
				coordList["Label2"] = "Drawer"
				coordList["Place2"] = coordinates.split("-")[2]
				coordList["Label3"] = "Section"
				coordList["Place3"] = coordinates.split("-")[3]
				coordList["Title"] = "Science Library, 3, Cold Storage [Cabinet: " + coordinates.split("-")[1] + ", Drawer: " + coordinates.split("-")[2] + ", Section: " + coordinates.split("-")[3] + "]"
			elif coordinates.lower().strip() == "cold":
				coordList["Label1"] = "Room"
				coordList["Place1"] = "Cold"
				coordList["Title"] = "Science Library, 3, Cold Storage [Room: Cold]"			
			else:
				print ("Error, shelf is in cold room, but is incorrect: " + coordinates)	
		
		
		elif coordinates.lower().startswith("v"):
			coordList["Building"] = "Science Library"
			coordList["Floor"] = "3"
			coordList["Room"] = "Vault"
			coordList["Area"] = "V"
			if len(coordinates.split("-")) == 1:
				coordList["Label1"] = "Room"
				coordList["Place1"] = "Vault"
				coordList["Title"] = "Science Library, 3, Vault [Room: Vault]"
			elif len(coordinates.split("-")) == 4:
				coordList["Label1"] = "Row"
				coordList["Place1"] = coordinates.split("-")[1]
				coordList["Label2"] = "Bay"
				coordList["Place2"] = coordinates.split("-")[2]
				coordList["Label3"] = "Shelf"
				coordList["Place3"] = coordinates.split("-")[3]
				coordList["Title"] = "Science Library, 3, Vault [Row: " + coordinates.split("-")[1] + ", Bay: " + coordinates.split("-")[2] + ", Shelf: " + coordinates.split("-")[3] + "]" 
			elif len(coordinates.split("-")) == 5:
				coordList["Label1"] = "Row"
				coordList["Place1"] = coordinates.split("-")[2]
				coordList["Label2"] = "Bay"
				coordList["Place2"] = coordinates.split("-")[3]
				coordList["Label3"] = "Shelf"
				coordList["Place3"] = coordinates.split("-")[4]
				coordList["Title"] = "Science Library, 3, Vault [Row: " + coordinates.split("-")[2] + ", Bay: " + coordinates.split("-")[3] + ", Shelf: " + coordinates.split("-")[4] + "]" 
			else:
				print ("Error, shelf is in vault, but is incorrect: " + coordinates)	
		
		if "(" in coordinates:
			coordList["Note"] =  coordinates.split("(")[1].split(")")[0].strip()
	
		
	return coordList, isRange
	
def ASpace2Location(locationTitle):
	if "CCBE" in locationTitle:
		#index out of rance for apap306?
		locationOutput = "CCBE-" + locationTitle.split("Row: ")[1].replace("]", "")
		
	elif "Reading Room" in locationTitle:
		locationOutput = "RR-" + locationTitle.split("Shelf: ")[1].replace("]", "")
		
	elif "Main Library" in locationTitle:
		room = locationTitle.split("Basement, ")[1]
		if "Room" in room:
			locationOutput = room.split(" [")[0]
		else:
			locationOutput = room.split(" [")[0] +"-" + room.split("Row: ")[1].split(",")[0] + "-" + room.split("Bay: ")[1].split(",")[0] + "-" + room.split("Shelf: ")[1].split("]")[0]
			
	elif "Cold Storage" in locationTitle:
		if "Room" in locationTitle:
			locationOutput = "Cold"
		elif  "Cabinet" in locationTitle:
			locationOutput = "Cold-" + locationTitle.split("Cabinet: ")[1].split(",")[0] + "-" +  locationTitle.split("Drawer: ")[1].split(",")[0] + "-" + locationTitle.split("Section: ")[1].split("]")[0]
		else:
			locationOutput = "Cold-" + locationTitle.split("Bay: ")[1].split(",")[0] + "-" + locationTitle.split("Shelf: ")[1].split("]")[0]
			
	elif "Vault" in locationTitle:
		if "Room" in locationTitle:
			locationOutput = "Vault"
		else:
			locationOutput = "Vault-V-" + locationTitle.split("Row: ")[1].split(",")[0] + "-" +  locationTitle.split("Bay: ")[1].split(",")[0] + "-" + locationTitle.split("Shelf: ")[1].split("]")[0]
			
	elif "Main Storage, L" in locationTitle:
		locationOutput = "L-" + locationTitle.split("Bay: ")[1].split(",")[0] + "-" + locationTitle.split("Bay: ")[1].split(": ")[1].replace("]", "")
		
	else:
		locationOutput =  locationTitle.split("Main Storage, ")[1].split(" [")[0] + "-" + locationTitle.split("Row: ")[1].split(",")[0] + "-" +  locationTitle.split("Bay: ")[1].split(",")[0] + "-" + locationTitle.split("Shelf: ")[1].split("]")[0]	
		
	return locationOutput