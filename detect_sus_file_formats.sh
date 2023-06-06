#!/bin/bash
find packages | parallel file | grep executable | grep -v text | tee -a sus_files.txt
find packages | parallel file | grep -F .pyc | tee -a sus_files.txt
find packages | parallel file | grep -F .exe | tee -a  sus_files.txt
find packages | parallel file | grep -F .sh | tee -a sus_files.txt

cp sus_files.txt sus_files.txt.1
sort -u sus_files.txt.1 > sus_files.txt
rm sus_files.txt.1

