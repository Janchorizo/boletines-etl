from params.db_params import DBParams

class TestDBParams:
	def test_parameters(self):
		expected_parameters = (
			'host',
			'user',
			'password',
			'database'
		)
		parameters = DBParams.get_param_names()

		all_parameters_present = all(
			map(lambda param: param in parameters, expected_parameters)
		)
		equal_length = len(expected_parameters) == len(parameters)

		assert equal_length and all_parameters_present
