# NgSpice_data_generator
**Python script to generate data from netlist file**


Ngspice is a mixed-level/mixed-signal electronic circuit simulator that is compatible with linux, windows and mac. 
Ngspice can write simulation data such input and output as output data in a separate file. This script automatically run a netlist in Ngspice and is able to downsample or upsample among data to generate fixed-size dataset


Commands 
---
1. get help ```python3 Datagenerator.py -h ```
2. calculate runtime ``` python3 Datagenerator.py -r [netlistname] ``
    Calculate runtime for generate each dataset in a linux machines 
3. generate data ``` python3 Datagenerator.py -g [netlistname] [train/test] ``` 
  data generation will run the input netlist in NgSpice and fix generated data, then save them is ./Fixd path
  train or test will specifies you generate training dataset or test.\\
  As data generation for each component is diffrent you need to change training and test part manually inside the code. 


Python dependencies
---
* numpy: v. 1.19.5
* scipy: v. 1.6.3
* os
* sys
