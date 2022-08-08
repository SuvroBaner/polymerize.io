# polymerize.io

## Set-up your environment (Windows)

pip install virtualenv

python -m venv polymerize_env

polymerize_env\Scripts\activate

git clone git@github.com:SuvroBaner/polymerize.io.git

cd polymerize.io

pip install -r requirements.txt

## Run the application

Fom the root folder (polymerize.io) run the below command-

uvicorn app.main:app --reload

## Use Swagger (Open API) docs to send request -

http://127.0.0.1:8000/v1/polymerize_predict/docs

Request URL:

http://127.0.0.1:8000/v1/polymerize_predict/predict_roughness?api_key=1234

Curl :

curl -X 'POST' \
  'http://127.0.0.1:8000/v1/polymerize_predict/predict_roughness?api_key=1234' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "num_points": 100,
  "response_bin": "low"
}'

## Request & Response

Request Body :

{
  "num_points": 100,
  "response_bin": "low"
}

Note - 

"num_points" - > integer. PLease provide the number of observations you want to generate

"response_bin" - > The values are either "low", "medium" or "high"


Sample Response -

```{
  "status": true,
  "message": "The response is successful",
  "input_samplespace": {
    "layer_height": [
      0.007881018603815931,
      0.05643405486620378
    ],
    "wall_thickness": [
      2.0977267155834642,
      6.939230263133773
    ],
    "infill_density": [
      48.945156479585066,
      87.39971635095745
    ],
    "print_speed": [
      88.40959678745978,
      125.64716524863368
    ],
    "infill_pattern_honeycomb": [
      1.0010004457205604,
      0.6345485272789351
    ],
    "material_pla": [
      0.13466285924421406,
      -0.0780016608201401
    ]
  },
  "predictions": [
    66.03547674472648,
    159.45610735551273
  ]
}```


## Descriptive Statistical Insights -
A good start is to look at some descriptive statistics -

1. There are in total 46 datapoints
2. There are two categorical variables which need to be one-hot encoded
3. The mean of each term shows that the data needs to be normalized before the model is trained.
4. **Correlation** with the response variable : 
    * 'roughness' : 'layer_height'(0.77) and 'nozzle_temperature'(0.41) are **positively** correlated AND 'wall_thickness' (-0.20) is **negatively** correlated
    * 'tensile_strength' : 'wall_thickness'(0.43) and 'elongation'(0.84) are **positively** correlated 'nozzle_temperature'(-0.42), 'bed_temperature'(-0.27), 'print_speed'(-0.27), 'fan_speed'(-0.27) are **negatively** correlated
    * 'elongation': 'layer_height'(0.49) and 'tensile_strength'(0.84) are **positively** correlated and 'nozzle_temperature'(-0.52), 'bed_temperature'(-0.29), 'print_speed'(-0.23) and 'fan_speed'(-0.29) are **negatively** correlated
5. For **Categorical Variables** (infill_pattern and 'material')-
    * There is a similar distribution of "infill_pattern" and "material" with respect to the target feature "roughness" with a mean value close to 200 resulting in roughness
    * For "tensile_strength" both the values of "infill_pattern" i.e. "grid" and "honeycomb" have similar distributions resulting a mean value of approx 20 for the tensile_strength.
    * 'material' values 'pla' yields a mean of 25 'tensile_strength' and 'abs' yields a mean of '15' in 'tensile_strength'. This shows a distinct variability.
    * Both 'infill_pattern' values 'grid' and 'honeycomb' results in a similar distribution of response variable 'elongation' with a mean value close to 1.5
    * There is a high variability of the response 'elongation' with respect to the type of 'materials'. The mean value of 'elongation' is close to 1 for 'material' type 'abs' and the mean value of 'elongation' is close to 2 for 'material' type 'pla'
    
## Normality Test
An important decision point whether to use a Parametric or Non-parametric statistical methods depends on how the data is distributed and how a sample is drawn from a given distribution.
* Parametric Statistical Methods : It assumes that the data follows a Gaussian or Normal distribution.
* Non-parametric Statistical Methods : The distribution of data need not be a normal distribution.

### Quantile-Quantile (QQ plot)
This plot generates its own sample of the idealized distribution that we are comparing with, in this case the Gaussian distribution. The idealized samples are divided into groups, called quantiles. Each data point in the sample is paired with a similar member from the idealized distribution at the same cumulative distribution.

The resulting points are plotted as a scatter plot with the idealized value on the x-axis and the data sample on the y-axis. A perfect match for the distribution will be shown by a line of dots on a 45-degree angle from the bottom left of the plot to the top right. Often a line is drawn on the plot to help make this expectation clear. Deviations by the dots from the line shows a deviation from the expected distribution.

### Normality Insights - Part 1
* From the QQ plot we can see that "Roughness" is very close to a Gaussian Distribution.
* However 'tensile_strength' and 'elongation' have some deviations from the Gaussian Distribution, but it is not that different.

