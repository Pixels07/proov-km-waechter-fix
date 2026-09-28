# What I checked, and what the agent got wrong

Write this yourself, in your own words. It is the part of the repo that proves the work is yours.

## What the agent got wrong
The wear calculation used `//`, which is floor division. It dropped the decimal part of the fraction before converting it to a percentage. For example, 14,900 divided by 15,000 became 0 instead of about 0.993, so the result was reported as 0% wear and the car was not flagged. I caught this by running the tests and checking the wear calculation directly. I also checked the mileage conversion: the old code multiplied kilometers by 1.609, which converts miles to kilometers rather than kilometers to miles.

## What I checked before I accepted its work
I checked that wear uses true division and added a test expecting about 99.33% wear for 14,900 km in a 15,000 km interval. I checked that a car with no last-service reading is not treated as due, and added a report test for a missing reading. The service interval remains 15,000 km and the warning threshold remains 80% in both the code and `settings.cfg`. I ran `pytest -q`; all 9 tests passed. I also ran `git diff --check` to check the patch formatting.

## What the data actually said
I compared the labeled breakdown and non-breakdown cars. Their average odometer readings and ages were nearly identical, so those columns did not meaningfully separate the groups. The breakdown cars averaged about 11,678 km since service compared with 7,261 km for other cars, 159.7 versus 131.4 average daily km, and a 0.60 versus 0.51 load factor. Those three metrics showed a real gap, so the risk score uses `km_since_service`, `avg_daily_km`, and `load_factor`, and ignores odometer and age. The score ranks vehicles for screening; it does not guarantee that a vehicle will break down.
