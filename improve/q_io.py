def mapToTxt(hMap, filepath):
	f = open(filepath, 'w')
	for elem in hMap.keys():
		toWrite = str(elem) + " " + str(hMap[elem]) + "\n"
		f.write(toWrite)
	f.close(); 
	
def listToTxt(w_list, filepath):
	f = open(filepath, 'w')
	for elem in w_list:
		toWrite = str(elem)+"\n"
		f.write(toWrite)
	f.close();

	
'''def txtToMap(filepath): 
	newMap = {}
	f = open(filepath)
	while True:
		string = f.readline(); 
		if not string: break
		tmp = stringSplitter(string)
		newMap[tmp[0]] = float(tmp[1]); 
	f.close()
	return newMap;'''

def txtToMap(filepath): 
	newMap = {}
	f = open(filepath,'r')
	for string in f:
		tmp = string.split()
		if len(tmp) == 10:
			newMap[tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3] +" " +  tmp[4] +" " +  tmp[5] +" "+  tmp[6] +" "+ tmp[7] +" "+ tmp[8]  ] = float(tmp[9]) 
	f.close()
	return newMap;

def save_average(filepath ,number, average):
	f = open(filepath, 'a')
	toWrite = "number of play : " + str(number) + " average : " + str(average) + "\n"
	f.write(toWrite)
	f.close()
	
	

def txtToList(filepath): 
	w_list = []
	f = open(filepath)
	for string in f:
		w_list.append(float(string))
	f.close()
	return w_list; 

def stringSplitter(string): 
	i = string.find(' '); 
	head = string[:i]
	rest = string[i+1: len(string)-1] # getting rid of the \n's
	return (head, rest)
