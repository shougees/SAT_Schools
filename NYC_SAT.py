import pandas as pd
import re

# read csv data and assign to data dictionary
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
data = {}

for f in data_files:
    d = pd.read_csv("schools/{0}".format(f))
    key_name = f.replace(".csv", "")
    data[key_name] = d


# Display the first 5 rows of the SAT scores data
print(data["sat_results"].head(5))

for d in data:
    print(data[d].head(5))

# Read survey files
all_survey = pd.read_csv("schools/survey_all.txt", delimiter="\t", encoding="windows-1252")
d75_survey = pd.read_csv("schools/survey_d75.txt", delimiter="\t", encoding="windows-1252")
survey = pd.concat([all_survey, d75_survey], axis=0)

print(survey.head())

# Keep only necessary data
survey["DBN"] = survey["dbn"]
columns_to_keep = ["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11",]
survey = survey.loc[:,columns_to_keep]

data["survey"] = survey

print(survey.head())

# Create DBN column
data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

def generate_csd(number):
    number = str(number)
    if len(number) == 2:
        return number
    elif len(number) == 1:
        number = number.zfill(2)
        return number

data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(generate_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]
print(data["class_size"].head())

# Combine SAT scores
columns = ["SAT Math Avg. Score", "SAT Critical Reading Avg. Score", "SAT Writing Avg. Score"]

for c in columns:
    data["sat_results"][c] = pd.to_numeric(data["sat_results"][c], errors="coerce")

data["sat_results"]["sat_score"] = data["sat_results"][columns[0]] + data["sat_results"][columns[1]] + data["sat_results"][columns[2]]
print(data["sat_results"]["sat_score"].head())

# Obtain just the latitude data
def extract_latitude(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lat = coords[0].split(",")[0].replace("(", "")
    return lat

data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(extract_latitude)
print(data["hs_directory"].head())

# Obtain longitude data and convert latitude and longitude data into numeric
def extract_longtitude(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon

data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(extract_longtitude)
data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors="coerce")
print(data["hs_directory"].head())
