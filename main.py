import numpy

terminus = 90
currentAge = 24
retirementAge = 35
startingBalance = 100000
annualSpend = 24000
inflation = 1.0225
simulations = 1000
returnStdev = 0.24907273550480202
returnAverage = 0.12393469387755104
contribution = 40000

success = 0
bestCase = 0
worstCase = 0

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

    # print('${:,}'.format(portfolio))
    if portfolio > 0:
        success += 1
        if bestCase == 0 or bestCase < portfolio:
            bestCase = portfolio

print('Success Rate: ', success / simulations * 100, '%', sep = '')
print('Best Case: ${:,}'.format(bestCase))
print('Worst Case:', worstCase, 'years')