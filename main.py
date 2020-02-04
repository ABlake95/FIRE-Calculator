import numpy

terminus = 90
currentAge = 25
retirementAge = 54
startingBalance = 137069.23
annualSpend = 34000
inflation = 1.032430142824996
simulations = 10000
returnStdev = 0.24907273550480202
# returnAverage = 0.12393469387755104
# returnStdev = 0.35
returnAverage = 0.2
contribution = 20000

success = 0
bestCase = 0
worstCase = 0
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
            if worstCase == 0 or worstCase > j + 1:
                worstCase = j + 1
                break

        portfolio *= (1 + sample[j])
        if portfolio <= 0:
            if worstCase == 0 or worstCase > j + 1:
                worstCase = j + 1
                break

    medianCase.append(portfolio)
    if portfolio > 0:
        success += 1
        if bestCase == 0 or bestCase < portfolio:
            bestCase = portfolio

bestCase /= (inflation ** (terminus - currentAge))

print('Success Rate: ', success / simulations * 100, '%', sep = '')
print('Worst Case:', worstCase, 'years')
print('Inflation-Adjusted Retirement Start Median Case: ${:,}'.format(numpy.median(retirementStartBalance) / (inflation ** (retirementAge - currentAge))))
print('Inflation-Adjusted Terminus Median Case: ${:,}'.format(numpy.median(medianCase) / (inflation ** (terminus - currentAge))))
print('Inflation-Adjusted Terminus Best Case: ${:,}'.format(bestCase))
