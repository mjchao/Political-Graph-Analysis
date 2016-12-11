year=1986
echo $year
for i in `seq 105 113`;
do
		((year=year+1))
        python generate_voting_graph.py $i 171 271
done 