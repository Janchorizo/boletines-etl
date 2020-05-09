from params.global_params import GlobalParams
import inspect

class TestGlobalParams:
    def test_parameters(self):
        expected_parameters = ('base_dir',)
        parameters = GlobalParams.get_param_names()

        all_parameters_present = all(
            map(lambda param: param in parameters, expected_parameters)
        )
        equal_length = len(expected_parameters) == len(parameters)

        assert equal_length and all_parameters_present
