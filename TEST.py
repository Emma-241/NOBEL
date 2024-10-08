import re

data = "imei:864893038636224,tracker,240918111525,,F,111525.00,A,0025.46333,N,00927.60696,E,31.162,106.68;"

# Regex fournie des groupes nommés
pattern = r'imei:(?P<IMEI>[0-9]+),([a-z]+),(?P<DATE>\d{6})\d{6},,(?P<GPS_FIX>[FL]),(?P<TIME>\d{6})\.\d+,(?P<STATUS>[AV]),(\d+\.\d+),(?P<LATITUDE_NS>[NS]),(\d+\.\d+),(?P<LONGITUDE_EW>[ES]),(\d+\.\d+),(\d+\.\d+);'

# Appliquer la regex
match = re.match(pattern, data)
if match:
    resultat = match.groupdict()
    print(resultat)

else :
    print("entrée invalide")

print("End programme!!!")

print("finished")
