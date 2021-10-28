import matplotlib.pyplot as plt 
import numpy as np 
data_file = "data/raw_data.csv"
import csv, os, pickle  
from tqdm import tqdm 
import numpy as np 
from functools import reduce 
from xml.etree import ElementTree as ET
raw_folder = "raw_data"

pattern_string = "participants group_id"

def icdcode_text_2_lst_of_lst(text):
	text = text[2:-2]
	lst_lst = []
	for i in text.split('", "'):
		i = i[1:-1]
		lst_lst.append([j.strip()[1:-1] for j in i.split(',')])
	return lst_lst 

def row2icdcodelst(row):
	icdcode_text = row[6]
	icdcode_lst2 = icdcode_text_2_lst_of_lst(icdcode_text)
	icdcode_lst = reduce(lambda x,y:x+y, icdcode_lst2)
	icdcode_lst = [i.replace('.', '') for i in icdcode_lst]
	return icdcode_lst 

def xmlfile_2_startyear(xml_file):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	try:
		start_date = root.find('start_date').text	
		start_date = int(start_date.split()[-1])
	except:
		start_date = -1
	return start_date

def file2patientnumber(xml_file):
	os.system('grep "' + pattern_string + '" ' + xml_file + ' | head -1 > tmp')
	with open("tmp", 'r') as fin:
		line = fin.readline()
	num = int(line.split('"')[3])
	return num 

if not (os.path.exists("data/nctid2year.pkl") and os.path.exists("data/nctid2patientnumber.pkl")):
	year_lst = []
	nctid2year = dict()
	nctid2patientnumber = dict() 
	with open(data_file) as f:
		reader = list(csv.reader(f))[1:]
		for line in tqdm(reader):
			nctid = line[0]
			file = os.path.join(raw_folder, nctid[:7]+"xxxx/"+nctid+".xml")
			# assert os.path.exists(file)
			start_year = xmlfile_2_startyear(file)
			try:
				patientnumber = file2patientnumber(file)
				nctid2patientnumber[nctid] = patientnumber
				print(patientnumber)
			except:
				pass 
			if start_year != -1:
				year_lst.append(start_year)
				nctid2year[nctid] = start_year 

	data = year_lst 
	data = list(filter(lambda x:x>1998, data))
	pickle.dump(nctid2year, open("data/nctid2year.pkl", 'wb'))
	pickle.dump(nctid2patientnumber, open("data/nctid2patientnumber.pkl", 'wb'))
	fig, ax = plt.subplots()
	num_bins = 23
	n, bins, patches = ax.hist(data, num_bins, )
	plt.tick_params(labelsize=15)
	ax.set_xlabel('Year', fontsize = 20)  
	ax.set_ylabel('Selected trial number', fontsize = 20)  
	plt.tight_layout() 
	# ax.set_title(r'Histogram of trial number in each year') 
	# fig.set_facecolor('cyan')  #
	plt.savefig("histogram.png")
else:
	nctid2year = pickle.load(open("data/nctid2year.pkl", 'rb'))
	nctid2patientnumber = pickle.load(open("data/nctid2patientnumber.pkl", 'rb'))

if not os.path.exists("data/nctid2label.pkl"):
	nctid2label = dict() 
	nctid2drug = dict() 
	nctid2disease = dict() 
	nctid2icd = dict() 
	with open("data/raw_data.csv") as fin:
		readers = list(csv.reader(fin))[1:]
		for row in readers:
			nctid = row[0]
			label = int(row[3])
			nctid2label[nctid] = label
			drug = row[7].strip('"[],')
			drug_lst = drug.strip("'").split("', '")
			print("drug", drug_lst)
			nctid2drug[nctid] = drug_lst
			disease = row[5].strip('"[],')
			disease_lst = disease.strip("'").split("', '")
			print("disease", disease_lst)
			nctid2disease[nctid] = disease_lst 	
			icdcode_lst = row2icdcodelst(row)
			nctid2icd[nctid] = icdcode_lst 

		pickle.dump(nctid2label, open("data/nctid2label.pkl", 'wb'))
		pickle.dump(nctid2drug, open("data/nctid2drug.pkl", 'wb'))
		pickle.dump(nctid2disease, open("data/nctid2disease.pkl", 'wb'))
		pickle.dump(nctid2icd, open("data/nctid2icd.pkl", 'wb'))
else:
	nctid2label = pickle.load(open("data/nctid2label.pkl", 'rb'))
	nctid2drug = pickle.load(open("data/nctid2drug.pkl", 'rb'))
	nctid2disease = pickle.load(open("data/nctid2disease.pkl", 'rb'))
	nctid2icd = pickle.load(open("data/nctid2icd.pkl", 'rb'))

disease_lst = [disease for nctid, disease in nctid2disease.items()]
disease_lst = list(reduce(lambda x,y:x+y, disease_lst))
print("total disease", len(set(disease_lst)))
drug_lst = [drug for nctid, drug in nctid2drug.items()]
drug_lst = list(reduce(lambda x,y:x+y, drug_lst))
print("total drug", len(set(drug_lst)))




