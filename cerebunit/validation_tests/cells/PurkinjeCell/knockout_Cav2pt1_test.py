# ============================================================================
# knockout_Cav2pt1_test.py
#
# created  01 September 2017 Lungsi
# modified 2017 Lungsi
#
# ============================================================================

import sciunit
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
#from cerebunit.statistical_tests.interval import NameHereScore


class KOCav2pt1Test(sciunit.Test, sciunit.Score):
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
        model.set_simulation_properties(setup_parameters)
        # =================Knock out Cav2.1 channels==================
        # in SOMA
        setattr(model, "cell.soma.pcabar_Cav2_1", 0)
        # in DENDRITES
        for d in model.cell.dend:
            setattr(d, "pcabar_Cav2_1", 0)
        # in AIS
        setattr(model, "cell.axonAIS.pcabar_Cav2_1", 0)
        # in NORs
        setattr(model, "cell.axonNOR.pcabar_Cav2_1", 0)
        setattr(model, "cell.axonNOR2.pcabar_Cav2_1", 0)
        setattr(model, "cell.axonNOR3.pcabar_Cav2_1", 0)
        # in COLLATERALS
        setattr(model, "cell.axoncoll.pcabar_Cav2_1", 0)
        setattr(model, "cell.axoncoll2.pcabar_Cav2_1", 0)
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
