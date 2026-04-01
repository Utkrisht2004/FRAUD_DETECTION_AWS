module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "fraud-detection-vpc"
  cidr = "10.0.0.0/16"

  # Using two Availability Zones for high availability
  azs             = ["ap-south-1a", "ap-south-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  # NAT Gateway allows instances in private subnets to reach the internet (needed for downloading packages)
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  # EKS needs these tags to know where to place external load balancers
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  # EKS needs these tags to know where to place internal load balancers
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}