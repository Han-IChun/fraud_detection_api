import unittest
from inference import InferencePipeline, XGboostModel, XGboostDataTransformor
import numpy as np
import json

class TestInferencePipeline(unittest.TestCase):
    def test_infer_model(self, model_path ='./models/xgboost.json'):
        # read data from data/test_data.json
        data = json.load(open('data/test_inference.json'))
        data, _ = XGboostDataTransformor().transform(data, 'xgboost')
        inference_pipeline = InferencePipeline(XGboostModel(model_path, location='local'))
        output = inference_pipeline.get_inferecne(data)
        
        # Check that the length of the output matches the length of the input data
        self.assertEqual(len(output), len(data))

        # check the output is the same as the expected output
        expected_output = np.array([0, 0, 0, 0, 0])
        self.assertTrue(np.allclose(output, expected_output))

if __name__ == '__main__':
    unittest.main()