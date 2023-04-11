import pigpio

pi = pigpio.pi()
h = pi.spi_open(0,1000000)
c = pi.spi_open(1,1000000)


def findFrequency(find):
    Frequencies =   [10250, 9920, 9640, 9300, 9070, 8800, 8560, 8330, 8120, 7910, 7730, 7520,	
                      7360,	7190, 7030,	6870, 6730,	6580, 6460,	6300, 6200,	6080, 5976,	5850, 5750,	
                      5640,	5550, 5450,	5380, 5280,	5200, 5110,	5030, 4950,	4880, 4810,	4750, 4680,	
                      4620,	4540, 4485,	4410, 4360,	4300, 4270,	4210, 4155,	4100, 4050,	3994, 3950,	
                      3900,	3870, 3820,	3770, 3742,	3695, 3651,	3612, 3570,	3540, 3500,	3460, 3420,	
                      3390,	3355, 3319,	3287, 3261,	3227, 3195,	3160, 3131,	3100, 3071,	3040, 3025,	
                      2995,	2965, 2935,	2919, 2885,	2861, 2831,	2820, 2795,	2770, 2745,	2725, 2700,	
                      2678,	2653, 2640,	2620, 2600,	2580, 2555,	2537, 2517,	2496, 2487,	2470, 2447,	
                      2437,	2415, 2391,	2375, 2357,	2340, 2332,	2312, 2295,	2270, 2240,	2235, 2225,	
                      2225,	2210, 2170,	2163, 2160,	2150, 2136,	2120, 2110,	2100, 2086,	2070, 2059,	
                      2045,	2032, 2020,	2015, 2000,	1989, 1970,	1965, 1950,	1940, 1928,	1922, 1909,	
                      1900,	1887, 1875,	1865, 1855,	1843, 1840,	1828, 1819,	1807, 1799,	1785, 1778,	
                      1765,	1764, 1753,	1749, 1735,	1725, 1715,	1708, 1697,	1693, 1684,	1676, 1666,	
                      1658,	1649, 1641,	1632, 1629,	1619, 1612,	1603, 1595,	1588, 1580,	1570, 1569,	
                      1561,	1554, 1546,	1538, 1530,	1524, 1515,	1512, 1506,	1500, 1491,	1484, 1477,	
                      1470,	1465, 1462,	1456, 1449,	1442, 1436,	1429, 1422,	1415, 1413,	1408, 1402,	
                      1400,	1389, 1382,	1377, 1370,	1369, 1363,	1357, 1351,	1346, 1340,	1333, 1329,	
                      1327,	1322, 1315, 1309, 1304, 1299, 1294, 1286, 1288, 1281, 1276, 1270, 1265,	
                      1261,	1255, 1250, 1249, 1244, 1239, 1234, 1229, 1224, 1219, 1215, 1213, 1208,	
                      1203,	1198, 1194, 1190, 1185]
    
    #intialize frequency and i
    frequency = 11000
    i = -1
    #find when the table frequency is lower than the desired frequency
    while ((frequency > find) and (frequency != 1185)):
        i += 1
        frequency = Frequencies[i]

    #Calculate how far off the two closet frequencies are    
    test1 =(Frequencies[i-1] - find) 
    test2 =(find - Frequencies[i])

    #This inverts the table so the higher frequency corresponds to higher in the table and vice versa
    i = 250 - i
    #Check to find the closer freqeuncy to the desired frequency
    if test1 < test2:
        i = 250 - i - 1
        return i/2
    else:
        return i/2

def sine(frequency, amplitude):
    #Found frequency
    foundfrequency = findFrequency(frequency)

    #Check to see if its a half step
    isHalf = foundfrequency
    isHalf %= 1

    #Check to see if the pots should be different than one another
    if isHalf == .5:
        pot1 = foundfrequency + .5
        pot0 = foundfrequency - .5
    else:
        pot1 = foundfrequency
        pot0 = foundfrequency

    #Write the found digipot values
    pi.spi_write(h, [0b0000_0000, pot0])
    pi.spi_write(h, [0b0001_0000, pot1])
    print(f"Pot1 is {pot1}, pot0 is {pot0}")

