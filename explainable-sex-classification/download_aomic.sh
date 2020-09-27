mkdir aomic

#mkdir aomic/piop2
#mkdir aomic/piop1
mkdir aomic/id1000


aws s3 sync --no-sign-request s3://openneuro.org/ds002895 aomic/id1000 --exclude "*" --include "sub-*/dwi/*run-1*"
aws s3 sync --no-sign-request s3://openneuro.org/ds002895 aomic/id1000 --exclude "*" --include "sub-*/anat/*run-1*"

#aws s3 sync --no-sign-request s3://openneuro.org/ds002790 aomic/piop2 --exclude "*" --include "sub-*/dwi/*"
#aws s3 sync --no-sign-request s3://openneuro.org/ds002790 aomic/piop2 --exclude "*" --include "sub-*/anat/*"

#aws s3 sync --no-sign-request s3://openneuro.org/ds002785 aomic/piop1 --exclude "*" --include "sub-*/dwi/*"
#aws s3 sync --no-sign-request s3://openneuro.org/ds002785 aomic/piop1 --exclude "*" --include "sub-*/anat/*"