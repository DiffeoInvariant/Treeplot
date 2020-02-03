#!/usr/bin/fish

for opts in hw3_options/*.txt
	    ./treeplot.py -f $opts
end
