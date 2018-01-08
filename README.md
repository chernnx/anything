# Timetable Compiler 

We want to find the common time periods a group of people can meet
(i.e. mutual free time), given their course index numbers. The course
indexes contain information about their class timing.

Come up with a script that will:
- Print out the whole result as a heatmap/suitable visual
interpretation format
- Recommend the best option given the desired length of meeting
- Is adaptable to future changes (i.e. can bring in more info e.g. other blocked-off busy timeslots)

## Requirements

- matplotlib
- seaborn
- numpy
- bs4

(do a pip/pip3 install on your python directory)

## Task Breakdown

- Scrape the data from [here](https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main). Enter a space in the search bar to generate all the course info.
- Fill up blank 'index' columns with previous row entry in database 
- Master timetable stored in a 2-D numpy array

# Outstanding items
- Account for Online Courses (e.g. 28400,55050,70120,70130)
- Easier input (don't need input index number manually, maybe SS a pic of their timetable or of the indexes)
- Input sanity check (if index number wrong)
- Multi-user input
- Add course code/name to database
- Remove the *^ from the course title
- Account for the 'Week' information in Remarks
- Cases like ['00571', '\xa0', '1', '\xa0', '\xa0', '\xa0', '  Online Course ']
- Desired meeting length 
- If ‘Desired meeting length’ > 30mins, provide optimal meeting time for 3 cases: shorter (-15min), normal, longer (+15min). Else, provide optimal meeting time for the normal case and longer case