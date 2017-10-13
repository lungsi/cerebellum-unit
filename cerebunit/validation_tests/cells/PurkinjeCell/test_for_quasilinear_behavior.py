# ============================================================================
# test_for_quasilinear_behavior.py
#
# created  06 September 2017 Lungsi
# modified 09 October 2017 Lungsi
#
# ============================================================================
#
import sciunit
import quantities as pq
from elephant.statistics import mean_firing_rate as mfr
#
from cerebunit.capabilities.cells.response import ProducesSpikeTrain
from cerebunit.score_manager import BinaryScore, OverallBinaryScore
#
#
class QuasiLinearTest(sciunit.Test, BinaryScore, OverallBinaryScore):
    '''
    The QuasiLinear Test is a test where the model is injected with currents.
    First the model is injected with increasing currents in steps.
    This is followed by decreasing currents (same amplitudes).
    For each respective amplitude current injection the mean spiking frequencies
    are compared. The Binary score is 1 if the frequencies are different.
    The OverallBinary score is 1 if this is the case for all the amplitudes.
    '''
    required_capabilities = (ProducesSpikeTrain,)
    score_type = OverallBinaryScore
#
#
    def generate_prediction(self, model, verbose=False):
        '''
        Generates spike train from "vm_soma", cell region.
        The function is automatically called by sciunit.Test whic this test
        is a child of.
        Therefore as part of sciunit generate_prediction is mandatory.
        '''
        # ============Ramp Up and then Down Step Currents (nA)==============
        self.ramp_up_down_currents = \
                { "current1": {"amp": 0.2, "dur": 100.0, "delay": 100.0},
                  "current2": {"amp": 0.4, "dur": 100.0, "delay": 200.0},
                  "current3": {"amp": 0.5, "dur": 100.0, "delay": 300.0},
                  "current4": {"amp": 0.4, "dur": 100.0, "delay": 400.0},
                  "current5": {"amp": 0.2, "dur": 100.0, "delay": 500.0},
                  #"current1": {"amp": 0.2, "dur": 1000.0, "delay": 1000.0},
                  #"current2": {"amp": 0.4, "dur": 1000.0, "delay": 2000.0},
                  #"current3": {"amp": 0.6, "dur": 1000.0, "delay": 3000.0},
                  #"current4": {"amp": 0.8, "dur": 1000.0, "delay": 4000.0},
                  #"current5": {"amp": 1.0, "dur": 1000.0, "delay": 5000.0},
                  #"current6": {"amp": 1.2, "dur": 1000.0, "delay": 6000.0},
                  #"current7": {"amp": 1.4, "dur": 1000.0, "delay": 7000.0},
                  #"current8": {"amp": 1.6, "dur": 1000.0, "delay": 8000.0},
                  #"current9": {"amp": 1.4, "dur": 1000.0, "delay": 9000.0},
                  #"current10": {"amp": 1.2, "dur": 1000.0, "delay": 10000.0},
                  #"current11": {"amp": 1.0, "dur": 1000.0, "delay": 11000.0},
                  #"current12": {"amp": 0.8, "dur": 1000.0, "delay": 12000.0},
                  #"current13": {"amp": 0.6, "dur": 1000.0, "delay": 13000.0},
                  #"current14": {"amp": 0.4, "dur": 1000.0, "delay": 14000.0},
                  #"current15": {"amp": 0.2, "dur": 1000.0, "delay": 15000.0}
                }
        stimulus = \
                model.set_stimulation_properties( self.ramp_up_down_currents )
        # below line is necessary for the simulation to run "correctly"
        [ stimulus[i].loc(0.5, sec=model.cell.soma) \
                for i in range(len(stimulus)) ]
        # =============================================================
        self.setup_parameters = { "dt": 0.025,   "celsius": 37,
                                  #"tstop": 17000, "v_init": -65 }
                                  "tstop": 600, "v_init": -65 }
        model.set_simulation_properties(self.setup_parameters)
        # =============================================================
        model.produce_spike_train()
        return model
