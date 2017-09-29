# ============================================================================
# no_channels_AIS_test.py
#
# created  01 September 2017 Lungsi
# modified 2017 Lungsi
#
# ============================================================================

import sciunit
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
#from cerebunit.statistical_tests.interval import NameHereScore


class NoChannelsAISTest(sciunit.Test, sciunit.Score):
    '''
    ff
    '''
    required_capabilities = (ProducesSpikeTrain,)
    score_type = sciunit.Score

    def generate_prediction(self, model, verbose=False):
        '''
        fdf
        '''
        setup_parameters = { "dt": 0.025,   "celsius": 37,
                             "tstop": 1000, "v_init": -65 }
        model.set_simulation_properties(setup_parameters)
        # ===================Turn-off AIS channels====================
        setattr(model, "cell.axonAIS.pcabar_Cav3_1", 0)
        setattr(model, "cell.axonAIS.gbar_Nav1_6", 1)
        setattr(model, "cell.axonAIS.pcabar_Cav2_1", 0)
        # ============================================================
        model.produce_spike_train()
        return model

    def validate_observation(self, observation, first_try=True):
        '''
        fdfd
        '''
        pass

    def compute_score(self, model, verbose=False):
        '''
        fdfd
        '''
        pass
