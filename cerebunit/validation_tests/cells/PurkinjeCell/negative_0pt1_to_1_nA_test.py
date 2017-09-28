# ============================================================================
# negative_0pt1_to_1_nA_test.py
#
# created  01 September 2017 Lungsi
# modified 2017 Lungsi
#
# ============================================================================

import sciunit
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
#from cerebunit.statistical_tests.interval import NameHereScore


class NegativeStepCurrentTest(sciunit.Test, sciunit.Score):
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
                             "tstop": 4500, "v_init": -65 }
        model.set_simulation_properties( setup_parameters )
        # ================Negative Step Currents (nA)==================
        negative_currents = { "current1":
                              {"amp": -0.1, "dur": 1000.0, "delay": 300.0},
                              "current2":
                              {"amp": -0.2, "dur": 1000.0, "delay": 1300.0},
                              "current3":
                              {"amp": -0.5, "dur": 1000.0, "delay": 2300.0},
                              "current4":
                              {"amp": -1.0, "dur": 1000.0, "delay": 4300.0}
                            }
        model.set_stimulation_properties( negative_currents )
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
