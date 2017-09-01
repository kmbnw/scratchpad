
#library(optparse)

#option_list <- list(
#  make_option(c("--nrounds"), type="integer", default = 200),
#  make_option(c("--maxdepth"), type="integer", default = 6),
#  make_option(c("--eta"), type="numeric", default = 0.3),
#  make_option(c("--gamma"), type="numeric", default = 1),
#  make_option(c("--subsample"), type="numeric", default = 1),
#  make_option(c("--minchildweight"), type="numeric", default = 1),
#  make_option(c("--colsamplebytree"), type="numeric", default = 1)
#)

#opt = parse_args(OptionParser(option_list=option_list))

df.vars <- data.frame(
    EnvVar = c(
        'XGB_NROUNDS',
        'XGB_MAXDEPTH',
        'XGB_ETA',
        'XGB_GAMMA',
        'XGB_SUBSAMPLE',
        'XGB_MIN_CHILD_WEIGHT',
        'XGB_COLSAMPLE_BYTREE'),
    OptVar = c(
        'nrounds',
        'maxdepth',
        'eta',
        'gamma',
        'subsample',
        'minchildweight',
        'colsamplebytree'),
    Default = c(
        200,
        6,
        0.3,
        1,
        1,
        1,
        1)
)

m.vars <- Sys.getenv(df.vars$EnvVar)

opt <- lapply(1:nrow(df.vars), function(idx) {
    if (m.vars[[idx]] == "") {
        df.vars[idx, 'Default', ]
    } else {
        as.numeric(m.vars[[idx]])
    }
})
names(opt) <- df.vars$OptVar

df <- read.table(
    '/data/housing.data.txt',
    sep = '\t',
    header = TRUE,
    strip.white = TRUE)

#    1. CRIM      per capita crime rate by town
#    2. ZN        proportion of residential land zoned for lots over 
#                 25,000 sq.ft.
#    3. INDUS     proportion of non-retail business acres per town
#    4. CHAS      Charles River dummy variable (= 1 if tract bounds 
#                 river; 0 otherwise)
#    5. NOX       nitric oxides concentration (parts per 10 million)
#    6. RM        average number of rooms per dwelling
#    7. AGE       proportion of owner-occupied units built prior to 1940
#    8. DIS       weighted distances to five Boston employment centres
#    9. RAD       index of accessibility to radial highways
#    10. TAX      full-value property-tax rate per $10,000
#    11. PTRATIO  pupil-teacher ratio by town
#    12. B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks 
#                 by town
#    13. LSTAT    % lower status of the population
#    14. MEDV     Median value of owner-occupied homes in $1000's

m.formula <- as.formula(
    paste('~',
        paste(
            'CRIM',
            'ZN',
            'INDUS',
            'CHAS',
            'NOX',
            'RM',
            'AGE',
            'DIS',
            'RAD',
            'TAX',
            'PTRATIO',
            'B',
            'LSTAT',
            sep = ' + ')),
    env = NULL)

m.params <- list(
    eta = opt$eta,
    gamma = opt$gamma,
    max_depth = opt$maxdepth,
    min_child_weight = opt$minchildweight,
    subsample = opt$subsample,
    colsample_bytree = opt$colsamplebytree
)

set.seed(1095)
folds <- caret::createFolds(df$MEDV, k = 10)

m.x = model.matrix(m.formula, df)

m.error <- do.call(
    c,
    lapply(folds, function(fold) {
        fit <- xgboost::xgboost(
            xgboost::xgb.DMatrix(m.x[-fold, ], label = df$MEDV[-fold]),
            params = m.params,
            nrounds = opt$nrounds)
        yhat <- predict(fit, m.x[fold, ])
        y <- df$MEDV[fold]
        return (y - yhat)
    }))

m.rmse <- sqrt(mean(m.error ^ 2))
df.out <- as.data.frame(opt)
df.out$RMSE <- m.rmse

jsondata <- jsonlite::toJSON(df.out, pretty = TRUE)
conn <- file("/output/metrics.json")
writeLines(jsondata, conn)
close(conn)
