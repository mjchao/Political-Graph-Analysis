import graph

print("Starting.")

nodes_by_year = []
edges_by_year = []
for i in range(10):
	nodes_by_year.append({})
	edges_by_year.append([])

f = open("contributions.csv",'r')
for line in f:
	line = line.split(",")
	if float(line[11]) >= 24000:
		year = int(line[2])/2 - 999
		nodes_by_year[year][line[0]] = True
		nodes_by_year[year][line[4]] = False
		edges_by_year[year].append([float(line[11]),line[0],line[4]])


f.close()
print("Data read.")
years = [1998,2000,2002,2004,2006,2008,2010,2012,2014,2016]

for i in range(len(years)):
	f = open("simrank_contributions_results_" + str(years[i]) + ".csv",'w')
	nodes_list = []
	for key, value in nodes_by_year[i].iteritems():
		nodes_list.append(key)

	contribution_graph = graph.SimrankGraph(nodes_list)
	for edge in edges_by_year[i]:
		contribution_graph.SetEdge(edge[2],edge[1],edge[0],directed=False)

	print("Graph made for year " + str(years[i]))

	contribution_graph.Run(r=(5*12000.0))

	print("Simrank run for year " + str(years[i]))

	politicians = []
	companies = []
	for key, value in nodes_by_year[i].iteritems():
		if value:
			politicians.append(key)
		else:
			companies.append(key)
	lenp = len(politicians)
	for j in range(lenp):
		for k in range((j+1),lenp):
			f.write(str(politicians[j]) + "," + str(politicians[k]) + "," + str(contribution_graph.Similarity(politicians[j],politicians[k])) + ",Policians\n")
	lenp = len(companies)
	for j in range(lenp):
		for k in range((j+1),lenp):
			f.write(str(companies[j]) + "," + str(companies[k]) + "," + str(contribution_graph.Similarity(companies[j],companies[k])) + ",Companies\n")

	print("Wrote to file for year " + str(years[i]))
	f.close()

