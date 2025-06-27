# Enterprise-Grade Sales & Marketing Data Platform on GCP

**Created by: Ida Bagus Gede Purwa Manik Adiputra**

## Project Objective

This project demonstrates a complete, production-grade ELT data platform built on Google Cloud Platform. It automatically ingests raw e-commerce data, loads it into a BigQuery data warehouse, transforms it into a clean, reliable, and tested analytics data mart using dbt, and orchestrates the entire workflow with Cloud Composer (Airflow).

## Architecture Diagram

![Airflow Pipeline Graph](architecture_screenshot.png)

*Screenshot of the successful Airflow Graph View showing the complete ELT pipeline workflow*

## Technologies Used

- **Cloud Platform**: Google Cloud Platform (GCP)
- **Infrastructure as Code (IaC)**: Terraform
- **Orchestration**: Cloud Composer (Apache Airflow)
- **Data Lake / Storage**: Google Cloud Storage (GCS)
- **Data Warehouse**: Google BigQuery
- **Data Transformation**: dbt (Data Build Tool)
- **Languages**: Python (for Airflow), SQL (for dbt), HCL (for Terraform)
- **Version Control**: Git & GitHub

## Key Features & Skills Demonstrated

- **End-to-End Automation**: The entire pipeline from data loading to transformation is fully automated and orchestrated by Airflow.
- **Infrastructure as Code**: All cloud resources are defined declaratively using Terraform, allowing for repeatable and version-controlled deployments.
- **Modern Data Modeling**: A staging and marts architecture built with dbt, promoting modularity, reusability, and clean data for analytics.
- **Data Quality Assurance**: In-model data tests were created with dbt to ensure the integrity and reliability of the final data assets (e.g., testing for unique and non-null primary keys).
- **Advanced Debugging**: Successfully diagnosed and resolved a wide range of real-world issues including complex IAM permissions, cloud networking failures, environment dependency conflicts, and esoteric caching bugs.

## Project Structure

```
├── terraform/                 # Infrastructure as Code
│   ├── provider.tf           # GCP provider configuration
│   ├── variables.tf          # Project variables
│   ├── network.tf            # VPC and networking setup
│   ├── iam.tf               # Service accounts and permissions
│   ├── gcs.tf               # Cloud Storage buckets
│   ├── bigquery.tf          # BigQuery datasets
│   └── composer.tf          # Cloud Composer environment
├── dbt/                      # Data transformation
│   ├── models/
│   │   ├── staging/         # Raw data cleaning and standardization
│   │   └── marts/           # Business logic and final data models
│   ├── dbt_project.yml      # dbt project configuration
│   └── profiles.yml         # Database connection profiles
├── airflow/
│   └── ecommerce_pipeline_dag.py  # Main orchestration DAG
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Google Cloud Platform account with billing enabled
- Terraform installed locally
- Git installed locally
- Basic knowledge of SQL, Python, and cloud computing concepts

### Deployment Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/idabaguspurwa/Enterprise-Grade-Sales-and-Marketing-Data-Platform.git
   cd Enterprise-Grade-Sales-and-Marketing-Data-Platform
   ```
2. **Configure GCP credentials**

   ```bash
   gcloud auth application-default login
   gcloud config set project your-project-id
   ```
3. **Deploy infrastructure with Terraform**

   ```bash
   terraform init
   terraform plan
   terraform apply
   ```
4. **Upload the DAG to Cloud Composer**

   - The Airflow DAG will be automatically deployed to your Composer environment
   - Monitor the pipeline execution through the Airflow UI

## Data Pipeline Overview

The pipeline consists of four main stages:

1. **Data Ingestion**: Raw CSV files are stored in Google Cloud Storage buckets
2. **Data Loading**: GCS data is loaded into BigQuery staging tables using Airflow operators
3. **Data Transformation**: dbt models transform staging data into clean, analytics-ready marts
4. **Data Quality Testing**: Automated tests ensure data integrity and business rule compliance

## Business Impact

This platform enables:

- **Real-time Analytics**: Business users can query clean, reliable data for decision-making
- **Scalable Architecture**: Can handle growing data volumes without manual intervention
- **Cost Optimization**: Automated lifecycle management and efficient resource utilization
- **Data Governance**: Built-in testing and documentation ensure data quality and lineage

## Future Enhancements

- Implementation of incremental data loading strategies
- Addition of data monitoring and alerting capabilities
- Integration with business intelligence tools (Looker, Tableau)
- Implementation of data catalog and metadata management

---

*This project showcases enterprise-level data engineering skills including cloud architecture, automation, data modeling, and DevOps practices.*
