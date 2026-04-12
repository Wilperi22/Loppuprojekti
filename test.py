from datetime import datetime
d1 = datetime.strptime("20-03-2026","%d-%m-%Y")
d2 = datetime.strptime("20-04-2026","%d-%m-%Y")

testi = d1 -d2
print(testi)
