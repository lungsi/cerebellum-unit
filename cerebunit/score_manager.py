# ============================================================================
# score_manager.py
#
# created 21 September 2017 Lungsi
#
# This py-file contains custum score functions initiated by
#
# from cerebuint import score_manager
# ============================================================================

import sciunit
import quantities as pq

# ==========================BinaryScore=======================================
# created  21 September 2017 Lungsi
# modified 12 October 2017 Lungsi added functionality for inequality
#
class BinaryScore(sciunit.Score):
    '''
    A Binary Score.
    0 if the prediction is not in the interval of the measurement within a margin of error (epsilon).
    '''
    #
    # -----------------------------Use Case-----------------------------------
    # x = BinaryScore.compute( measurement, prediction )
    # score = BinaryScore(x)
    # ------------------------------------------------------------------------
    #
    @classmethod
    def compute(self, measurement, prediction, epsilon=10**(-3)):
        # mesurement is in dictionary form whose value has
        # magnitude and python quantity
        # default epsilon = 10**(-3)        
        if len(measurement.keys()) > 1:
            for key in measurement:
                if key=="error":
                    epsilon_left = measurement[key]
                    epsilon_right = epsilon_left
                elif key=="error_left":
                    epsilon_left = measurement[key]
                elif key=="error_right":
                    epsilon_right = measurement[key]
                else:
                    amount = measurement[key]
            # Then
            if amount-epsilon_left <= prediction <= amount+epsilon_right:
                self.score = 1
            else:
                self.score = 0
        else:
            # For only one key
            for key in measurement:
                if key.lower()=="inequality":
                    str_num = measurement[key].split()[1]
                    num = float( ''.join(x for x in str_num if x.isdigit() or x=='.') )
                    if ">" in measurement[key]:
                        if prediction > num:
                            self.score = 1
                        else:
                            self.score = 0
                    elif "<" in measurement[key]:
                        if prediction < num:
                            self.score = 1
                        else:
                            self.score = 0
                    elif "!=" in measurement[key]:
                        if prediction != num:
                            self.score = 1
                        else:
                            self.score = 0
                    else:
                        raise ValueError("The inequality value must be of the form; > number or < number or != number")
                else:
                    amount = measurement[key]
                    if type(amount) is pq.quantity.Quantity:
                        amount = amount.item()
                    else:
                        amount = float(amount)
                    # Then
                    if amount-epsilon <= prediction <= amount+epsilon:
                        self.score = 1
                    else:
                        self.score = 0
        return self.score

    _description = ( "The BinaryScore gives a score of 0 or 1 based on the comparison between prediction vs. measurement, with "
                   + "\n 0: Fail"
                   + "\n 1: Pass"
                   + "\n\nDetails: The prediction is a python quantities, i.e, it is in the form of array(x.x) * <some_unit>. "
                   + "The measurement is also a python quantity, but in dictionary form. "
                   + "If the measurement has only 1-key, its value is the one that is the reference. "
                   + "The predicted value is then compared against the measurement with margin of error given by a default epsilon value. "
                   + "Therefore, BinaryScore checks that the predicted value is inside the interval. "
                   + "If it is not, a score-0 is given. "
                   + "If the measurement has an addition error-key its value is the epsilon.")

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "BinaryScore is " + str(self.score)
# ============================================================================
#
# =========================OverallBinaryScore==================================
# created  09 October 2017 Lungsi
# modified 
#
class OverallBinaryScore(sciunit.Score):
    '''
    An Overall Binary Score.
    0 if all the Binary Scores in a set are 0 or < sum of all the scores
    1 if the sum of all the scores = number of scores
    '''
    #
    # -----------------------------Use Case-----------------------------------
    # x = OverallBinaryScore.compute( list_of_binary_scores,
    #                                 breakdown_of_binary_scores )
    # score = OverallBinaryScore(x)
    # score.score # will give you the 0 or 1
    # score.breakdown # will give you the breakdown of the scores
    # ------------------------------------------------------------------------
    #
    @classmethod
    def compute(self, list_of_binary_scores, breakdown_of_binary_scores):
        # list_of_binary_scores = list of 0's and 1's
        # breakdown_of_binary_scores = any details of each binary score
        #
        no_of_scores = len(list_of_binary_scores)
        cummulative_score = sum(list_of_binary_scores)
        if cummulative_score == 0:
            self.score = 0
        elif (cummulative_score >= 0) and (cummulative_score < no_of_scores):
            self.score = 0
        elif cummulative_score == no_of_scores:
            self.score = 1
        #
        self.breakdown = breakdown_of_binary_scores
        return self.score

    _description = ( "The OverallBinaryScore gives a score of 0 or 1 based on the BinaryScores for each measurement vs prediction in a sample. "
                   + "The BinaryScores themselves can either be 0 or 1. "
                   + "Lets say the list of BinaryScores are  [0, 0, 0, 0, 0]. "
                   + "The OverallBinaryScore = 0 if sum([0, 0, 0, 0, 0]) = 0 or < len([0,0,0,0,0]) "
                   + "The OverallBinaryScore = 1 if sum([1, 1, 1, 1, 1]) = len([1,1,1,1,1]) "
                   + "Therefore, OverallBinaryScore checks that all the BinaryScore are 1 "
                   + "If it is not it, a score-0 is given.")

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "OverallBinaryScore is " + str(self.score)
# ============================================================================
#
# ==========================Score=============================================
class NameHereScore(sciunit.Score):
    '''
    text
    '''

    def __init__(self):
        pass
# ============================================================================
