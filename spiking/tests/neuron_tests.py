"""
Tests the spiking.neuron module.  A few points: 
  - There are no network oriented checks.
  - Only tests the neuron works as expected.
"""
from cyrusbus import Bus
import time
from nose.tools import *

from spiking.neuron import SpikingNeuron

def test_spiking_neuron():
  bus = Bus()

  neuron = SpikingNeuron('<1,1>', bus,
      efficacy_pause=2,
      efficacy_duration=4,
      arp=2,
      threshold=1.5)

  presynaptic = SpikingNeuron('<0,1>', bus,
      efficacy_pause=2,
      efficacy_duration=4,
      arp=2,
      threshold=1.5)

  presynaptic.attach(neuron)

  eq_(neuron.compute(), 0, 
      "Expected no preexisting action-potential") 

  test_flag = {'foo': 'bar'} 

  # Create a mock neuron class
  class MockNeuron:
    def __init__(self, test_flag):
      self.test_flag = test_flag

    def activate(self, bus, signal=None):
      self.test_flag['foo'] = 'baz'
       

  # Attach a mock neuron to 'neuron' to detect firings.
  neuron.attach(MockNeuron(test_flag))

  # Activate the presynaptic neuron
  presynaptic._fire()
  presynaptic._fire()
  presynaptic._fire()

  for i in range(1, 10):
    neuron.touch()
    time.sleep(0.0005)

  # Allow time for spikes to propagate
  time.sleep(1)
  eq_(test_flag['foo'], 'baz', 
      "This flag should be True")
