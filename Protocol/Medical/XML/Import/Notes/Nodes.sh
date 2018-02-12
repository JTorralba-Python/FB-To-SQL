echo "du" | xmllint --shell Sample.xml > Temp.txt
sort Temp.txt | uniq > Nodes.txt
rm Temp.txt
