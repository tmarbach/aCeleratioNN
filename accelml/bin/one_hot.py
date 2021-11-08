import numpy as np
from keras.utils import to_categorical
### Categorical data to be converted to numeric data
behaviors = ["s","l","t","c","a","d","i","w"]

### Universal list of colors
total_behaviors = ["s","l","t","c","a","d","i","w"]

### map each color to an integer
mapping = {}
for x in range(len(total_behaviors)):
  mapping[total_behaviors[x]] = x

# integer representation
for x in range(len(behaviors)):
  behaviors[x] = mapping[behaviors[x]]

one_hot_encode = to_categorical(behaviors)
print(one_hot_encode)