data = [year for nctid,year in nctid2year.items()]
target_year_range = [(2000,2004), (2005,2009), (2010,2014), (2015,2020)]
for year1, year2 in target_year_range:
	print(year1, year2)
	selected_nctids = [nctid for nctid,year in nctid2year.items() if year>=year1 and year<=year2]
	positive_sample = len(list(filter(lambda x:x in nctid2label and nctid2label[x]==1, selected_nctids)))
	print("total samples:", len(selected_nctids), "positive sample:", positive_sample, "negative sample", len(selected_nctids)-positive_sample)
	patientnumber_lst = [nctid2patientnumber[nctid] for nctid in selected_nctids if nctid in nctid2patientnumber]
	print("patient number ", np.mean(patientnumber_lst))
	disease_set, drug_set = set(), set() 
	for nctid in selected_nctids:
		disease_lst = nctid2disease[nctid] if nctid in nctid2disease else []
		disease_set = disease_set.union(set(disease_lst))
		drug_lst = nctid2drug[nctid] if nctid in nctid2drug else []
		drug_set = drug_set.union(set(drug_lst))
	print("disease ", len(disease_set))
	print("drug", len(drug_set))


print("# trials", len(selected_nctids))


print('########### neoplasm ############')
selected_nctids = [nctid for nctid,disease in nctid2disease.items() \
						if 'neoplasm' in ' '.join(disease).lower() or \
						'tumor' in ' '.join(disease).lower() or \
						'cancer' in ' '.join(disease).lower()]
positive_sample = len(list(filter(lambda x:x in nctid2label and nctid2label[x]==1, selected_nctids)))
print("total samples:", len(selected_nctids), "positive sample:", positive_sample, "negative sample", len(selected_nctids)-positive_sample)
patientnumber_lst = [nctid2patientnumber[nctid] for nctid in selected_nctids if nctid in nctid2patientnumber]
print("patient number ", np.mean(patientnumber_lst))
disease_set, drug_set = set(), set()  
for nctid in selected_nctids:
	disease_lst = nctid2disease[nctid] if nctid in nctid2disease else []
	disease_set = disease_set.union(set(disease_lst))
	drug_lst = nctid2drug[nctid] if nctid in nctid2drug else []
	drug_set = drug_set.union(set(drug_lst))
print("disease ", len(disease_set))
print("drug", len(drug_set))


from ccs_utils import file2_icd2ccs_and_ccs2description, file2_icd2ccsr
# icd2ccs, ccscode2description = file2_icd2ccs_and_ccs2description() 
icd2ccsr = file2_icd2ccsr()


print('########### respiratory ############')
selected_nctids = []
for nctid, icdcode_lst in nctid2icd.items():
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'RSP':
				selected_nctids.append(nctid)
				break 
		except:
			pass 
positive_sample = len(list(filter(lambda x:x in nctid2label and nctid2label[x]==1, selected_nctids)))
print("total samples:", len(selected_nctids), "positive sample:", positive_sample, "negative sample", len(selected_nctids)-positive_sample)
patientnumber_lst = [nctid2patientnumber[nctid] for nctid in selected_nctids if nctid in nctid2patientnumber]
print("patient number ", np.mean(patientnumber_lst))
disease_set, drug_set = set(), set()  
for nctid in selected_nctids:
	disease_lst = nctid2disease[nctid] if nctid in nctid2disease else []
	disease_set = disease_set.union(set(disease_lst))
	drug_lst = nctid2drug[nctid] if nctid in nctid2drug else []
	drug_set = drug_set.union(set(drug_lst))
print("disease ", len(disease_set))
print("drug", len(drug_set)) 












print('########### digestive ############')
selected_nctids = []
for nctid, icdcode_lst in nctid2icd.items():
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'DIG':
				selected_nctids.append(nctid)
				break 
		except:
			pass 
positive_sample = len(list(filter(lambda x:x in nctid2label and nctid2label[x]==1, selected_nctids)))
print("total samples:", len(selected_nctids), "positive sample:", positive_sample, "negative sample", len(selected_nctids)-positive_sample)
patientnumber_lst = [nctid2patientnumber[nctid] for nctid in selected_nctids if nctid in nctid2patientnumber]
print("patient number ", np.mean(patientnumber_lst))
disease_set, drug_set = set(), set()  
for nctid in selected_nctids:
	disease_lst = nctid2disease[nctid] if nctid in nctid2disease else []
	disease_set = disease_set.union(set(disease_lst))
	drug_lst = nctid2drug[nctid] if nctid in nctid2drug else []
	drug_set = drug_set.union(set(drug_lst))
print("disease ", len(disease_set))
print("drug", len(drug_set)) 














print('########### nervous ############')
selected_nctids = []
for nctid, icdcode_lst in nctid2icd.items():
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'NVS':
				selected_nctids.append(nctid)
				break 
		except:
			pass 
positive_sample = len(list(filter(lambda x:x in nctid2label and nctid2label[x]==1, selected_nctids)))
print("total samples:", len(selected_nctids), "positive sample:", positive_sample, "negative sample", len(selected_nctids)-positive_sample)
patientnumber_lst = [nctid2patientnumber[nctid] for nctid in selected_nctids if nctid in nctid2patientnumber]
print("patient number ", np.mean(patientnumber_lst))
disease_set, drug_set = set(), set()  
for nctid in selected_nctids:
	disease_lst = nctid2disease[nctid] if nctid in nctid2disease else []
	disease_set = disease_set.union(set(disease_lst))
	drug_lst = nctid2drug[nctid] if nctid in nctid2drug else []
	drug_set = drug_set.union(set(drug_lst))
print("disease ", len(disease_set))
print("drug", len(drug_set)) 












