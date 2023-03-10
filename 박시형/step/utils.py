import numpy as np


class Variable:
  def __init__(self, data) -> None:
    if data is not None:
      if not isinstance(data, np.ndarray):
        raise TypeError(f'{type(data)}는 지원하지 않는 타입입니다.')
    self.data = data
    self.grad = None
    self.creator = None
  
  def set_creator(self, func):
    self.creator = func
  
  def backward(self):
    if self.grad is None:
      self.grad = np.ones_like(self.data)
    
    funcs = [self.creator]
    while len(funcs) != 0:
      f = funcs.pop()
      x, y = f.input, f.output
      x.grad = f.backward(y.grad)
      
      if x.creator is not None:
        funcs.append(x.creator)
    
    
class Function:
  def __call__(self, input: Variable):
    x = input.data
    y = self.forward(x)
    output = Variable(self._as_array(y))
    output.set_creator(self)
    self.input = input
    self.output = output
    return output
  
  def forward(self, x):
    raise NotImplementedError

  def backward(self, gy):
    raise NotImplementedError
  
  @staticmethod
  def _as_array(x):
    if np.isscalar(x):
      return np.array(x)
    return x
  
  
class Square(Function):
  def forward(self, x):
    return x **2
  
  def backward(self, gy):
    x = self.input.data
    gx = 2 * x * gy
    return gx

class Exp(Function):
  def forward(self, x):
    return np.exp(x)
  
  def backward(self, gy):
    x = self.input.data
    gx = np.exp(x) * gy
    return gx
  
  
def square(x):
  return Square()(x)


def exp(x):
  return Exp()(x)


def numerical_diff(f, x: Variable, eps=1e-4):
  x0 = Variable(x.data - eps)
  x1 = Variable(x.data + eps)
  y0 = f(x0)
  y1 = f(x1)
  return (y1.data - y0.data) / (2 * eps)