# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        states = self.mdp.getStates()
        for k in range(self.iterations):
            next_values = util.Counter()
            for s in states:
                actions = self.mdp.getPossibleActions(s)
                max_value_s = -9999
                for a in actions:
                    transition = self.mdp.getTransitionStatesAndProbs(s, a)
                    sum_of_values = 0.0
                    for state_prob in transition:
                        print(state_prob)
                        sum_of_values += state_prob[1] * (self.mdp.getReward(s, a, state_prob[0]) + (self.discount * self.values[state_prob[0]]))
                    max_value_s = max(max_value_s, sum_of_values)
                if max_value_s != -9999:
                    next_values[s] = max_value_s
                    
            for s in states:
                self.values[s] = next_values[s]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        value = 0.0
        for stateProb in self.mdp.getTransitionStatesAndProbs(state, action):
            value += stateProb[1] * (self.mdp.getReward(state, action, stateProb[0]) + self.discount * self.values[stateProb[0]])

        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        max_value = -99999
        max_action = None

        for action in self.mdp.getPossibleActions(state):
            action_value = self.computeQValueFromValues(state, action)
            if action_value > max_value:
                max_value = action_value
                max_action = action
        return max_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()

        for k in range(self.iterations):
            state = states[k % len(states)]
            if self.mdp.isTerminal(state):
                continue
            q_value = list()
            for action in self.mdp.getPossibleActions(state):
                q_value.append(self.getQValue(state, action))
            self.values[state] = max(q_value)
        
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def get_max_value(self,state):
        max_value = -9999
        for action in self.mdp.getPossibleActions(state) :
            q_value = self.computeQValueFromValues(state, action)
            if(q_value > max_value):
                max_value = q_value
        return max_value

        
    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        # creating predecessors dictionary
        predecessors = dict()

        for s in self.mdp.getStates():
            predecessors[s]= list()
        
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for stateProb in self.mdp.getTransitionStatesAndProbs(state, action):
                        predecessors[stateProb[0]].append(state)
    
        # creating a empty queue for keep priorities
        queue = util.PriorityQueue()

        # for non-terminal states we add them to the queue 
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                max_value = self.get_max_value(state)
                diff = abs(self.values[state] - max_value)
                queue.update(state, -diff)



        # for the number of iterations we run the algorithm
        for iteration in range(self.iterations):
            if queue.isEmpty():
                break
            state = queue.pop()
            if not self.mdp.isTerminal(state):
                max_value = self.get_max_value(state)
                self.values[state] = max_value

            # calculating the diff again, and then we will update the value
            # if it was more than theta
            for p in predecessors[state]:
                if not self.mdp.isTerminal(p):
                    max_value = self.get_max_value(p)
                    diff = abs(self.values[p] - max_value)
                    if diff > self.theta:
                        queue.update(p, -diff)
