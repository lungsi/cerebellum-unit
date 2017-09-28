# =========================================================================
# responses.py
#
# created  27 July 2017 Lungsi
# modified 25 August 2017 Lungsi
#
# This py-file contains general capabilities for cerebellar cells.
#
# note: Each capability is its own class. The way SciUnit works is that the
#       method of the model must have the same name as the name of the
#       method in the capability class. Thus both the model class and the
#       capability class must have the same method name.
#
# ---------------------------------------------------------------------
#                    GENERAL CEREBELLAR CELL CAPABILITIES
#            Class name               |          method name
# ---------------------------------------------------------------------
#   ProducesSpikeTrain                |      produce_spike_train
#   ProducesElectricalResponse        |      produce_voltage_response
# ---------------------------------------------------------------------
# =========================================================================

import sciunit


# ========================Produce Spike Capability=========================
class ProducesSpikeTrain(sciunit.Capability):
    '''
    The model produces spike(AP).
    '''
    def __init__(self):
        pass
    def produce_spike_train(self):
        '''
        gets spike train
        '''
        raise NotImplementedError("Must implement produce_spike_train")
# ========================================================================


# ======================Produce Electrical Capability=====================
class ProducesElectricalResponse(sciunit.Capability):
    '''
    The model produces electrical responses.
    '''
    def __init__(self):
        pass
    def produce_voltage_response(self):
        '''
        get voltage response
        '''
        raise NotImplementedError("Must implement produce_voltage_response")
# ========================================================================


# ========================Name of the Capability==========================
#
# ========================================================================
