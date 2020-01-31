import numpy

terminus = 90
currentAge = 25
retirementAge = 30
startingBalance = 105823.95
annualSpend = 24000
inflation = 1.0225
simulations = 10000
# returnStdev = 0.24907273550480202
# returnAverage = 0.12393469387755104
returnStdev = 0.35
returnAverage = 0.2
contribution = 24000

success = 0
bestCase = 0
worstCase = 0
medianCase = []

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
    
    for j in range(retirementAge - currentAge, terminus - retirementAge):
        spend *= inflation
        portfolio -= spend
        if portfolio <= 0:
            if worstCase == 0 or worstCase > j + 1:
                worstCase = j + 1
                break

        portfolio *= (1 + sample[j])
        if portfolio <= 0:
            if worstCase == 0 or worstCase > j + 1:
                worstCase = j + 1
                break

    medianCase.append(portfolio)
    # print('${:,}'.format(portfolio))
    if portfolio > 0:
        success += 1
        if bestCase == 0 or bestCase < portfolio:
            bestCase = portfolio

bestCase /= (inflation ** (terminus - currentAge))

print('Success Rate: ', success / simulations * 100, '%', sep = '')
print('Inflation-Adjusted Best Case: ${:,}'.format(bestCase))
print('Worst Case:', worstCase, 'years')
print('Inflation-Adjusted Median Case: ${:,}'.format(numpy.median(medianCase) / (inflation ** (terminus - currentAge))))

