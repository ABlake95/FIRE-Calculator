import numpy

simulations = 10000
terminus = 90
currentAge = 25
retirementAge = 75
startingBalance = 140000
inflation = 1.032430142824996
annualSpend = 400000
contribution = 45000

returnAverage = 0.2
returnStdev = 0.3

# NASDAQ Metrics
# returnAverage = 0.12393469387755104
# returnStdev = 0.24907273550480202

success = 0
worstCase = None
medianCase = []
retirementStartBalance = []

for i in range(simulations):
    sample = numpy.random.normal(returnAverage, returnStdev, terminus - currentAge)
    portfolio = startingBalance
    spend = annualSpend
    addition = contribution

    for j in range(retirementAge - currentAge):
        portfolio += addition
        addition *= inflation
        spend *= inflation
        portfolio *= (1 + sample[j])

    retirementStartBalance.append(portfolio)
    
    for j in range(retirementAge - currentAge, terminus - retirementAge):
        spend *= inflation
        portfolio -= spend
        if portfolio <= 0:
            if worstCase == None or worstCase > j + 1:
                worstCase = j + 1
                break

        portfolio *= (1 + sample[j])
        if portfolio <= 0:
            if worstCase == None or worstCase > j + 1:
                worstCase = j + 1
                break

    medianCase.append(portfolio)
    if portfolio > 0:
        success += 1
    else:
    	if worstCase == None or worstCase > terminus - retirementAge:
    		worstCase = terminus - retirementAge

print('Success Rate: ', success / simulations * 100, '%', sep = '')
if worstCase:
	print('Worst Case Return to Work at:', worstCase + retirementAge)
else:
	print('No Worst Case after 10,000 simulations')

print()
print('Inflation-Adjusted Retirement Start Median Case: ${:,}'.format(numpy.median(retirementStartBalance) / (inflation ** (retirementAge - currentAge))))
print('Terminus Median Case (NOT ADJUSTED FOR INFLATION): ${:,}'.format(numpy.median(medianCase)))
print()