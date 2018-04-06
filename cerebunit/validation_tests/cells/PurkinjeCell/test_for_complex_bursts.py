# ============================================================================
# test_for_complex_bursts.py
#
# created  10 October 2017 Lungsi
# modified
#
# ============================================================================
#
import os
#
import numpy as np
import sciunit
import quantities as pq
from elephant.statistics import isi
#
from cerebunit.file_manager import get_folder_path_and_name as gfpan
from cerebunit.score_manager import BinaryScore
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
#
#
class ComplexBurstingTest(sciunit.Test):
    '''
    The Complex Bursting Test is a test comparing the observed spiking frequency in real animal to those generated by the model (from soma, "vm_soma"). This is done by comparing the mean spike frequencies.
    '''
    required_capabilities = (ProducesSpikeTrain,)
    score_type = BinaryScore
    #
    def generate_prediction(self, model, verbose=False):
        '''
        Generates spike train from various cell regions.
        Default cell_regions = {"vm_soma": 0.0, "vm_NOR3": 0.0}
        The value of each key is the threshold defined for
        spiking.
        The function is automatically called by sciunit.Test
        which this test is a child of.
        Therefore as part of sciunit generate_prediction is
        mandatory.
        '''
        # Inject current >= 2 nA
        self.inj_current = \
                { "current1":
                    {"amp": 2.0, "dur": 4000.0, "delay": 1000.0} }
        stimulus = \
                model.set_stimulation_properties( self.inj_current )
        # below is necessary step for correct simulation result
        [ stimulus[i].loc(0.5, sec=model.cell.soma) \
                for i in range(len(stimulus)) ]
        #
        setup_parameters = { "dt": 0.025,   "celsius": 37,
                             "tstop": 4000, "v_init": -65 }
        model.cell_regions = {"vm_soma": 0.0}
        model.set_simulation_properties( setup_parameters )
        #
        model.set_stimulation_properties( self.inj_current )
        #
        model.produce_spike_train()
        #self.process_prediction(model)
        return model
#
#
    def get_isi_for_current(self, model):
        '''
        The model.produce_spike_train() results in spike train for
        the initial (no injection), injection and later (no inject)
        This function calculates the isi for the whole spike train
        Then return the isi for spike train during injection alone.
        **As of Neo5.1 and Elephant4.1 isi(for_sliced_spike_train)
        generates an error. So isi(whole_spike_train) is taken here.
        ======================Use Case============================
        sliced_isi = self.get_isi_for_current(model)
        ===========================================================
        This function is called by process_prediction
        '''
        # get all the spike train for desired cell region
        all_spike_train = \
                model.predictions["spike_train"]["vm_soma"]
        # set the time boundaries for the spike train
        current_key = self.inj_current.keys()[0] # for only 1 current
        current_start = \
                self.inj_current[current_key]["delay"]
        current_stop = current_start \
                + self.inj_current[current_key]["dur"]
        #
        sliced_indices = []
        for i, j in enumerate(all_spike_train):
            if j >= current_start and j <= current_stop:
                sliced_indices.append(i)
        #
        all_isi = isi(all_spike_train)
        sliced_isi = all_isi[ sliced_indices[0] : sliced_indices[-1] ]
        #
        return sliced_isi
#
#
    def process_prediction(self, model):
        '''
        Once the model has run, this function can be used to
        process the sliced_isi prediction to get the coefficient of
        variation.
        ========================Use Case==============================
        coeff_var = self.process_prediction(model)
        ==============================================================
        This function is called by compute_score
        '''
        # get isi for spike train only during current injection
        sliced_isi = self.get_isi_for_current(model)
        # compute the coeff. of variation
        coeff_variation = np.std(sliced_isi)/np.mean(sliced_isi)
        # return without quantity term since this is dimensionless
        return coeff_variation.item()
#
#
    def validate_observation(self, observation, first_try=True):
        pass
#
#
    def compute_score(self, observation, model, verbose=False):
        '''
        This function like generate_pediction is called automatically
        by sciunit which SpontaneousFiringTest is a child of.
        This function must be named compute_score
        This function calls the function process_prediction to return
        - coefficient of variation of spike trains during injection
          from our region of interest, "vm_soma".
        The prediction processed from "vm_soma" is then compared against
        the experimental_data to get the binary score; 0 if the
        prediction correspond with experiment, else 1.
        '''
        a_prediction = self.process_prediction(model)
        x = BinaryScore.compute( observation,
                                 a_prediction  )
        score = BinaryScore(x)
        score.description = "The complex bursting test is defined by checking if the coefficient of variation of the model = " + str(a_prediction) + " is " + str(observation) + " whose " + str(score)
        if score.score==1:
            ans = "The model " + model.name + " passed the " + self.__class__.__name__ + ". The coefficient of variation of the model = " + str(a_prediction) + " > 1."
        else:
            ans = "The model " + model.name + " failed the " + self.__class__.__name__ + ". The coefficient of variation of the model = " + str(a_prediction) + " not > 1."
        print ans
        return score


