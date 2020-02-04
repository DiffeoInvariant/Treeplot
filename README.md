# Treeplot
Plots fractal trees.

For examples of how to write an options file for treeplot, see the hw3_options directory. (NOTE: you can also pass the options as command-line arguments to the program)

To see all the options and explanations for their uses, use

```
./treeplot --help
```

or

```
./treeplot -h
```

To run the program with an options file--say, hw3_options/options_1.txt--just do

```
./treeplot --file hw3_options/options_1.txt
```

or equivalently

```
./treeplot -f hw3_options/options_1.txt
```

An interesting feature that's available is estimation of the fractal (Hausdorff) dimension of the generated tree, which can be enabled with the option --hausdorff_dimension, for example like

```
./treeplot.py --hausdorff_dimension 1.0e-6 -f hw3_options/options_12.txt
```
