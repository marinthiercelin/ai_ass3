def get_feature(screen):
	features = ""
	pos = 0
	for i in range(16):
		for j in range(14):
			feature = 128*"0"
			for k in range(10):
				for l in range(15):
					val = screen[pos]
					feature = feature[:val] + "1" +feature[val+1:]
					pos += 1
			features += feature
	return features
			
