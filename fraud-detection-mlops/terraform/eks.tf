module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "fraud-detection-eks"
  cluster_version = "1.30"

  # Allows you to connect to the cluster from your local machine
  cluster_endpoint_public_access  = true

  # Hooking the cluster into the VPC we just built
  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets

  # Defining the actual EC2 servers (worker nodes) that will run your app
  eks_managed_node_groups = {
    main = {
      min_size     = 1
      max_size     = 2
      desired_size = 1

      # Using the same instance size you are familiar with for Kubernetes
      instance_types = ["m7i-flex.large"]
    }
  }

  # Automatically gives your AWS CLI user admin access to the cluster
  enable_cluster_creator_admin_permissions = true
}