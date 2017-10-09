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


# ==========================BinaryScore=======================================
# created  21 September 2017 Lungsi
# modified 29 September 2017 Lungsi
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
                if measurement[key]-epsilon <= prediction \
                        <= measurement[key]+epsilon:
                    self.score = 1
                else:
                    self.score = 0
        return self.score

    _description = ( "The BinaryScore gives a score of 0 or 1 based on the comparison between prediction vs. measurement. "
                   + "The prediction is a python quantities, i.e, it is in the form of array(x.x) * <some_unit>. "
                   + "The measurement is also a python quantity, but in dictionary form. "
                   + "If the measurement has only 1-key, its value is the one that is the reference. "
                   + "The predicted value is then compared against the measurement with margin of error given by a default epsilon value. "
                   + "Therefore, BinaryScore checks that the predicted value is inside the interval. "
                   + "If it is not it, a score-0 is given. "
                   + "If the measurement has an addition error-key its value is the epsilon.")

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "BinaryScore is " + str(self.score)
# ============================================================================
#
# =========================BinaryMatrixScore==================================
# created  21 September 2017 Lungsi
# modified 29 September 2017 Lungsi
#
class BinaryMatrixScore(sciunit.Score):
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
    def compute(self, list_of_binary_scores, breakdown_of_binary_scores):
        # mesurement is in dictionary form whose value has
        # magnitude and python quantity
        # default epsilon = 10**(-3)
        no_of_scores = len(list_of_binary_scores)
        cummulative_score = sum(list_of_binary_scores)
        if cummulative_score == 0:
            self.score = 0
        elif (cummulative_score >= 0) and (cumulative_score < no_of_scores):
            self.score = 0
        elif cummulative_score == no_of_scores:
            self.score = 1
        #
        self.score_breakdown = breakdown_of_binary_scores
        return self.score

    _description = ( "The BinaryScore gives a score of 0 or 1 based on the comparison between prediction vs. measurement. "
                   + "The prediction is a python quantities, i.e, it is in the form of array(x.x) * <some_unit>. "
                   + "The measurement is also a python quantity, but in dictionary form. "
                   + "If the measurement has only 1-key, its value is the one that is the reference. "
                   + "The predicted value is then compared against the measurement with margin of error given by a default epsilon value. "
                   + "Therefore, BinaryScore checks that the predicted value is inside the interval. "
                   + "If it is not it, a score-0 is given. "
                   + "If the measurement has an addition error-key its value is the epsilon.")

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "BinaryMatrixScore is " + str(self.score)
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
