import pandas as pd

df = pd.read_csv("raw_data.csv")
print("Before cleaning:", len(df))

# Split the details text into separate columns
parts = df["details"].str.split(r"\s\|\s", expand=True).reindex(columns=range(4))
df["location"] = parts[1]
df["opened"] = pd.to_numeric(parts[2], errors="coerce")
df["area_sqft"] = pd.to_numeric(
    parts[3].str.extract(r"^([\d,]+)")[0].str.replace(",", "", regex=False),
    errors="coerce")

# Clean the names
df["name"] = df["name"].str.replace(r"\[\d+\]", "", regex=True)
df["name"] = df["name"].str.split(r"\s[-–—]\s|,", n=1, regex=True).str[0]
df["name"] = df["name"].str.strip()
df = df.dropna(subset=["name"])
df = df[df["name"].str.len() > 3]
df = df[~df["name"].str.lower().isin(["nan", "none"])]

# Remove duplicates, keeping the row with the fullest address
df["address_len"] = df["location"].fillna("").str.len()
df = df.sort_values("address_len", ascending=False).drop_duplicates(subset="name", keep="first")

df = df[["name", "location", "opened", "area_sqft"]].sort_values("name")
df.to_csv("clean_data.csv", index=False)
print("After cleaning:", len(df))