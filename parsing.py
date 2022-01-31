import json
import csv
import pandas as pd
import numpy as np
import itertools
import os
from univariate_plots import *
from bivariate_plots import *
from Misc_plots import *
import json
import csv

def get_dtype_groups(data_types):
    float_unis=[]
    object_unis=[]
    int_unis=[]
    for i,v in data_types.items():
        if i == np.dtype('float64') or i == np.dtype('float32'):
            float_unis.append(v)
        if i == np.dtype('O'):
            object_unis.append(v)
        if i == np.dtype('int64') or i==np.dtype('int32') or i==np.dtype('int16'):
            int_unis.append(v)

    return float_unis,object_unis,int_unis

def findsubsets(s, n):
    
    return list(itertools.permutations(s, n))

def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
        
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)   

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parser(filepath,has_headers):
    d=0
    ext=''
    ext_opt1=''
    ext_opt2=''

    extension_file=(filepath.split('/')[-1].split('.')[1]).lower()
    # extension_magic=(magic.from_file(filepath)).lower()



    # if extension_file in extension_magic:
    #     ext=extension_file

    # else:
    #     ext_opt1=extension_file
    #     ext_opt2=extension_magic

    ext = extension_file

    if ext=='':
        ext=ext_opt1

    if ext=='csv' or ext=='xlsx':

        try:
            if ext=='csv':
                df=pd.read_csv(filepath)
            elif ext=='xlsx':
                df= pd.read_excel(filepath)
            df=df.dropna()
            try:
                sample_bytes=1024
                sniffer = csv.Sniffer()
                header = sniffer.has_header(open(filepath).read(sample_bytes))

            except:
                first_=df.columns
                h=0
                for k in first_:

                    if RepresentsInt(k):
                        h+=1
                if h>int(len(first_)/3):
                    header=None
    
                else:
                    header=True


            if header:

                head=df.columns
                cols = [c for c in head if 'unnamed' not in c.lower()]
                df=df[cols]
                head=cols
            else:
                n=len(df.columns)
                df.columns=[str(i) for i in range(n)]
                head=df.columns
                
                cols = [c for c in head if 'unnamed' not in c.lower()]
                df=df[cols]
                print(df)
                head=cols    
        except:
            df=None
            d=1
            head=None




    elif ext=='json':
        try:
            with open(filepath, encoding='utf-8') as f:
                data = json.loads(f.read())

            try:
                df = pd.json_normalize(data, sep='_')
                if has_headers:
                    head=df.columns
                    cols = [c for c in head if 'unnamed' not in c.lower()]
                    df=df[cols]
                    head=cols
                    
            except Exception as e:
                print(e)
                head=None
                df=None
                d=1
                
        except Exception as e:
            print(e)
            head=None
            df=None
            d=1
        


  #  elif ext=='xlsx':
   #     df= pd.read_excel(filepath)
   #     head=df.columns


    elif ext=='npy' or ext=='npz':
        try:
            df=np.load(filepath)
            if len(df.shape)==3 and 1 in df.shape:
                n=df.shape[0]
                r=df.shape[1]
                c=df.shape[2]
                if n==1:
                    df=df.reshape(r,c)
                elif r==1:
                    df=df.reshape(n,c)
                elif c==1:
                    df=df.reshape(n,r)
            
            
            df = pd.DataFrame(df)
            head=None
        except:
            df=None
            d=1
            head=None



    elif ext=='txt':
        try:

            try:

                with open(filepath, 'r') as f1:
                    dialect = csv.Sniffer().sniff(f1.read(1024)) #### detect delimiters
                    deli=dialect.delimiter
            except:
                deli='\t'

            remove_empty_lines(filepath)

            with open(filepath) as f:
                for i in f:
                    first=i
                    break

            if ',' not in first:
                first_=first.split()
            
            elif ',' in first:
                first_=first.split(',')

            file1 = open(filepath, 'r')
            Lines = file1.readlines()
        

            h=0
            for k in first_:
                if RepresentsInt(k):
                    h+=1
            if h>int(len(first_)/3):
                header=None

                
                cols=[str(i) for i in range(len(first_))]
        
                df = pd.DataFrame(columns=cols)
                for idx,line in enumerate(Lines):
                    
                    df.loc[idx] = line.split()
                df= df[(df !='NA').all(1)]
                head=df.columns
                for i in list(head):
                    vals=df[i].tolist()
                    int_,fl=0,0
                    for j in range(10):
                    
                        if '.' in vals[j]:
                            fl+=1
                        elif RepresentsInt(vals[j]):
                    
                            int_+=1
                
                    if int_>7:
                        convert_dict={i:int}
                        df=df.astype(convert_dict)
                        
                    if fl >7:
                        convert_dict={i:float}
                        df=df.astype(convert_dict)

            else:
                df = pd.DataFrame(columns=first_)
                #print(len(Lines))
                for idx,line in enumerate(Lines):
                
                    df.loc[idx] = line.split()
                    

                
                head=df.columns
                if list(head)==list(df.iloc[0]):
                    df=df.drop(0)
                df= df.dropna()
                df= df[(df !='NA').all(1)]
                df= df[(df !='Na').all(1)]
                df= df[(df !='na').all(1)]
                for i in list(head):
                    vals=df[i].tolist()
                    int_,fl=0,0
                    for j in range(10):
                    
                        if '.' in vals[j]:
                            fl+=1
                        elif RepresentsInt(vals[j]):
                    
                            int_+=1
                
                    if int_>7:
                        convert_dict={i:int}
                        df=df.astype(convert_dict)
                        
                    if fl >7:
                        convert_dict={i:float}
                        df=df.astype(convert_dict)

        except:
            df=None
            d=1
            head=None

     
   
     
    print('---------------------------------------------')
    print(df)
    print(head)
    print('-----------------------------------------------------')

    return df,ext,head,d


def get_dtype(data,headers):
    dataTypeDict = dict(data.dtypes)
    print(dataTypeDict)
    res = {}
    for i, v in dataTypeDict.items():
        res[v] = [i] if v not in res.keys() else res[v] + [i]
    #print(res)
    return res
    


########################################### MAIN #####################################################
def get_data(filepath,has_headers=1):

    filename=(filepath.split('/')[1]).split('.')[0]
    data,ext,headers,d=parser(filepath,has_headers)
    print(data,ext,headers)
    if d!=1:
        data_types=get_dtype(data,headers)
        return data, headers,data_types,filename,d
    else:
        return None, None, None, None, 1

def start_plotting(data, headers,data_types,filename):
  
    plot_uni(data,headers,data_types,filename)
        #time.sleep(1)
    plot_bi(data,headers,data_types,filename)
    # time.sleep(1)
    plot_3d(data,headers,data_types,filename)
        #time.sleep(2)
    plot_groupby(data,headers,data_types,filename)

    folders=['Univariate_Plots','Bivariate_Plots','Misc_Plots']
    import shutil
    for i in folders:
        
        zip_name = 'saved_plots/'+filename+'_'+i
        directory_name = zip_name
        shutil.make_archive(zip_name, 'zip', directory_name)
    







