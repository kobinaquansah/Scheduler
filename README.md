# Scheduler
# Introduction
This is a mockup of a scheduler which probabilistically finds possible combinations of schedules of teachers under constraints.

# Availability:
There is a total of 5 work days a week with 6 total slots each. Slots can either be open or closed. Only open slots can be assigned to teachers.

# Responsibility:
Each teacher is responsible for one or more sets of students. The teacher in question must take each set of students a definite number of times. eg. Teacher 1 teaches Set 1 twice a week. Teacher 1 also teaches Set 2 twice a week.

#Constraints:
One teacher cannot teach two classes at the same time.
One class cannot be taught by two teachers at the same time.

This mockup was performed on a timetable consisting of only two of the 5 workdays in a week. Some available slots were labelled as closed by assigning the value of 1 to their respective cells. Each teacher had an alphanumeric representation of how many lectures they will deliver per set. eg ["1A","3B"] means the teacher in question must lecture student set A once and student set B three times.
