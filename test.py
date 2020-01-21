import pandas
import numpy

df = pandas.read_csv('data.csv')

print(numpy.std(df['return']))
print(numpy.mean(df['return']))