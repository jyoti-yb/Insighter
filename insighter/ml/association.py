### Step 4: ml/association.py

from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

def find_patterns(action_lists):
    te = TransactionEncoder()
    te_ary = te.fit(action_lists).transform(action_lists)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    freq = apriori(df, min_support=0.2, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=0.6)
    return rules[['antecedents', 'consequents', 'support', 'confidence']]
