#!/bin/bash
find packages | parallel file | grep -E '(executable)|(\.exe)|(\.pyc)' | grep -v text | tee new_sus_files.txt