#
#
    def get_spike_train_for_each_current(self, model):
        '''
        The model.produce_spike_train() results in spike train for all
        the current inject in one place
        model.predictions["spike_train"]["vm_soma"]
        This function slices the spike train for ramp-up current phase
        and ramp-down current phases.
        And for each ramp spike trains for each respective current
        amplitude is stored in a dictionary such that
        ramp_currents = {"currentid": sliced_spike_train, ... }
        =======================Use Case================================
        ramp_up_train, ramp_down_train = \
                self.get_spike_train_for_each_current(model)
        ===============================================================
        This function is called by process_prediction
        '''
        last_I_id = len(self.ramp_up_down_currents)
        # get all the spike train for desired cell region
        cell_region = "vm_soma"
        response_type = "spike_train"
        all_spike_train = model.predictions[response_type][cell_region]
        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++Spike trains for current0 => no current injection++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #
        # ====================Setup For Ramp-Up=========================
        # set the time boundaries
        spike_start = 0.0
        spike_stop = self.ramp_up_down_currents["current1"]["delay"]
        # get the spike train for the time boundaries
        ramp_up_spike_train_for = \
                { "current0":
                  all_spike_train.time_slice(spike_start, spike_stop) }
        #
        # ====================Setup For Ramp-Down======================
        # set the time boundaries
        spike_start = \
                self.ramp_up_down_currents["current"+str(last_I_id)]["delay"] \
                + self.ramp_up_down_currents["current"+str(last_I_id)]["dur"]
        spike_stop = self.setup_parameters["tstop"]
        # get the spike train for the time boundaries
        ramp_down_spike_train_for = \
                { "current0":
                  all_spike_train.time_slice(spike_start, spike_stop) }
        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++Spike trains for currenti for each ith current injections++
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #
        # ==========Setup indices for Ramp-Up and Ramp-Down============
        # total number of injections
        no_of_Iclamps = len(self.ramp_up_down_currents)
        ramp_up_start_idx = 1 # first current is current1
        ramp_down_stop_idx = no_of_Iclamps # last current is currentN
        if no_of_Iclamps % 2 == 0:
            # there is no largest current in the middle of ramp-up/down
            # that is, all the currents are repeated in ramp-down
            # so the middle current is the last current in ramp-up
            ramp_up_stop_idx = no_of_Iclamps / 2
            # so ramp-down current starts from ramp-up last current + 1
            ramp_down_start_idx = ramp_up_stop_idx + 1
        else:
            # the largest current is the middle of ramp-up & ramp-down
            # so the last ramp-up current is the one before the largest
            ramp_up_stop_idx = (no_of_Iclamps - 1) / 2
            # so ramp-down current starts from ramp-up last current + 1
            ramp_down_start_idx = ramp_up_stop_idx + 2
        #
        # create list of current indices from current1 for both ramps
        ramp_up_indices = \
                [ k for k in range(ramp_up_stop_idx+1)
                        if k >= ramp_up_start_idx
                        and k <= ramp_up_stop_idx ]
        ramp_down_indices = \
                [ k for k in range(ramp_down_stop_idx+1)
                        if k >= ramp_down_start_idx
                        and k <= ramp_down_stop_idx ]
        #
        # Note: ramp_down_stop_idx is not the last currentID in ramp-down
        # The last currentID in ramp-down = first currentID in ramp-up
        ramp_down_indices.reverse()
        # This is done as follows:
        # ============Loop through each current injection==============
        no_of_I_per_ramp = len(ramp_up_indices) # ramp-up = ramp-down
        for i in range(no_of_Iclamps):
            # currentID in self.ramp_up_down_currents start from current1
            idx = i+1
            # get current stimulation parameters for currenti
            inj_times = self.ramp_up_down_currents["current"+str(idx)]
            # lower bound of the time boundary
            spike_start = inj_times["delay"]
            # upper bound of the time boundary
            spike_stop = spike_start + inj_times["dur"]
            # if the current stimulation is during ramp-up phase
            # i.e idx in ramp_up_indices
            if idx <= ramp_up_stop_idx:
                # slice the spike train from total spike train into a
                # dictionary with respective currenti tag
                spike_train = \
                    { "current"+str(idx):
                        all_spike_train.time_slice(spike_start, spike_stop) }
                # add the dictionary into the dictionary for ramp-up trains
                ramp_up_spike_train_for.update(spike_train)
            # on the other hand if the stimulation is during ramp-down
            # do the above and add the dictionary inot ramp-down trains
            elif idx in ramp_down_indices:
                dwn_idx = ramp_down_indices.index(idx)+1
                spike_train = \
                    { "current"+str(dwn_idx): # 0 is reserved for no injection
                        all_spike_train.time_slice(spike_start, spike_stop) }
                ramp_down_spike_train_for.update(spike_train)
            print ramp_down_indices
        # ============================================================
        # return the dictionaries for both ramp-up and ramp-down phases
        return ramp_up_spike_train_for, ramp_down_spike_train_for
