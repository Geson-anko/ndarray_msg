# Tensor message type for pure numerical data
string dtype          # numpy dtype name (e.g., 'float32', 'float64', 'int64')
uint32[] shape        # tensor dimensions
uint32 data_size      # total number of elements
byte[] data          # serialized tensor data
