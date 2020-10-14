
# How to Use VisualpH

## Parsing a new video

Use the following command:

> python3 vpH.py -p 'filename.py'

and it will bring up a window to select the tubes to process

the following argument can be added to the end of the command to shrink the size of the window by any constant

> -sm 0.5

The process command will automatically save the data files in /data/, with the names 0, 1, 2, 3 ...

make sure you rename these files before processing the next video if you want to save them
s
The following command can be used for data files that have already been processed

> python3 vpH.py -r 'filename.npy'

If you have a set of data files you want to display on a graph, use the following argument
where x is an integer above 1

> -m x

x will denote the number of files to process, starting from 0 to x-1

## Windows

The above applies, but use the 
> python 
command rather than 
> python3