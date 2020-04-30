import copy
import numpy

def main():
    simulations = 10000
    terminus = 90
    currentAge = 25
    retirementAge = 75
    startingBalance = 140000
    inflation = (1552 / 1399) ** (1 / 2.75)
    annualSpend = 1000000
    contribution = 42000

    returnAverage = 0.2
    returnStdev = 0.3

    # NASDAQ Metrics
    # returnAverage = 0.12393469387755104
    # returnStdev = 0.24907273550480202

    success = 0
    successSW = 0
    worstCase = None
    worstCaseSW = None
    medianCase = []
    retirementStartBalance = []
    safeWithdrawlRate = []

    for i in range(simulations):
        sample = numpy.random.normal(returnAverage, returnStdev, terminus - currentAge)
        portfolio = startingBalance
        addition = contribution

        for j in range(retirementAge - currentAge):
            portfolio += addition
            addition *= inflation
            annualSpend *= inflation
            portfolio *= (1 + sample[j])

        retirementStartBalance.append(portfolio)

        portfolioSW = copy.deepcopy(portfolio)
        for j in range(retirementAge - currentAge, terminus - retirementAge):
            portfolioSW *= 0.99
            if portfolioSW <= 0:
                if worstCaseSW == None or worstCaseSW > j + 1:
                    worstCaseSW = j + 1
                    break

            portfolioSW *= (1 + sample[j])
            if portfolioSW <= 0:
                if worstCaseSW == None or worstCaseSW > j + 1:
                    worstCaseSW = j + 1
                    break
        safeWithdrawlRate.append(portfolioSW)
        if portfolioSW > 0:
            successSW += 1
        else:
            if worstCaseSW == None or worstCaseSW > terminus - retirementAge:
                worstCaseSW = terminus - retirementAge

        '''
        if portfolioSW == portfolio:
            print("Error")
            return
        else:
            print("Success")
        '''
        
        for j in range(retirementAge - currentAge, terminus - retirementAge):
            annualSpend *= inflation
            portfolio -= annualSpend
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

    print('Success Rate (Annual Spend): ', success / simulations * 100, '%', sep = '')
    if worstCase:
        print('Worst Case Return to Work at (Annual Spend):', worstCase + retirementAge)
    else:
        print('No Worst Case after 10,000 simulations (Annual Spend)')
    print()

    '''
    print('Success Rate (1% Withdrawl): ', successSW / simulations * 100, '%', sep = '')
    if worstCaseSW:
        print('Worst Case Return to Work at (1% Withdrawl):', worstCaseSW + retirementAge)
    else:
        print('No Worst Case after 10,000 simulations (1% Withdrawl)')
    print()
    '''

    print('Inflation-Adjusted Retirement 1% Withdrawl Amount: ${:,}'.format(0.01 * numpy.median(retirementStartBalance) / (inflation ** (retirementAge - currentAge))))
    print('Inflation-Adjusted Retirement Start Median Case: ${:,}'.format(numpy.median(retirementStartBalance) / (inflation ** (retirementAge - currentAge))))
    print()
    print('Terminus Median Case Annual Spend (NOT ADJUSTED FOR INFLATION): ${:,}'.format(numpy.median(medianCase)))
    # print('Terminus Median Case 1% Withdrawl (NOT ADJUSTED FOR INFLATION): ${:,}'.format(numpy.median(safeWithdrawlRate)))

if __name__ == '__main__':
    main()