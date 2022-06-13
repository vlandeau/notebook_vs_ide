terraform {
  backend "s3" {
    bucket         = "ekinox-tfstates"
    key            = "acceleration/bootcamp-2021-01.tfstate"
    encrypt        = "true"
    region         = "eu-west-1"
    dynamodb_table = "terraform-lock-states"
  }
}
