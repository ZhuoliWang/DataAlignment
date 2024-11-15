# DataAlignment

This project is for data preprocessing for Xsens and iOS project.

## iOS Data Alignment
[iosDataAlign.py](iosDataAlign/iosDataAlign.py) is for preprocessing iOS data. There are several files collected from the phone, and the start and end times vary slightly across different devices. 

This code will merge these files into a single CSV file, retaining only the data that exists within the common time frame.

### How to use
* There is a dictionary `iosData` in the same directory as this Python file [iosDataAlign.py](iosDataAlign/iosDataAlign.py).
* Place all the data files you want to merge in dictionary `iosData`.
  * You can also change this dictionary by change the parameter `data_dic` in line 4.
* Then the merged file, `allData.csv`, will then be saved in the same directory as `iosDataAlign.py`.
