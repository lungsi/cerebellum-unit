# ============================================================================
# positive_0pt1_to_1pt5_nA_test.py
#
# created  01 September 2017 Lungsi
# modified 2017 Lungsi
#
# ============================================================================

import sciunit
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
#from cerebunit.statistical_tests.interval import NameHereScore


class PositiveStepCurrentTest(sciunit.Test, sciunit.Score):
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
                             "tstop": 5500, "v_init": -65 }
        model.set_simulation_properties( setup_parameters )
        # ================Positive Step Currents (nA)==================
        positive_currents = { "current1":
                              {"amp": 0.1, "dur": 1000.0, "delay": 300.0},
                              "current2":
                              {"amp": 0.2, "dur": 1000.0, "delay": 1300.0},
                              "current3":
                              {"amp": 0.5, "dur": 1000.0, "delay": 2300.0},
                              "current4":
                              {"amp": 1.0, "dur": 1000.0, "delay": 3300.0},
                              "current5":
                              {"amp": 1.5, "dur": 1000.0, "delay": 4300.0}
                            }
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
