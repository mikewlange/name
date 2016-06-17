# Gender and Country Prediction based on full name. Supports Chinese and English spellings.

## Website:

[namepredict.com](https://namepredict.com)

## Usage:

- Gender Classification

```
python scripts/gender_classifier.py etc/params.txt 
```

- Country Classfication

```
tar zxf data/model/country.pkl_02.npy.tgz
```


```
python scripts/country_classifier.py etc/params.txt
```

## Model:

The model was a decison tree with n-gram features, trained on Wikipedia. We subsampled on male names to balance to ratio of male to female. We inferred gender from the number of occurences of masculine words like "he", "him" or "his" and feminine words like "she", "her". We inferred country based on nationality and place of birth.
