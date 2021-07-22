import numpy as np
import os
import sys
from scipy.interpolate import interp1d

     # interpolate 
     
def UniformSteps(DataFileAddress, TimeSteps=200, kind='linear'):
    # read data file
    '''
    DataFileAddress : address of .txt data file.
    TimeSteps: number of output steps, default 200 row of data will generate.
    kind: interpolation kind. defulat is linear but it can be 'nearest' , 'cubic' or etc. (look at scypy documents).
    '''    
    SampleData=np.loadtxt(DataFileAddress,dtype=float)
    
  
        #interpolate data
    input_interpolate=interp1d(SampleData[:,0],SampleData[:,1],kind=kind)
    output_interpolate=interp1d(SampleData[:,0],SampleData[:,3],kind=kind)

    #find border of Time vector and generate new time vector with fixed steps
    mintime=min(SampleData[:,0])
    maxtime=max(SampleData[:,0])
    newtime=np.linspace(mintime ,maxtime,num=TimeSteps,endpoint=False)
    
    return np.transpose([newtime,input_interpolate(newtime),output_interpolate(newtime)])


def SavedUniformedData(UniformedFileAddress, UniformedData, delimiter='\t'):
    ''' 
    UniformedFileAddress: name and address of uniformed  data to save it. .txt format
    UniformedData: array of data that has been uniformed in given steps.
    delimiter: delimiter of output file
    '''
    np.savetxt(UniformedFileAddress,UniformedData ,delimiter=delimiter)
    print('werite succesfull')

def generate_data(netlistname, ChangeParamList, TrainTest='train'):
    #print to file
    fid=open(netlistname,'r')
    netfile_text=fid.read()
    fid.close()

    #initial
    save_filenameOld='wrdata sn1126-*.txt v(A) v(Y)'
    VinOld='Vin A 0 PULSE(0 Vh 1n Trn Tfn 50n 100n)'
    

    #generate train and test data
    if TrainTest=='train':
        Vin_High = [4.8, 5.0, 5.2] # generate train data
        Tr = Tf = [2, 2.33, 2.66, 3]
        
    else:
        Vin_High = [4.9, 5.0, 5.1] # generate test data
        Tr = Tf = [2.5]
        

    
    i=0
    for j in range(len(Vin_High)):
        for k in range(len(Tr)):
            # manipulate new file 
            
            save_filenameNew='wrdata SN1126-'+str(i)+'.txt v(A) v(Y)'
            VinNew='Vin A 0 PULSE(0 '+str(Vin_High[j])+' 1n '+str(Tr[k])+'n '+str(Tf[k])+'n 50n 100n)'
            netfile_text=netfile_text.replace(VinOld,VinNew)
            netfile_text=netfile_text.replace(save_filenameOld,save_filenameNew)
            
            #update
            save_filenameOld=save_filenameNew
            VinOld=VinNew
            i+=1

            print(netfile_text)
            # save file
            fid=open('NewNetlist.net','w')
            fid.write(netfile_text)
            fid.close()

            datafileaddress='SN1126-'+str(i-1)+'.txt'
            os.system('ngspice NewNetlist.net')
            uniformedDat=UniformSteps(DataFileAddress=datafileaddress,TimeSteps=251)
            if TrainTest == "train":
                SavedFoleAddress='Fixed/Train/'+str(datafileaddress)
            else:
                SavedFoleAddress='Fixed/Test/'+str(datafileaddress)

            SavedUniformedData(SavedFoleAddress,uniformedDat)
            
def timecalculator(netlistname):
    import time
    executefile='ngspice '+str(netlistname)
    run_itr=20
    total_time=0
    for i in range(run_itr):
        begin=time.time()
        os.system(executefile)
        end=time.time()
        total_time+=end-begin

    print('total time in sec: '+str(total_time/run_itr))
   
def help():
    help= '''This is a file generator for ngspice witch recive a netlist and generate data by list of parameters that inserted. to use it, enter 
    -h          : help
    -r          : runtime, calculate runtime of one round of data generation by ngspice. NOTICE: netlist should be on run and quit mode. Do not plot or write anything.
    -g          : generate data. three input parameter will get this function. 
          ''' 
    print(help)

if __name__ == "__main__":
    controlparameter=sys.argv[1]
    if controlparameter=='-h':
        help()
    elif controlparameter=='-r':
        timecalculator(netlistname=sys.argv[2])
    elif controlparameter=='-g':
        generate_data(netlistname=sys.argv[2],ChangeParamList=['Vin','Freq','Vo'],TrainTest=sys.argv[3])
    else:
        print('Wrong parameters. enter -h to find help')
