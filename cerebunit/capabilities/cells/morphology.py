import sciunit

# =======================Can Disconnect Dendrite========================
class CanDisconnectDendrites(sciunit.Capability):
    '''
    The model can disconnect dendrites from the soma.
    '''
    def __init__(self):
        pass
    def disconnect_all_dendrites(self):
        '''
        disconnect all dendrites from the soma
        '''
        raise NotImplementedError("Must implement disconnect_all_dendrites")
# ======================================================================
#
# ========================Turns Off AIS Channel=========================
#class TurnsOffAISChannels(sciunit.Capability):
#    '''
#    The model can turn off channels in AIS.
#    '''
#    def __init__(self):
#        pass
#    def turn_off_AIS_channel(self):
#        '''
#        turn off channels in AIS
#        '''
#        raise NotImplementedError("Must implement turn_off_AIS_channel")
