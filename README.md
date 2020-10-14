
# How to Use VisualpH

## python
make sure you have installed python 3, and that pip is properly working. Once that is done, run

> pip install -r requirements.txt

to install the dependencies.

## Parsing a new video

Use the following command:

linux
> python3 vpH.py -p 'filename.py'

windows
> python vpH.py -p 'filename.py'

and it will bring up a window to select the tubes to process

the following argument can be added to the end of the command to shrink the size of the window by any constant

> -sm 0.5

The process command will automatically save the data files in /data/, with the names 0, 1, 2, 3 ...

make sure you rename these files before processing the next video if you want to save them

## Displaying parsed data

The following command can be used for data files that have already been processed

linux
> python3 vpH.py -r 'filename.npy'

windows
> python vpH.py -r 'filename.npy'

If you have a set of data files you want to display on a graph, use the following argument
where x is an integer above 1

> -m x

x will denote the number of files to process, starting from 0 to x-1

## Windows

The above applies, but instead of using the command python3 use
> python 