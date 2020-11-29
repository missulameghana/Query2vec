import csv
with open('bitmaps.96.50.csv','r') as f:
	r = csv.reader(f)	
	with open('bitmaps.96.50.2.csv','w') as f1:
		w = csv.writer(f1)
		i = 1
		for item in r:
			item.insert(0,"tpcds-{}".format(i))
			i+=1
			w.writerow(item)
