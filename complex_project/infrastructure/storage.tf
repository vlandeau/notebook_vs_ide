resource "aws_s3_bucket" "data" {
  bucket = "bootcamp-2021-01-data"
  acl    = "private"
}

resource "aws_s3_bucket_policy" "data-policy" {
  bucket = aws_s3_bucket.data.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "BOOTCAMP-2021-01BUCKETPOLICY",
  "Statement": [
    {
      "Sid": "IPAllow",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::bootcamp-2021-01-data/*"
    }
  ]
}
POLICY
}
