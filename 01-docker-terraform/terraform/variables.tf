variable "credentials_file" {
    description = "The path to the service account key file"
    default = "./keys/credentials.json"
}

variable "project" {
  description = "Project"
  default = "terraform-demo-448100"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
    description = "The location of the resources"
    default = "US"
}

variable "bq_dataset_name" {
    description = "My BigQuery dataset name"
    default = "demo_dataset"
}

variable "gcs_bucket_name" {
    description = "Bucket name"
    default = "terraform-demo-448100-demo-bucket"
}

variable "gcs_storage_class" {
    description = "Bucket storage class"
    default = "STANDARD"
}