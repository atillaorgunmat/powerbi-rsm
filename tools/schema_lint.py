# tools/schema_lint.py   (keep under your repo)
import sys, csv, json, pathlib

SPEC = {
    'pos': ['OrderID','ProductSKU','Qty','UnitPrice','LineTotal','OrderDate','StoreCode'],
    'wms': ['StoreCode','ProductSKU','QtyOnHand','SnapshotDate'],
    'oms': ['OrderID','Status','CreatedDate'],
    'mkt': ['CampaignID','SpendAmount','SpendDate','Channel']
}

def check_csv(path, cols):
    with open(path, newline='') as f: header = next(csv.reader(f))
    return header == cols

def check_json(path, cols):
    with open(path) as f: obj = json.load(f)[0]
    return all(c in obj for c in cols)

src, fp = sys.argv[1], pathlib.Path(sys.argv[2])
ok = (check_csv if fp.suffix=='.csv' else check_json)(fp, SPEC[src])
print("OK" if ok else "FAIL"); sys.exit(0 if ok else 2)
