# ============================================================================
# test_for_quasilinear_behavior.py
#
# created  01 September 2017 Lungsi
# modified 05 October 2017 Lungsi
#
# ============================================================================

import sciunit
import quantities as pq
from elephant.statistics import mean_firing_rate as mfr

from cerebunit.capabilities.cells.response import ProducesSpikeTrain
from cerebunit.score_manager import BinaryScore


class QuasiLinearTest(sciunit.Test, BinaryScore):
    '''
    ff
    '''
    required_capabilities = (ProducesSpikeTrain,)
    score_type = BinaryScore

    def generate_prediction(self, model, verbose=False):
        '''
        fdf
        '''
        # ============Ramp Up and then Down Step Currents (nA)==============
        self.ramp_up_down_currents = \
                { "current1": {"amp": 0.2, "dur": 1000.0, "delay": 1000.0},
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
                  "current2": {"amp": 0.2, "dur": 1000.0, "delay": 2000.0} # current15 delay 15000
                }
        model.set_stimulation_properties( self.ramp_up_down_currents )
        # =============================================================
        self.setup_parameters = { "dt": 0.025,   "celsius": 37,
                                  "tstop": 3000, "v_init": -65 } # tstop 17000
        model.set_simulation_properties(self.setup_parameters)
        # =============================================================
        model.produce_spike_train()
        return model

    def get_prediction_for_each_current(self, model):
        '''
        fsd
        '''
        last_I_id = len(self.ramp_up_down_currents)
        # get all the spike train for desired cell region
        cell_region = "vm_soma"
        response_type = "spike_train"
        all_spike_train = model.predictions[response_type][cell_region]
        # ========For Ramp-Up
        # get spike_train for 1st no_current
        spike_start = 0.0
        spike_stop = self.ramp_up_down_currents["current1"]["delay"]
        ramp_up_spike_train_for = \
                { "current0":
                  all_spike_train.time_slice(spike_start, spike_stop) }
        # ========For Ramp-Down
        # get spike_train for last no_current
        spike_start = self.ramp_up_down_currents["current"+str(last_I_id)]["delay"] \
                      + self.ramp_up_down_currents["current"+str(last_I_id)]["dur"]
        spike_stop = self.setup_parameters["tstop"]
        ramp_down_spike_train_for = \
                { "current0":
                  all_spike_train.time_slice(spike_start, spike_stop) }
        # ========Setup indices for Ramp-Up and Ramp-Down
        no_of_Iclamps = len(self.ramp_up_down_currents)
        ramp_up_start_idx = 1
        if no_of_Iclamps % 2 == 0:
            ramp_up_stop_idx = no_of_Iclamps / 2
            ramp_down_start_idx = ramp_up_stop_idx + 1
        else:
            ramp_up_stop_idx = (no_of_Iclamps - 1) / 2
            ramp_down_start_idx = ramp_up_stop_idx + 2
        ramp_down_stop_idx = no_of_Iclamps
        #
        ramp_up_indices = [k+1 for k in list(range(ramp_up_stop_idx))]
        ramp_down_indices = [k+1 for k in list(range(ramp_down_stop_idx))]
        #
        ramp_up_idx = 1
        ramp_down_idx = 1
        # =========Loop through
        for i in range(no_of_Iclamps):
            #
            inj_times = self.ramp_up_down_currents["current"+str(i+1)]
            spike_start = inj_times["delay"]
            spike_stop = spike_start + inj_times["dur"]
            #
            if (i+1) in ramp_up_indices:
                spike_train = \
                        { "current"+str(ramp_up_idx):
                          all_spike_train.time_slice(spike_start, spike_stop) }
                ramp_up_spike_train_for.update(spike_train)
                ramp_up_idx += 1
            elif (i+1) in ramp_down_indices:
                spike_train = \
                        { "current"+str(ramp_down_idx):
                          all_spike_train.time_slice(spike_start, spike_stop) }
                ramp_down_spike_train_for.update(spike_train)
                ramp_down_idx += 1
        # ==============================
        # return the spike_train_for dictionary
        return ramp_up_spike_train_for, ramp_up_spike_train_for

    def process_prediction(self, model):
        '''
        fsd
        '''
        ramp_up_spike_train_for, ramp_down_spike_train_for = \
                        self.get_prediction_for_each_current(model)
        #
        ramp_up_mean_spike_freq = {}
        for current_id, spike_array in ramp_up_spike_train_for.iteritems():
            x = mfr(spike_array)
            ramp_up_mean_spike_freq.update({current_id: x.rescale(pq.Hz)})
        #
        ramp_down_mean_spike_freq = {}
        for current_id, spike_array in ramp_down_spike_train_for.iteritems():
            x = mfr(spike_array)
            ramp_down_mean_spike_freq.update({current_id: x.rescale(pq.Hz)})
        #
        return ramp_up_mean_spike_freq, ramp_down_mean_spike_freq

    def compute_score(self, observation, model, verbose=False):
        '''
        fdfd
        '''
        ramp_up_mean_spike_freq_for, ramp_down_mean_spike_freq_for = \
                                        self.process_prediction(model)
        score_for = {}
        list_of_scores = []
        for current_id in ramp_up_mean_spike_freq_for.keys():
            if current_id in ramp_down_mean_spike_freq_for.keys():
                observation = ramp_up_mean_spike_freq_for[current_id]
                a_prediction = ramp_down_mean_spike_freq_for[current_id]
                x = BinaryScore.compute( observation, a_prediction )
                y = BinaryScore(x)
                score_for.update({current_id: y})
                list_of_scores.append(y.score)
        #
        score.score = sum(list_of_scores)
        score.score_for = score_for
        return score


