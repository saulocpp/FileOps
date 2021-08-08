{
if($1 == "TDP2")
	WELL_NAME = $2
else if($1 == "TDP3")
	TD_TABLE = $2
else if($1 == "TDP5")
	printf("%12s  %12s\n", $2, $3) >> WELL_NAME"_"TD_TABLE".txt"
}

