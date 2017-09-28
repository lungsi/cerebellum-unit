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
