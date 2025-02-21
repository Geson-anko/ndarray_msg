# NDArray message type for pure numerical data
std_msgs/Header header # header information
string dtype          # numpy dtype name (e.g., 'float32', 'float64', 'int64')
uint32[] shape        # ndarray dimensions
uint32 data_size      # total number of elements
uint8[] data          # serialized ndarray data
