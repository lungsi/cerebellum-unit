# ============================================================================
# ca_spikes_na_bursts_test.py
#
# created  01 September 2017 Lungsi
# modified 2017 Lungsi
#
# ============================================================================

import sciunit
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
#from cerebunit.statistical_tests.interval import NameHereScore


class CaSpikesNaBurstsTest(sciunit.Test, sciunit.Score):
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
                             "tstop": 4000, "v_init": -65 }
        model.set_simulation_properties( setup_parameters )
        # ========================2 nA currents========================
        positive_currents = \
                { "current1": {"amp": 2.0, "dur": 4000.0, "delay": 1000.0} }
        model.set_stimulation_properties( positive_currents )
        # =============================================================
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
