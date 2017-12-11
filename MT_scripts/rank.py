import pandas as pd
import sys

gen = sys.argv[1]
# else:
csv = "data/rank%s.csv" % gen
csv2 = "data/find%s.csv" % gen

rank = pd.read_csv(csv, index_col=False)
rank.sort_values('trial')

find = pd.read_csv(csv2, index_col=False)

ranks = ['rank%i' % i for i in range(10)]
crosstab = pd.melt(rank, ['rank_id', 'trial'], ranks)
crosstab['rank'] = crosstab['variable'].apply(lambda x: ranks.index(x))
grouped = crosstab.groupby(['trial', 'value'])['rank'].mean()
grouped = grouped.reset_index()

for trial in grouped.trial.unique():
    print "\nBEST FOR TRIAL %i: " % trial,
    best_id = grouped[grouped.trial == trial].sort_values('rank')['value'].iloc[0]
    runner_up = grouped[grouped.trial == trial].sort_values('rank')['value'].iloc[1]
    print best_id, "(runner-up is", runner_up, ")"

    if best_id == 9999:
        print "**",find[find.trial == trial].original.iloc[0]
    else:
        print "**",find[find.find_id == best_id].updated.iloc[0]

    if runner_up == 9999:
        print "*",find[find.trial == trial].original.iloc[0]
    else:
        print "*",find[find.find_id == runner_up].updated.iloc[0]
