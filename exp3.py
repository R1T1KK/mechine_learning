import itertools
import matplotlib.pyplot as plt

# ---------------------------------
# TRANSACTIONS
# ---------------------------------
transactions = [
    ["Milk", "Eggs", "Jam"],
    ["Juice", "Milk"],
    ["Eggs", "Bread", "Milk"],
    ["Bread", "Butter", "Milk", "Eggs"],
    ["Jam", "Eggs"]
]

total_transactions = len(transactions)

# ---------------------------------
# THRESHOLDS
# ---------------------------------
min_support_percent = 0.40      # 40%
min_confidence = 0.70           # 70%
min_support_count = min_support_percent * total_transactions

# ---------------------------------
# 1-FREQUENT ITEMSET
# ---------------------------------
item_count = {}
for t in transactions:
    for item in t:
        item_count[item] = item_count.get(item, 0) + 1

print("1-Frequent Itemset (Support Count)")
freq1 = {}
for item, count in item_count.items():
    if count >= min_support_count:
        freq1[item] = count
        print(f"{item} : {count}")

# ---------------------------------
# 2-FREQUENT ITEMSET
# ---------------------------------
pair_count = {}
for t in transactions:
    for pair in itertools.combinations(sorted(t), 2):
        pair_count[pair] = pair_count.get(pair, 0) + 1

print("\n2-Frequent Itemset (Support Count)")
freq2 = {}
for pair, count in pair_count.items():
    if count >= min_support_count:
        freq2[pair] = count
        print(f"{pair} : {count}/{total_transactions}")

# ---------------------------------
# 3-FREQUENT ITEMSET
# ---------------------------------
triple_count = {}
for t in transactions:
    for triple in itertools.combinations(sorted(t), 3):
        triple_count[triple] = triple_count.get(triple, 0) + 1

print("\n3-Frequent Itemset (Support Count)")
freq3 = {}
for triple, count in triple_count.items():
    if count >= min_support_count:
        freq3[triple] = count
        print(f"{triple} : {count}/{total_transactions}")

# ---------------------------------
# ASSOCIATION RULES (with counts / total transactions)
# ---------------------------------
print("\nAssociation Rules (Confidence ≥ 70%)")

rule_names = []
conf_values = []

# ---- Rules from 2-Frequent Itemsets ----
for (a, b), sup_ab in freq2.items():
    sup_x = item_count[a]
    sup_y = item_count[b]

    conf_ab = sup_ab / sup_x
    conf_ba = sup_ab / sup_y

    status_ab = "✓" if conf_ab >= min_confidence else "✗"
    status_ba = "✓" if conf_ba >= min_confidence else "✗"

    # Print numerator as sup(X∪Y) / total transactions
    print(f"{a} → {b} = {sup_ab}/{total_transactions} = {round(conf_ab*100)}% {status_ab}")
    print(f"{b} → {a} = {sup_ab}/{total_transactions} = {round(conf_ba*100)}% {status_ba}\n")

    rule_names.append(f"{a} → {b}")
    conf_values.append(conf_ab*100)
    rule_names.append(f"{b} → {a}")
    conf_values.append(conf_ba*100)

# ---- Rules from 3-Frequent Itemsets ----
for (a, b, c), sup_abc in freq3.items():
    # {a,b} -> c
    if (a, b) in freq2:
        conf = sup_abc / freq2[(a, b)]
        status = "✓" if conf >= min_confidence else "✗"
        print(f"{a}, {b} → {c} = {sup_abc}/{total_transactions} = {round(conf*100)}% {status}")
        rule_names.append(f"{a}, {b} → {c}")
        conf_values.append(conf*100)

    # {a,c} -> b
    if (a, c) in freq2:
        conf = sup_abc / freq2[(a, c)]
        status = "✓" if conf >= min_confidence else "✗"
        print(f"{a}, {c} → {b} = {sup_abc}/{total_transactions} = {round(conf*100)}% {status}")
        rule_names.append(f"{a}, {c} → {b}")
        conf_values.append(conf*100)

    # {b,c} -> a
    if (b, c) in freq2:
        conf = sup_abc / freq2[(b, c)]
        status = "✓" if conf >= min_confidence else "✗"
        print(f"{b}, {c} → {a} = {sup_abc}/{total_transactions} = {round(conf*100)}% {status}")
        rule_names.append(f"{b}, {c} → {a}")
        conf_values.append(conf*100)

# ---------------------------------
# VISUALIZATION
# ---------------------------------
colors = ["green" if c >= 70 else "orange" for c in conf_values]

plt.figure(figsize=(12, 6))
plt.bar(rule_names, conf_values, color=colors)
plt.axhline(y=70, linestyle='--', label='Min Confidence (70%)')
plt.xlabel("Association Rules")
plt.ylabel("Confidence (%)")
plt.title("Association Rule Confidence (Min Support = 40%)")
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()
