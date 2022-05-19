# TestTask-Solution
The assignment solution for the sports mathematician position is located in the repository files.
 
3-4.docx is a solution for tasks 3 and 4. It is written in russian because the task was also given in russian.
## Assignment
**Conditions**

There is a standard table tennis match. Players take turns doing 2 serves until the score is 10-10 or one of them will not score 11. After 10-10 overtime starts. Overtime ends as soon as one of the players gains an advantage of 2 points.
Let's say we have 2 parameters:
- p1 - the probability of taking the round (serving) by the first player on his own filing.
- p2 - the probability of taking the round (serve) by the first player on the serve opponent.
⠀

**Tasks**
1. We believe that the match does not go into overtime (with a score of 10-10, the game ends). It is necessary to implement an algorithm that takes as input p1 and p2, and outputs the distribution of final scores in the format {(score1, score2): probability} in three ways:
 - Monte Carlo evaluation.
 - The passage of possible outcomes through the tree.
 - Finding a stationary distribution using the matrix transitions of the Markov process.

2. We believe that the starting score is 10-10. Implement the evaluation algorithm probabilities of each player winning in overtime provided that p1=p2, in the same ways.

3. Describe the comparative pros and cons of methods A, B, and C for both points.

4. Let's say we are doing a similar evaluation for Counter-Strike. One of the main features is that in case of taking the round, the team gains an advantage in the economy, which can help in taking the next round. Describe the applicability of the above methods to such a case.