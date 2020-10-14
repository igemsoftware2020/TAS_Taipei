
# How to Use VisualpH

## Parsing a new video

Use the following command:

> python3 vpH.py -p 'filename.py'

and it will bring up a window to select the tubes to process

the following argument can be added to the end of the command to shrink the size of the window by any constant

> -sm 0.5

The process command will automatically save the data files in /data/, with the names 0, 1, 2, 3 ...

make sure you rename these files before processing the next video if you want to save them

The following command can be used for data files that have already been processed

> python3 vpH.py -r 'filename.npy'

If you have a set of data files you want to display on a graph, use the following argument
where x is an integer above 1

> -m x

x will denote the number of files to process, starting from 0 to x-1


# Modelling
TAS_Taipei developed our own script, VisualpH, that measures the pH of a solution, or even the change in pH over time with just a photo or video. This allows the quantification of pH data for small volumes of solutions where we are unable to use a conventional pH meter. With this software we are able to model the reaction and find the relations between different reactants to optimize the reaction time.

## VisualpH

VisualpH is a python script that utilizes the openCV api to analyze photos and videos and extract pH data from it. The software takes the average hue of each tube at every frame, and using a standard generated from the pH indicator used, the hue can be converted to ph. 

![alt text](assets/Annotation.png)

The location of each tube is first selected by the user, and the software then collects the values of those pixels at every frame in the video. The RGB data is converted into HSV, but only the hue data is used. 

The hue can be converted to pH using the following equation where *pH* is the pH, *h* is hue, and *a*, *b*, *c* are constants. 

![alt text](assets/equation.png)

Using this equation, we can get a model of the advancement of the reaction over time. 
