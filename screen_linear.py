def get_feature(screen):
	features = []
	string = ""
	for i in range(12):
		for j in range(16):
			feature = []
			pos1 = 160*15*i + j*10
			for k in range(10):
				pos2 = 160*k
				for l in range(10):
					val = screen[pos1 + pos2 + l]
					if val not in feature and val != 74 and val != 144 and val != 0:
						feature.append(val)
						string += str(val) + ","
			string += "/"
			features.append(feature)
	return (features,hash(string))
			
