'''
Created on 23.01.2018

@author: mabelli
'''
import re

def find_id(self, name, lst):
        for item in lst:
            if re.match(name, item.Name):
                return item.ID