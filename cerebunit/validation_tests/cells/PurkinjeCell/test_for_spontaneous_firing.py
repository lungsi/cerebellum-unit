# ============================================================================
# test_for_spontaneous_firing.py
#
# created  14 August 2017 Lungsi
# modified 29 September 2017 Lungsi
#
# ============================================================================

import os
from math import sqrt
import sciunit
import quantities as pq
from elephant.statistics import mean_firing_rate as mfr

from neuron import h

from cerebunit.file_manager import get_folder_path_and_name as gfpan
from cerebunit.score_manager import BinaryScore
from cerebunit.capabilities.cells.response import ProducesSpikeTrain


class SpontaneousFiringTest(sciunit.Test):
    '''
    The Spontaneous Firing Test is a test comparing the observed spiking frequency in real animal to those generated by the model (from soma, "vm_soma"). This is done by comparing the mean spike frequencies.
    '''
    required_capabilities = (ProducesSpikeTrain,)
    score_type = BinaryScore
    #
    # ================================Use Case==============================
    # from cerebunit.validation_tests.cells.PurkinjeCell \
    #        import SpontaneousFiringTest as sft
    # test = sft(some_data)
    # s = test.judge(some_model, deep_error=True)
    # ======================================================================
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
        # this is not needed for running the test multiple times
        # but if you are running the model in an interpreter and then the test
        # resetting the model is essential
        #model.reset()
        #
        print("generate prediction...")
        print ("size of rec_t is "+ str(model.cell.rec_t.size()) +
               " and its current value is "+ str(h._ref_t[0]))
        print ("size of vm_soma is "+ str(model.cell.vm_soma.size()) +
               " and its current value is "+ str(model.cell.soma(0.5)._ref_v[0]))
        print ("size of vm_NOR3 is "+ str(model.cell.vm_NOR3.size()) +
               " and its current value is "+ str(model.cell.axonNOR3(0.5)._ref_v[0]))
        #
        setup_parameters = { "dt": 0.025,   "celsius": 37,
                             "tstop": 1000, "v_init": -65 }
        model.cell_regions = {"vm_soma": 0.0}
        model.set_simulation_properties(setup_parameters)
        model.reset()
        print ("size of rec_t is "+ str(model.cell.rec_t.size()) +
               " and its current value is "+ str(h._ref_t[0]))
        print ("size of vm_soma is "+ str(model.cell.vm_soma.size()) +
               " and its current value is "+ str(model.cell.soma(0.5)._ref_v[0]))
        print ("size of vm_NOR3 is "+ str(model.cell.vm_NOR3.size()) +
               " and its current value is "+ str(model.cell.axonNOR3(0.5)._ref_v[0]))
        model.produce_spike_train()
        print ("size of rec_t is "+ str(model.cell.rec_t.size()) +
               " and its current value is "+ str(h._ref_t[0]))
        print ("size of vm_soma is "+ str(model.cell.vm_soma.size()) +
               " and its current value is "+ str(model.cell.soma(0.5)._ref_v[0]))
        print ("size of vm_NOR3 is "+ str(model.cell.vm_NOR3.size()) +
               " and its current value is "+ str(model.cell.axonNOR3(0.5)._ref_v[0]))
        #self.process_prediction(model)
        return model

    def process_prediction(self, model):
        '''
        Once the model has run, this function can be used to
        process the spike_train prediction to get the
        prediction of interest, mean firing rate.
        Prediction of interest implies all the listed cell_regions
        '''
        print("process prediction...")
        model_mean_firing_rates = {}
        for cell_region in model.cell_regions:
            x = mfr(model.predictions["spike_train"][cell_region])
            a_firing_rate = {cell_region: [x, x.rescale(pq.Hz)]}
            model_mean_firing_rates.update(a_firing_rate)
        #
        #self.processed_prediction = model_mean_firing_rates
        return model_mean_firing_rates


    def validate_observation(self, observation, first_try=True):
        '''
        This function is called automatically by sciunit.
        This checks if the experimental_data is of some desired
        form or magnitude.
        Not exactly this function but a version of this is already
        performed by the ValidationTestLibrary.get_validation_test
        '''
        print("validate observation...")
        if "mean" not in observation:
            raise sciunit.ObservationError
        if "error" in observation:
            pass
        elif "standard error" in observation and "n" in observation:
            # calculate standard deviation from standard error and number of observations
            self.observation = {
                "mean": observation["mean"],
                "error": observation["standard error"] * sqrt(observation["n"])
            }
        else:
            raise sciunit.ObservationError
        if "units" in observation:
            self.observation["mean"] = pq.Quantity(self.observation["mean"],
                                                   units=observation["units"])
            self.observation["error"] = pq.Quantity(self.observation["error"],
                                                    units=observation["units"])

    def compute_score(self, observation, model, verbose=False):
        '''
        This function like generate_pediction is called automatically
        by sciunit which SpontaneousFiringTest is a child of.
        This function must be named compute_score
        This function calls the function process_prediction to return
        the mean firing reate of spike trains from all the cell_regions
        Off al the cell_regions our region of interest is "vm_soma".
        The prediction processed from "vm_soma" is then compared against
        the experimental_data to get the binary score; 0 if the
        prediction correspond with experiment, else 1.
        '''
        print("compute score...")
        processed_prediction = self.process_prediction(model)
        a_prediction = processed_prediction["vm_soma"][1]
        #a_prediction = self.processed_prediction["vm_soma"][1]
        x = BinaryScore.compute( observation,
                                 a_prediction  )
        score = BinaryScore(x)
        score.description = "The spontaneous firing test defined by the mean firing rate of the model = " + str(a_prediction) + " compared against the observed experimental data " + str(observation) + " whose " + str(score)
        if score.score==1:
            ans = "The model " + model.name + " passed the " + self.__class__.__name__ + ". The mean firing rate of the model = " + str(a_prediction) + " and the validation data is " + str(observation)
        else:
            ans = "The model " + model.name + " failed the " + self.__class__.__name__ + ". The mean firing rate of the model = " + str(a_prediction) + " and the validation data is " + str(observation)
        print(ans)
        return score
        #computed_scores = {}
        #for cell_region in model.cell_regions:
        #    a_prediction = self.processed_prediction[cell_region][1]
        #    a_binary = BinaryScore.compute( a_prediction,
        #                                    observation )
        #    a_score = {cell_region: BinaryScore(a_binary.score)}
        #    computed_scores.update(a_score)


