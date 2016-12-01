year=1986
echo $year
for i in `seq 100 113`;
do
		((year=year+1))
        python voting_simrank.py $i
done 