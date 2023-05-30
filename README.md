# Blinking-Model
This model consists of a group of follower and a leader (described as Imam in the code) that blink at random times. 
There exists a probability that a follower will change their blinking time to match that of the Imam - probability decreases with row number- 
and when a follower blinks, there is a probability that the adjacent followers will blink.  
The former is called Imam Probability. The variable that controls how much Imam probability decreaese with each row is called Row Multiplier.
The latter is called follower Probability.

The two plots that could be turned on both have Blink groups on the y-axis, and one has Imam probabilty on the x-axis , while the other 
has (Row multiplier * Follower Probability) on the x-axis. Syncronization would occur when the number of Blink groups is equal to 1. 

In the model, A red rectangle is a follower that is blinking. A rectangle turns green if the follower blinks at the same time as the Imam, grey if it is affected by its neighbor and blinks at the same time as it, black if it blinks at its own natural blinking time. 

This project was inspired by Muslim prayer and Syncronization of sound during this prayer, but the model could be applicable to other areas.



