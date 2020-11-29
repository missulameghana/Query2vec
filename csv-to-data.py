import csv
n = 96 #no of RDFs in dataset
operators_dict ={"PIPE":0, "HSJOIN":1,"UNIQUE":2,"FILTER":3,"TBSCAN":4, "TQ":5, "CMPEXP":6, "UNION":7, "GRPBY":8, "RETURN":9, "SORT":10, "TEMP":11, "NLJOIN":12, "IXSCAN":13, "FETCH":14}
fname = 'gSpan/graphdata/graphs-{}.data'.format(n)
with open(fname,'w') as f:
	for i in range(n):
		f.write("t # {}\n".format(i))
		vertices_fname = 'vertices/v{}.csv'.format(i)
		with open(vertices_fname,'r') as v_csv:
			csv_reader = csv.reader(v_csv,delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count==0:
					line_count+=1
				else:
					f.write("v {} {}\n".format(int(row[0].strip(' "')),operators_dict[row[1].strip(' "')]))
					line_count+=1
		print("Graph {} has {} vertices".format(i,line_count-1))
		edges_fname = 'edges/e{}.csv'.format(i)
		with open(edges_fname,'r') as e_csv:
			csv_reader = csv.reader(e_csv,delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count==0:
					line_count+=1
				else:
					leaf_node = row[1]
					if leaf_node.strip(' ')!="":
						f.write("e {} {} {}\n".format(int(row[0].strip(' "')),int(row[1].strip(' "')),int(float(row[2].strip(' "')))))
						line_count+=1
		print("Graph {} has {} edges".format(i,line_count-1))
	f.write("t # -1\n")

	
	
