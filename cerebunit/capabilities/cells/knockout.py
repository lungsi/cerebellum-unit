import sciunit

# ===========================Can KO AIS Channel==========================
class CanKOAISChannels(sciunit.Capability):
    '''
    The model can turn off channels in AIS.
    '''
    def __init__(self):
        pass
    def ko_AIS_channels(self):
        '''
        turn off channels in AIS
        '''
        raise NotImplementedError("Must implement ko_AIS_channel")
# ======================================================================
#
# ==========================Can KO Cav2.1 Channel=======================
class CanKOCav2pt1Channels(sciunit.Capability):
    '''
    The model can turn off Cav2.1 channels.
    '''
    def __init__(self):
        pass
    def ko_Cav2_1_channels(self):
        '''
        turn off Cav2.1 channels from everywhere
        '''
        raise NotImplementedError("Must implement ko_Cav2_1_channels")
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
