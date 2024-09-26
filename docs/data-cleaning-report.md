## Problems with the data


### 1. Missing prices

- for some rows in the CSV file, the price is missing for the given timestamp.

#### Solution

I considered carrying the previous value forward, or carrying the next value backward (LOCF and NOCB, respectively), but 
I implemented linear interpolation for my data cleaner. My reasoning being, the time-series data is so high-frequency
(with data coming in multiple times a second), that linear interpolation would give me a reasonable approximation for the price, even 
though it takes away some of the entropy that we would expect from the step-like nature of stock prices. I know ARIMA models are sometimes used here,
but keeping in theme with not installing any new packages, and with the fact that the time gaps between items is so small, I thought keeping things linear was "good enough" for the time being.

### 2. Random negative prices

- some rows of the CSV randomly seem to have prices that are negative.

#### Solution

I assumed that the prices were meant to be positive, as stock prices generally can't go negative, so I just took the absolute value of the price.

### 3. Exponent errors (decimal point shifts)

- Some prices seem to randomly have the decimal in the wrong place (that is, the prices have the wrong order of magnitude)

#### Solution

I did a sliding window approach, comparing each element to the median of it's 5 neighbouring elements. If the element was more than 50% smaller than the median, it was considered to be anomolous, and it's order of magnitude was adjusted.

### 4. Multiple entries at the same time-stamp

- There are some entries which have the same time-stamp, though they have different prices and quantities.

#### Solution

Rather than considering one of the two entries to be invalid, I combined the entries. I considered the new price to the volume-weighted average of two entries, and the new volume to be the sum of the two volumes. Though this does sacrifice some of specificity of the data, the combined entry should still have the same statistical effect on the overall dataset.