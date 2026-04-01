# 1. S3 Bucket for Machine Learning Data and Model Artifacts
resource "aws_s3_bucket" "ml_data_bucket" {
  bucket_prefix = "fraud-detection-ml-data-" # AWS requires globally unique bucket names, prefix helps with this
  force_destroy = true                       # Allows us to easily delete the bucket later during cleanup
}

# 2. Elastic Container Registry for the Docker Image
resource "aws_ecr_repository" "app_repo" {
  name                 = "fraud-detection-api"
  image_tag_mutability = "MUTABLE"

  # Scans your Docker images for security vulnerabilities automatically
  image_scanning_configuration {
    scan_on_push = true
  }
}

# Output the exact names so we can use them in our next steps
output "s3_bucket_name" {
  value = aws_s3_bucket.ml_data_bucket.bucket
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}