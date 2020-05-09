from params.s3_params import S3Params

class TestS3Params:
	def test_parameters(self):
		expected_parameters = (
			'aws_access_key_id',
			'aws_secret_access_key',
			'aws_session_token'
		)
		parameters = S3Params.get_param_names()

		all_parameters_present = all(
			map(lambda param: param in parameters, expected_parameters)
		)
		equal_length = len(expected_parameters) == len(parameters)

		assert equal_length and all_parameters_present
