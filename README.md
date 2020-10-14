
# How to Use VisualpH

## prereqs
make sure you have installed python 3, and that pip is properly working. Once that is done, run

> pip install -r requirements.txt

to install the dependencies.

## Example

run the following commands in the terminal

linux
> python3 vpH.py -p "exampleData/C-19DNA.mov" -sm 0.5 -pp 3

windows
> python vpH.py -p "exampleData/C-19DNA.mov" -sm 0.5 -pp 3

then, select 3 points to encircle the coloured portion of the leftmost microcentrifuge tube
repeat the same for all 4, from left to right

note that the default is 4 points, but the argument -pp 3 overrides that
The video is also of a fairly large resolution, so the window can be shrinked and expanded using -sm

After the video is processed, a window should pop up that shows graphs of each tube over time.

To see each graph individually, run

linux
> python3 vpH.py -r 0.npy

windows
> python vpH.py -r 0.npy

To see all 4 again, run

linux
> python3 vpH.py -m 4

windows
> python vpH.py -m 4

## Parsing a new video

Use the following command:

linux
> python3 vpH.py -p "filename.py"

windows
> python vpH.py -p "filename.py"

and it will bring up a window to select the tubes to process

the following argument can be added to the end of the command to shrink the size of the window by any constant

> -sm 0.5

The process command will automatically save the data files in /data/, with the names 0, 1, 2, 3 ...

make sure you rename these files before processing the next video if you want to save them

## Displaying parsed data

The following command can be used for data files that have already been processed

linux
> python3 vpH.py -r "filename.npy"

windows
> python vpH.py -r "filename.npy"

If you have a set of data files you want to display on a graph, use the following argument
where x is an integer above 1

> -m x

x will denote the number of files to process, starting from 0 to x-1