So, we will test it further using few Statistical Normality Tests.
The following tests assume that the sample was drawn from a Gaussian Distribution. This is called the Null Hypothesis (H0). A threshold level is chosen called alpha, typically 5 % (or 0.05), that is used to interpret the p-value

* p <= alpha : reject H0 (or accept Alternative Hypothesis H1), i.e. not normal
* p > alpha : fail to reject H0, i.e. normal

So, in general we are seeking results with a larger p-value to confirm that our sample was likely drawn from a Gaussian Distribution.

### Normality Insights - Part 2
* In Shapiro-Wilk test : 'roughness' and 'tensile_strength' came out to be drawn from a Gaussian (normal) distribution. However 'elongation' seems to be non-normal.
* In D Agostino's k^2 test : 'roughness' and 'elongation' came out to be drawn from a Gaussian (normal) distribution. However 'tensile_strength' seems to be non-normal.

So, we will definitely consider 'roughness' coming from a normal distribution and will go for a parameteric statistical model.
And, 'tensile_strength' and 'elongation' seem to be soft fail, so we will try out both parametric and non-parametric statistical model.

#### Evaluating the Linear Regression Model on "roughness"
* MAE is the easiest to understand, because it's the average error.
* MSE is more popular than MAE, because MSE "punishes" larger errors, which tends to be useful in the real world.
* RMSE is even more popular than MSE, because RMSE is interpretable in the "y" units.
* R-squared : (coefficient of determination) regression score function. Score close to 1 is the goodness of fit

* MAE: 36.944464480366506
* MSE: 2039.4781899144302
* RMSE: 45.160582258363654
* R-squared: 0.8248963910144327

### Feature selection using (significant coefficients) using t-stats and p-values
* ['layer_height', 'nozzle_temperature', 'bed_temperature', 'fan_speed', 'material']

* MAE: 34.606584112319624
* MSE: 2473.428834888112
* RMSE: 49.73357854496408
* R-squared: 0.7876386628208821

#### Fixing Multicollinearity -

VIF (Variable Inflation Factors) determines the strength of the correlation between the independent variables. It is predicted by taking a variable and regressing it against every other variable. 

VIF = 1 / (1 - R^2)

* VIF starts at 1 and has no upper limit
* VIF = 1, no correlation between the independent variable and the other variables
* VIF exceeding 5 or 10 indicates high multicollinearity between this independent variable and the others

We can clearly see that the following features are highly multicollinear-
* nozzle_temperature
* bed_temperature
* fan_speed
* material_pla

Let's fix this by droping the variables iteratively and checking back the VIFs, we will start the max ones 

One heuristic could be that we can drop of the temperatures. Let's see-

Final Results -

['layer_height',
 'wall_thickness',
 'infill_density',
 'print_speed',
 'infill_pattern_honeycomb',
 'material_pla']
 
* MAE: 51.84332052789431
* MSE: 4584.0861268399585
* RMSE: 67.70587955886813
* R-squared: 0.606423825133415

### Further improvements -

* Auto-correlation of error terms can be checked.
* Normalizing the inputs 
* Do more robust feature selection like doing regularization (Ridge Regression using L2 norm and Lasso using L1 norm)
* Bias Variance trade-off using k-fold cross-validation
* Bin the response feature into high, medium and low and perform classification task on them
* Adding non-linearity to the model
* Using non-parametric methods like Random forst, Boosting and Support Vector Machines
* Before regression we could do an unsupervised learning and do the feature selection based on that and then regress
* Finally use a shallow neural network (multi-layer perceptron) to capture the non-linearity and intercation terms and minimize the mean squared error loss function.
* Can augment the training data using the open-source

# Exploration and Optimization -

Uniform Distribution of Y "roughness"

Generating the inputs -

Draw random samples from a normal (Gaussian) distribution.

The probability density function of the normal distribution, is often called the bell curve because of its characteristic shape (see the example below).

The normal distributions occurs often in nature. For example, it describes the commonly occurring distribution of samples influenced by a large number of tiny, random disturbances, each with its own unique distribution

The probability density for the Gaussian distribution is

p(x) = (1 / sqrt(2*pi*sigma^2)) * exp^(-(x - mu)^2 / 2*sigma^2)

where  is the mean and  the standard deviation. The square of the standard deviation, , is called the variance.

The function has its peak at the mean, and its “spread” increases with the standard deviation (the function reaches 0.607 times its maximum at  and  [2]). This implies that normal is more likely to return samples lying close to the mean, rather than those far away.

The generateDistribution() would be used to generate the input space of features which will be used to regress the "Roughness" for which we already have a model trained. You can think of these as partial derivaties and if you sum them up, it gives you the value of the Total Derivatives. Higher the total derivative, higher the final value of roughness. We come to this step where internally the Mean Squared Error Loss function is optimized.

