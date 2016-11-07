def get_feature(screen):
	features = ""
	for i in range(16):
		for j in range(14):
			feature = []
			pos1 = 210*10*i + j*15
			for k in range(10):
				pos2 = 210*k
				for l in range(15):
					val = screen[pos1 + pos2 + l]
					if val is not in feature:
						feature.append(val)
						features += str(val)+","
			features += "/"
	return features
			
