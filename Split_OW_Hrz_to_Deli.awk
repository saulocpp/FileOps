{
if($1 != "!")
	if(NF == 6)
		HRZ_NAME = $4
	else if(NF == 5)
		printf("%u,%u,%.3f,%.3f,%.3f\n", $1, $2, $3, $4, $5) >> HRZ_NAME".dat"
}
