# test_predictive_model_api
A Python package for easy testing API of predictive models.

## Predictive Model API
A typical predictive model accepts one or more features and return a prediction which could be a continious number or a categorical label. For example, a fraud detection model in financial service industry may accept featuers like age, income, occupation, etc and return a label of Fraudent or Not, or return a numerical score indicating the likelihood of fraud.

## PM Test v.s. Unit Test
This package is dedicated to test if return values are same as expected, assuming all utilities are functioning normally, e.g. network traffic, authetication, etc.   Also tests in this package are expect to be representive of all the combination of features, if not exhaustive.

Some predictive models also return infomative messages by validating features they accept to inform the API caller the reason why a prediction can not be yielded. These cases are also tested in this package.