#
#
    def get_prediction_for_each_current(self, ramp_spike_train):
        '''
        For a given ramp (up or down) dictionary of spike trains tagged
        with respective current id their mean frequencies are calculated
        and its magnitude is stored in a dictionary of the form
        {currentid: {mean_freq: magnitude}}
        for all the currents in A ramp.
        ========================Use Case===============================
        ramp_up_mean_spike_freq = \
                self.get_prediction_for_each_current(ramp_up_spike_train)
        ===============================================================
        This function is called by process_prediction
        '''
        ramp_mean_spike_freq = {}
        for current_id, spike_array in ramp_spike_train.iteritems():
            x = mfr(spike_array)
            y = {current_id: {"mean_freq": x.rescale(pq.Hz).item()} } # just the magnitude
            ramp_mean_spike_freq.update(y)
        return ramp_mean_spike_freq
#
#
    def process_prediction(self, model):
        '''
        Once the model has run, this function can be used to process the
        spike_train prediction to get the prediction of interest,
        mean firing rate.
        =======================Use Case===============================
        ramp_up_freq, ramp_down_freq = process_prediction(model)
        ==============================================================
        This function is called by compute_score
        '''
        # First,
        # get spike trains for respective currents during both
        # ramp Up and ramp Down stages
        ramp_up_spike_train, ramp_down_spike_train = \
                        self.get_spike_train_for_each_current(model)
        #
        # Now for each ramps get the spike frequencies
        # For Ramp-Up stage
        # compute and store mean firing rate for each spike train
        ramp_up_mean_spike_freq = \
                self.get_prediction_for_each_current(ramp_up_spike_train)
        # For Ramp-Down stage
        # compute and store mean firing rate for each spike train
        ramp_down_mean_spike_freq = \
                self.get_prediction_for_each_current(ramp_down_spike_train)
        # For both Ramp-Up and Ramp-Down
        # Return the mean firing rates (respective currents)
        print ramp_up_spike_train, ramp_down_spike_train
        print ramp_up_mean_spike_freq, ramp_down_mean_spike_freq
        return ramp_up_mean_spike_freq, ramp_down_mean_spike_freq
#
#
    def compute_score(self, observation, model, verbose=False):
        '''
        This function is like generate_prediction. It is therefore
        called automatically by sciunit which this test is a child of.
        This function with the same name compute_score is also therefore
        mandatory.
        '''
        # Since the model has already run, call process_prediction
        # to get the spike freqs for ramp up and ramp down phases
        ramp_up_mean_spike_freq_for, ramp_down_mean_spike_freq_for = \
                                        self.process_prediction(model)
        score_breakdown = {} # store here the score breakdowns
        list_of_scores = []  # store here the list of scores
        # =======Loop through each current id in ramp up phase======
        # Note: this includes current0, no injection
        for current_id in ramp_up_mean_spike_freq_for.keys():
            # take corresponding freq at ramp up as observation
            raw_observation = ramp_up_mean_spike_freq_for[current_id]
            observation = \
                    { "inequality":
                            "> " + str(raw_observation["mean_freq"]) }
            # if this current id is also in ramp down phase
            if current_id in ramp_down_mean_spike_freq_for.keys():
                # take corresponding freq at ramp down as prediction
                a_prediction = ramp_down_mean_spike_freq_for[current_id]
                # get their Binary score
                x = BinaryScore.compute( observation, a_prediction )
                y = BinaryScore(x)
                # Create details to be added in score_breakdown dict
                step_up_freq = \
                    "stepUp = "+str(raw_observation["mean_freq"])+" Hz"
                step_down_freq = \
                    "stepDown = "+str(a_prediction["mean_freq"])+" Hz"
                if current_id=="current0":
                    score_detail = { current_id: [ "0 nA",
                                                   step_up_freq,
                                                   step_down_freq,
                                                   y ] }
                else:
                    amp = \
                     self.ramp_up_down_currents[current_id]["amp"]
                    score_detail = { current_id: [ str(amp)+" nA",
                                                   step_up_freq,
                                                   step_down_freq,
                                                   y ] }
                # For the respective current id
                # Store the score breakdown in the dictionary
                score_breakdown.update(score_detail)
                # Store the score in the list
                list_of_scores.append(y.score)
        # Send all the scores and its breakdown to get OverallBinary score
        x2 = OverallBinaryScore.compute( list_of_scores, score_breakdown )
        score = OverallBinaryScore(x2)
        if score.score==1:
            score.description = "The model " + model.name + " passed the " + self.__class__.__name__ + ". The mean spike frequencies of a given amplitude of injection during ramp-up phase is greater than those during ramp-down phase."
        else:
            score.description = "The model " + model.name + " failed the " + self.__class__.__name__ + ". The mean spike frequencies of an (or many) amplitude of injection are similar for ramp-up phase versus ramp-down phase."
        print score.description
        return score


