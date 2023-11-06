import numpy as np
from typing import AsyncIterable


class LayerInfo():
  def __init__(self, input, output, activation = 'relu'):
    self.input = input
    self.output = output
    self.activation = activation


# example
class NeuralNetwork():
  def __init__(self):
    self.seed = 100;
    self.layers = []

  def add_dense(self, output, input = None, activation = 'relu'):
    if(input == None):
      input = self.layers[-1].output
    layer = LayerInfo(input, output, activation)

    self.layers.append(layer)  

  def get_weights(self):
    return self.weights

  def get_bias(self):
    return self.bias

  def set_weights(self, weights):
    self.weights = weights

  def set_bias(self, bias):
    self.bias = bias

  def compile(self):
    self.weights = self.set_initial_weights()
    self.bias = self.set_initial_bias()

  def set_initial_weights(self):
    return [np.random.randn(self.layers[i].output, self.layers[i].input) * 0.1  for i in range(0, len(self.layers))]
 
  def set_initial_bias(self):
    return [np.random.randn(self.layers[i].output, 1) * 0.1  for i in range(0, len(self.layers))]
  
  def sigmoid(self, Z):
    return 1/(1+np.exp(-Z))

  def relu(self, Z):
    return np.maximum(0,Z)

  def softmax(self, Z):
    return np.exp(Z - np.max(Z)) / Z.sum(axis = 0)


  def single_layer_forward_propagation(self, inputs, weights, biases, activation = 'relu'):
    layer_output = np.dot(weights, inputs) + biases

    if activation == 'relu':
      return self.relu(layer_output)
    elif activation == 'sigmoid':
      return self.sigmoid(layer_output)
    elif activation == 'softmax':
      return self.softmax(layer_output)
    else:
      raise Exception("Wrong activation function")
  
  def forward_propagation(self, input):
    current_layer = input[0]

    for index, layer in enumerate(self.layers):
      prev_layer = current_layer
      weights = self.weights[index]
      bias = np.expand_dims(self.bias[index], axis=0)
      current_layer = self.single_layer_forward_propagation(prev_layer, weights, bias)

    return current_layer    

  def predict(self, input):
    return self.forward_propagation(input);