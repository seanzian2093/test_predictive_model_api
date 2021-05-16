# test_predictive_model_api
A Python package for easy testing API of predictive models.

## Predictive Model API
A typical predictive model accepts one or more features and return a prediction which could be a continious number or a categorical label. For example, a fraud detection model in financial service industry may accept featuers like age, income, occupation, etc and return a label of Fraudent or Not, or return a numerical score indicating the likelihood of fraud.

* A typical input could be 
`{"age": 27, "gender": "male", "marital_status": "Y"}`

* A typical output could be
`{"RiskGroup": "Grp2"}`

* Another typical output could be
`["Invalida age", "Invalid gender"]`

## PM Test v.s. Unit Test
This package is dedicated to test if return values are same as expected, assuming all utilities are functioning normally, e.g. network traffic, authetication, etc.   Also tests in this package are expected to be representive of all the combination of features, if not exhaustive.

Some predictive models also return infomative messages by validating features they accept to inform the API caller the reason why a prediction can not be yielded. These cases are also tested in this package.

## Usage

* import and call main() by providing a file path to your config file in JSON format.

`import main from main; main(config_fp)`

* A config file should be of below structure

`
{
  "id": "your_test_id",
  "url": "your_api_url",
  "auth": {
    "auth_type": "Basic Auth",
    "username": "env_id",
    "password": "env_pwd"
  },
  "input_json": "api_input.json",
  "sample_rate": 0.10,
  "return_key": "key_in_the_returned_dictionary",
  "expected_json": "api_expected.json",
  "type": "your_api_type"
}
`

* username and passowrd should be the environment variables where your real ones are stored for security consideration.

* `"id"` and `"type"` are information purpose, are not involved in testing process.

* `"sample_rate"` is to sample a portion of all your test samples.