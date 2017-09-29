# ============================================================================
# test_for_firing_without_AIS_channels.py
#
# created  01 September 2017 Lungsi
# modified 29 September 2017 Lungsi
#
# ============================================================================

import sciunit
import quantities as pq
from elephant.statistics import mean_firing_rate as mfr

from cerebunit.capabilities.cells.response import ProducesSpikeTrain
from cerebunit.capabilities.cells.knockout import CanKOAISChannels
from cerebunit.score_manager import BinaryScore


class NoChannelsAISTest(sciunit.Test, BinaryScore):
    '''
    The No Channels AIS Test is a test for whether firing occurs (from the soma) without the channels. There is no current injection for this test.
    '''
    required_capabilities = (CanKOAISChannels,ProducesSpikeTrain,)
    score_type = BinaryScore

    def generate_prediction(self, model, verbose=False):
        '''
        fdf
        '''
        setup_parameters = { "dt": 0.025,   "celsius": 37,
                             "tstop": 1000, "v_init": -65 }
        model.ko_AIS_channels()
        model.set_simulation_properties(setup_parameters)
        model.produce_spike_train()
        return model

    def process_prediction(self, model):
        '''
        afdd
        '''
        cell_region = "vm_soma"
        return mfr(model.predictions["spike_train"][cell_region])


    def validate_observation(self, observation, first_try=True):
        '''
        fdfd
        '''
        pass

    def compute_score(self, observation, model, verbose=False):
        '''
        fdfd
        '''
        processed_prediction = self.process_prediction(model)
        a_prediction = processed_prediction.item() # just the magnitude
        x = BinaryScore.compute( observation, a_prediction )
        score = BinaryScore(x)
        score.description = "The No Channels in AIS Firing test results in the prediction by the model to be " + str(processed_prediction) + " which means that the " + str(score)
        return score
