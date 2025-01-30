import onnxruntime as ort  
import numpy as np

def load_and_predict_onnx(model_path: str, X_test):
    # Initialize the ONNX Runtime session
    session = ort.InferenceSession(model_path)

    # Prepare the input data for prediction
    input_name = session.get_inputs()[0].name
    X_test_onnx = np.array(X_test, dtype=np.float32)

    # Perform inference
    y_pred = session.run(None, {input_name: X_test_onnx})[0]
    
    return y_pred