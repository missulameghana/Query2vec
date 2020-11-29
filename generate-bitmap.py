import networkx as nx
from networkx.algorithms import isomorphism
import sys
import csv
import matplotlib.pyplot as plt
operators_list =["PIPE", "HSJOIN","UNIQUE","FILTER","TBSCAN", "TQ", "CMPEXP", "UNION", "GRPBY", "RETURN", "SORT", "TEMP", "NLJOIN", "IXSCAN", "FETCH"]
thresholds = [10,50]
for thresh in thresholds:
	patterns_file =  "patterns.96.{}.txt".format(thresh) #expected in txt format
	n_patterns = 0 # no of patterns to be read from patterns file redirected from gSpan's output
	patterns_graphs =[]
	patterns_freq = []
	bitmap = []
	with open(patterns_file,'r') as f:
		line = f.readline()
		G = nx.DiGraph()
		while not line.startswith("Read:"):		
			if line.startswith("t #"):
				n_patterns += 1
			elif line.startswith("v "):
				vl = line.split()
				G.add_node(vl[1],type=operators_list[int(vl[2])])
			elif line.startswith("e "):
				el = line.split()
				G.add_edge(el[1],el[2], weight=int(el[3]))
			elif line.startswith("Support:"):
				sl = line.split()
				patterns_freq.append(sl[1])
			elif line.startswith("-----------------"):
				patterns_graphs.append(G)
				pos = nx.spring_layout(G)
				color_map = []
				for node in G:
					color_map.append('white')
				nx.draw(G, pos,node_color=color_map)
				node_labels = nx.get_node_attributes(G,'type')
				nx.draw_networkx_labels(G, pos, labels = node_labels)
				edge_labels = nx.get_edge_attributes(G,'weight')
				nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
				plt.savefig("visualized_patterns/pattern{}.96.{}.png".format(n_patterns,thresh))
				plt.clf()
				print("printing {} for threshold value of {}".format(n_patterns,thresh))
				G.clear()
			line = f.readline()
	for i in range(96):
		vertices_file = "vertices/v{}.csv".format(i) #expected in csv format
		edges_file = "edges/e{}.csv".format(i) #expected in csv format
		
		input_G = nx.DiGraph()
		with open(vertices_file,'r') as vf:
			csv_reader = csv.reader(vf,delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count==0:
					line_count+=1
				else:
					input_G.add_node(int(row[0].strip(' "')), type=int(operators_dict[row[1].strip(' "')]))
					line_count+=1
		with open(edges_file,'r') as ef:
			csv_reader = csv.reader(ef,delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count==0:
					line_count+=1
				else:
					leaf_node = row[1]
					if leaf_node.strip(' ')!="":
						input_G.add_edge(int(row[0].strip(' "')), int(row[1].strip(' "')), weight=int(float(row[2].strip(' "'))))
						line_count+=1
		
		for g in patterns_graphs:
			nm = isomorphism.numerical_node_match('type',0)
			em = isomorphism.numerical_edge_match('weight',1)
			GM = isomorphism.GraphMatcher(input_G,g,node_match=nm,edge_match=em)	
			if GM.subgraph_is_isomorphic():
				bitmap.append(1)
			else:
				bitmap.append(0)
		with open('bitmaps.96.{}.csv'.format(thresh), 'a', newline='') as fil:
			writer = csv.writer(fil)
			writer.writerow(bitmap)



